"""
Analisis estadistico para validacion de hipotesis (Sprint 4.3).

Hipotesis:
  H1: Metaheuristicas reducen costo >= 5% vs baseline
  H2: GA-SA domina individuales con gap <= 2%
  H3: Reduccion inventario promedio >= 15% (endpoint primario)
  H3-lowrot: Reduccion inventario baja rotacion >= 15% (endpoint secundario)

Tests aplicados:
  - Shapiro-Wilk para normalidad
  - t-test / Wilcoxon de umbral (one-sided)
  - ANOVA + Tukey HSD (vista por corridas)
  - Friedman + Wilcoxon pareado Holm (vista bloqueada por instancia)
  - Cohen's d para tamano de efecto
  - IC 95% para estimaciones

Uso:
    python experiments/scripts/run_statistical_tests.py
    python experiments/scripts/run_statistical_tests.py --csv experiments/results/comparison.csv

Autor: Daniel Andres Castaneda Rodriguez
Sprint: 4.3
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, ".")

import numpy as np
import pandas as pd
from scipy import stats

# ============================================================
# Data classes para resultados
# ============================================================


@dataclass
class HypothesisResult:
    """Resultado de un test de hipotesis."""

    hypothesis: str
    description: str
    test_name: str
    statistic: float
    p_value: float
    effect_size: float  # Cohen's d
    effect_label: str  # small/medium/large
    ci_lower: float  # IC 95% inferior
    ci_upper: float  # IC 95% superior
    metric_value: float  # Valor medio del efecto
    threshold: float  # Umbral de la hipotesis
    verdict: str  # "SUPPORTED" / "NOT_SUPPORTED"
    normality_p: float  # p-value de Shapiro-Wilk
    used_parametric: bool  # True si se uso t-test

    def __repr__(self) -> str:
        return (
            f"{self.hypothesis}: {self.verdict} "
            f"(metric={self.metric_value:.2f}%, p={self.p_value:.4f}, "
            f"d={self.effect_size:.2f} [{self.effect_label}])"
        )


@dataclass
class RankingResult:
    """Resultado del ranking de algoritmos."""

    ranking: list[dict]  # [{algorithm, mean_z, std_z, rank}]
    anova_f: float
    anova_p: float
    tukey_results: list[dict]  # [{group1, group2, p_adj, reject}]
    friedman_chi2: float
    friedman_p: float
    wilcoxon_holm: list[dict]  # [{group1, group2, p_raw, p_adj_holm, reject}]


# ============================================================
# Funciones auxiliares
# ============================================================


def cohens_d(x: np.ndarray, y: np.ndarray) -> float:
    """Calcular Cohen's d para dos muestras."""
    nx, ny = len(x), len(y)
    diff = np.mean(x) - np.mean(y)
    pooled_std = np.sqrt(
        ((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / (nx + ny - 2)
    )
    if pooled_std < 1e-12:
        return 0.0
    return diff / pooled_std


def effect_label(d: float) -> str:
    """Etiquetar tamano de efecto segun Cohen."""
    d = abs(d)
    if d < 0.2:
        return "negligible"
    elif d < 0.5:
        return "small"
    elif d < 0.8:
        return "medium"
    else:
        return "large"


def paired_test(x: np.ndarray, y: np.ndarray, alpha: float = 0.05):
    """Test pareado: t-test si normal, Wilcoxon si no.

    Returns:
        (test_name, statistic, p_value, normality_p, used_parametric)
    """
    diff = x - y

    # Shapiro-Wilk para normalidad de las diferencias
    if len(diff) >= 3:
        norm_stat, norm_p = stats.shapiro(diff)
    else:
        norm_p = 0.0  # No se puede evaluar

    if norm_p > alpha:
        # Normal -> t-test pareado
        stat, p = stats.ttest_rel(x, y)
        return "t-test pareado", stat, p, norm_p, True
    else:
        # No normal -> Wilcoxon signed-rank
        try:
            stat, p = stats.wilcoxon(diff, alternative="two-sided")
        except ValueError:
            # All differences are zero
            stat, p = 0.0, 1.0
        return "Wilcoxon", stat, p, norm_p, False


def confidence_interval_95(data: np.ndarray) -> tuple[float, float]:
    """Calcular IC 95% para la media."""
    n = len(data)
    if n == 0:
        return (float("nan"), float("nan"))
    if n < 2:
        return (float(data[0]), float(data[0]))
    mean = np.mean(data)
    se = stats.sem(data)
    if not np.isfinite(se) or se < 1e-12:
        return (float(mean), float(mean))
    ci = stats.t.interval(0.95, df=n - 1, loc=mean, scale=se)
    if not np.isfinite(ci[0]) or not np.isfinite(ci[1]):
        return (float(mean), float(mean))
    return float(ci[0]), float(ci[1])


def threshold_one_sample_test(
    values: np.ndarray,
    threshold: float,
    alternative: str,
    alpha: float = 0.05,
):
    """Test one-sided de media contra umbral.

    Evalua H1: mean(values) < threshold   si alternative='less'
           o H1: mean(values) > threshold si alternative='greater'
    """
    shifted = values - threshold

    if len(shifted) < 2:
        return "NO_DATA", float("nan"), float("nan"), float("nan"), False

    # Serie constante: evitar warnings/NaN de tests parametricos.
    if np.ptp(shifted) < 1e-12:
        c = float(shifted[0])
        if alternative == "less":
            p = 0.0 if c < 0.0 else 1.0
        else:
            p = 0.0 if c > 0.0 else 1.0
        return "deterministic-constant", 0.0, p, 1.0, False

    if len(shifted) >= 3:
        _, norm_p = stats.shapiro(shifted)
    else:
        norm_p = 0.0

    if norm_p > alpha:
        # Normal: t-test una muestra con alternativa one-sided.
        try:
            stat, p = stats.ttest_1samp(shifted, popmean=0.0, alternative=alternative)
        except TypeError:
            # Fallback para versiones antiguas de SciPy sin 'alternative'.
            stat, p_two_sided = stats.ttest_1samp(shifted, popmean=0.0)
            if alternative == "less":
                p = p_two_sided / 2.0 if stat < 0 else 1.0 - (p_two_sided / 2.0)
            else:
                p = p_two_sided / 2.0 if stat > 0 else 1.0 - (p_two_sided / 2.0)
        return (
            "one-sample t-test (one-sided)",
            float(stat),
            float(p),
            float(norm_p),
            True,
        )

    try:
        stat, p = stats.wilcoxon(shifted, alternative=alternative)
    except ValueError:
        stat, p = 0.0, 1.0
    return "Wilcoxon one-sided", float(stat), float(p), float(norm_p), False


def aggregate_instance_mean(
    df: pd.DataFrame, algorithm: str, metric: str
) -> pd.Series:
    """Promediar una metrica por instancia para un algoritmo."""
    return (
        df[df["algorithm"] == algorithm]
        .groupby("instance", as_index=True)[metric]
        .mean()
    )


# ============================================================
# Tests de hipotesis
# ============================================================


def test_h1(df: pd.DataFrame) -> list[HypothesisResult]:
    """H1: Metaheuristicas reducen costo >= 5% vs baseline.

    Enfoque robusto bloqueado por instancia:
      1) baseline por instancia (determinista)
      2) metaheuristica promedio por instancia (sobre seeds)
      3) test one-sided sobre % mejora vs umbral 5%
    """
    results = []
    meta_algos = ["ga", "sa", "de", "ga_sa"]
    baseline = aggregate_instance_mean(df, "baseline", "z_value")

    for algo in meta_algos:
        algo_data = aggregate_instance_mean(df, algo, "z_value")
        common = baseline.index.intersection(algo_data.index)
        if len(common) < 3:
            continue

        z_base = baseline.loc[common].values.astype(float)
        z_meta = algo_data.loc[common].values.astype(float)
        # % mejora: (Z_meta - Z_baseline) / |Z_baseline| * 100
        improvement = (z_meta - z_base) / np.abs(z_base) * 100.0

        mean_improvement = float(np.mean(improvement))
        ci = confidence_interval_95(improvement)
        d = cohens_d(z_meta, z_base)
        test_name, stat, p, norm_p, parametric = threshold_one_sample_test(
            values=improvement,
            threshold=5.0,
            alternative="greater",
        )

        verdict = (
            "SUPPORTED" if mean_improvement >= 5.0 and p < 0.05 else "NOT_SUPPORTED"
        )

        results.append(
            HypothesisResult(
                hypothesis="H1",
                description=(
                    f"{algo.upper()} vs Baseline: mejora >= 5% "
                    "(promedio por instancia)"
                ),
                test_name=test_name,
                statistic=float(stat),
                p_value=float(p),
                effect_size=float(d),
                effect_label=effect_label(d),
                ci_lower=ci[0],
                ci_upper=ci[1],
                metric_value=mean_improvement,
                threshold=5.0,
                verdict=verdict,
                normality_p=float(norm_p),
                used_parametric=parametric,
            )
        )

    return results


def test_h2(df: pd.DataFrame) -> list[HypothesisResult]:
    """H2: GA-SA domina individuales con gap <= 2%.

    Reporte principal:
      - Gap por instancia (GA-SA promedio vs mejor individual promedio).
    Reporte complementario:
      - Gap por corrida (instance, seed) para trazabilidad historica.
    """
    results = []
    individual_algos = ["ga", "sa", "de"]

    # -----------------------
    # H2 principal: por instancia
    # -----------------------
    gasa_instance = aggregate_instance_mean(df, "ga_sa", "z_value")
    indiv_instance = (
        df[df["algorithm"].isin(individual_algos)]
        .groupby(["instance", "algorithm"], as_index=False)["z_value"]
        .mean()
    )
    best_indiv_instance = indiv_instance.groupby("instance")["z_value"].max()

    common_i = gasa_instance.index.intersection(best_indiv_instance.index)
    if len(common_i) >= 3:
        z_gasa_i = gasa_instance.loc[common_i].values.astype(float)
        z_best_i = best_indiv_instance.loc[common_i].values.astype(float)
        gap_i = (z_best_i - z_gasa_i) / np.abs(z_best_i) * 100.0

        mean_gap_i = float(np.mean(gap_i))
        ci_i = confidence_interval_95(gap_i)
        d_i = cohens_d(z_gasa_i, z_best_i)
        test_name_i, stat_i, p_i, norm_p_i, parametric_i = threshold_one_sample_test(
            values=gap_i,
            threshold=2.0,
            alternative="less",
        )
        verdict_i = "SUPPORTED" if mean_gap_i <= 2.0 and p_i < 0.05 else "NOT_SUPPORTED"

        results.append(
            HypothesisResult(
                hypothesis="H2",
                description=(
                    "GA-SA vs best{GA,SA,DE}: gap <= 2% "
                    "(promedio por instancia)"
                ),
                test_name=test_name_i,
                statistic=float(stat_i),
                p_value=float(p_i),
                effect_size=float(d_i),
                effect_label=effect_label(d_i),
                ci_lower=ci_i[0],
                ci_upper=ci_i[1],
                metric_value=mean_gap_i,
                threshold=2.0,
                verdict=verdict_i,
                normality_p=float(norm_p_i),
                used_parametric=parametric_i,
            )
        )

    # -----------------------
    # H2 complementario: por corrida
    # -----------------------
    ga_sa_run = df[df["algorithm"] == "ga_sa"].set_index(["instance", "seed"])["z_value"]
    best_indiv_run = (
        df[df["algorithm"].isin(individual_algos)]
        .groupby(["instance", "seed"])["z_value"]
        .max()
    )
    common_r = ga_sa_run.index.intersection(best_indiv_run.index)
    if len(common_r) >= 3:
        z_gasa_r = ga_sa_run.loc[common_r].values.astype(float)
        z_best_r = best_indiv_run.loc[common_r].values.astype(float)
        gap_r = (z_best_r - z_gasa_r) / np.abs(z_best_r) * 100.0

        mean_gap_r = float(np.mean(gap_r))
        ci_r = confidence_interval_95(gap_r)
        d_r = cohens_d(z_gasa_r, z_best_r)
        test_name_r, stat_r, p_r, norm_p_r, parametric_r = threshold_one_sample_test(
            values=gap_r,
            threshold=2.0,
            alternative="less",
        )
        verdict_r = "SUPPORTED" if mean_gap_r <= 2.0 and p_r < 0.05 else "NOT_SUPPORTED"

        results.append(
            HypothesisResult(
                hypothesis="H2-run",
                description=(
                    "GA-SA vs best{GA,SA,DE}: gap <= 2% "
                    "(por corrida instance-seed)"
                ),
                test_name=test_name_r,
                statistic=float(stat_r),
                p_value=float(p_r),
                effect_size=float(d_r),
                effect_label=effect_label(d_r),
                ci_lower=ci_r[0],
                ci_upper=ci_r[1],
                metric_value=mean_gap_r,
                threshold=2.0,
                verdict=verdict_r,
                normality_p=float(norm_p_r),
                used_parametric=parametric_r,
            )
        )

    # Comparacion de tiempos: GA-SA vs CBC
    cbc_data = aggregate_instance_mean(df, "cbc_exact", "elapsed_seconds")
    gasa_time = aggregate_instance_mean(df, "ga_sa", "elapsed_seconds")
    common_t = cbc_data.index.intersection(gasa_time.index)
    if len(common_t) >= 3:
        t_cbc = cbc_data.loc[common_t].values.astype(float)
        t_gasa = gasa_time.loc[common_t].values.astype(float)

        ratio = t_gasa / np.maximum(t_cbc, 1e-9)
        mean_ratio = float(np.mean(ratio))

        results.append(
            HypothesisResult(
                hypothesis="H2-time",
                description=f"GA-SA time <= 50% CBC time (ratio={mean_ratio:.2f})",
                test_name="ratio",
                statistic=mean_ratio,
                p_value=float("nan"),
                effect_size=0.0,
                effect_label="n/a",
                ci_lower=float(np.percentile(ratio, 2.5)),
                ci_upper=float(np.percentile(ratio, 97.5)),
                metric_value=mean_ratio * 100,
                threshold=50.0,
                verdict="SUPPORTED" if mean_ratio <= 0.5 else "NOT_SUPPORTED",
                normality_p=float("nan"),
                used_parametric=False,
            )
        )

    return results


def test_h3(df: pd.DataFrame) -> list[HypothesisResult]:
    """H3: Reduccion inventario >= 15% en dos endpoints.

    Endpoint primario (confirmatorio):
      - Inventario promedio total (`avg_inventory`) por instancia.
    Endpoint secundario (exploratorio):
      - Inventario de baja rotacion (`low_rotation_inventory`) por instancia.

    Ambos endpoints se evaluan en esquema bloqueado por instancia.
    """

    def _evaluate_endpoint(
        metric: str,
        hypothesis_name: str,
        endpoint_label: str,
        baseline_positive_only: bool,
        min_informative_n: int,
    ) -> list[HypothesisResult]:
        endpoint_results: list[HypothesisResult] = []
        baseline_inv = aggregate_instance_mean(df, "baseline", metric)
        if baseline_inv.empty:
            return endpoint_results

        for algo in meta_algos:
            algo_inv = aggregate_instance_mean(df, algo, metric)
            common = baseline_inv.index.intersection(algo_inv.index)
            if len(common) < 3:
                continue

            inv_base_all = baseline_inv.loc[common].values.astype(float)
            inv_meta_all = algo_inv.loc[common].values.astype(float)

            if baseline_positive_only:
                valid_mask = np.abs(inv_base_all) > 1e-9
                inv_base = inv_base_all[valid_mask]
                inv_meta = inv_meta_all[valid_mask]
            else:
                inv_base = inv_base_all
                inv_meta = inv_meta_all

            if len(inv_base) < 3:
                endpoint_results.append(
                    HypothesisResult(
                        hypothesis=hypothesis_name,
                        description=(
                            f"{algo.upper()} vs Baseline: reduccion inventario >= 15% "
                            f"({endpoint_label})"
                        ),
                        test_name="NO_DATA",
                        statistic=float("nan"),
                        p_value=float("nan"),
                        effect_size=float("nan"),
                        effect_label="n/a",
                        ci_lower=float("nan"),
                        ci_upper=float("nan"),
                        metric_value=float("nan"),
                        threshold=15.0,
                        verdict="NOT_SUPPORTED",
                        normality_p=float("nan"),
                        used_parametric=False,
                    )
                )
                continue

            reduction = (
                (inv_base - inv_meta) / np.maximum(np.abs(inv_base), 1e-9) * 100.0
            )
            mean_reduction = float(np.mean(reduction))
            ci = confidence_interval_95(reduction)
            d = cohens_d(inv_base, inv_meta)
            test_name, stat, p, norm_p, parametric = threshold_one_sample_test(
                values=reduction,
                threshold=15.0,
                alternative="greater",
            )

            verdict = (
                "SUPPORTED"
                if (
                    len(reduction) >= min_informative_n
                    and mean_reduction >= 15.0
                    and p < 0.05
                )
                else "NOT_SUPPORTED"
            )

            endpoint_results.append(
                HypothesisResult(
                    hypothesis=hypothesis_name,
                    description=(
                        f"{algo.upper()} vs Baseline: reduccion inventario >= 15% "
                        f"({endpoint_label})"
                    ),
                    test_name=test_name,
                    statistic=float(stat),
                    p_value=float(p),
                    effect_size=float(d),
                    effect_label=effect_label(d),
                    ci_lower=ci[0],
                    ci_upper=ci[1],
                    metric_value=mean_reduction,
                    threshold=15.0,
                    verdict=verdict,
                    normality_p=float(norm_p),
                    used_parametric=parametric,
                )
            )

        return endpoint_results

    results: list[HypothesisResult] = []
    meta_algos = ["ga", "sa", "de", "ga_sa"]

    # Endpoint primario confirmatorio
    results.extend(
        _evaluate_endpoint(
            metric="avg_inventory",
            hypothesis_name="H3",
            endpoint_label="endpoint primario: inventario promedio total por instancia",
            baseline_positive_only=False,
            min_informative_n=5,
        )
    )

    # Endpoint secundario exploratorio
    results.extend(
        _evaluate_endpoint(
            metric="low_rotation_inventory",
            hypothesis_name="H3-lowrot",
            endpoint_label="endpoint secundario: baja rotacion por instancia (baseline>0)",
            baseline_positive_only=True,
            min_informative_n=5,
        )
    )

    return results


def compute_ranking(df: pd.DataFrame) -> RankingResult:
    """Ranking de algoritmos con pruebas globales y bloqueadas por instancia."""
    meta_algos = ["ga", "sa", "de", "ga_sa"]
    algo_data = df[df["algorithm"].isin(meta_algos)]

    # Media y std por algoritmo
    summary = algo_data.groupby("algorithm")["z_value"].agg(["mean", "std", "count"])
    summary = summary.sort_values("mean", ascending=False).reset_index()
    summary["rank"] = range(1, len(summary) + 1)

    ranking = [
        {
            "algorithm": row["algorithm"],
            "mean_z": float(row["mean"]),
            "std_z": float(row["std"]) if not pd.isna(row["std"]) else 0.0,
            "count": int(row["count"]),
            "rank": int(row["rank"]),
        }
        for _, row in summary.iterrows()
    ]

    # ANOVA de un factor
    groups = [group["z_value"].values for _, group in algo_data.groupby("algorithm")]

    if len(groups) >= 2 and all(len(g) >= 2 for g in groups):
        f_stat, anova_p = stats.f_oneway(*groups)
    else:
        f_stat, anova_p = float("nan"), float("nan")

    # Tukey HSD
    tukey_results = []
    algo_names = list(algo_data.groupby("algorithm").groups.keys())
    can_run_multi_group_tests = len(groups) >= 2 and all(len(g) >= 2 for g in groups)

    if can_run_multi_group_tests:
        try:
            from scipy.stats import tukey_hsd

            result = tukey_hsd(*groups)
            for i in range(len(algo_names)):
                for j in range(i + 1, len(algo_names)):
                    p_adj = float(result.pvalue[i][j])
                    tukey_results.append(
                        {
                            "group1": algo_names[i],
                            "group2": algo_names[j],
                            "p_adj": p_adj,
                            "reject": p_adj < 0.05,
                        }
                    )
        except (ImportError, AttributeError, ValueError):
            # Fallback: pairwise t-tests with Bonferroni
            n_comparisons = len(algo_names) * (len(algo_names) - 1) // 2
            for i in range(len(algo_names)):
                for j in range(i + 1, len(algo_names)):
                    g1 = algo_data[algo_data["algorithm"] == algo_names[i]][
                        "z_value"
                    ].values
                    g2 = algo_data[algo_data["algorithm"] == algo_names[j]][
                        "z_value"
                    ].values
                    if len(g1) >= 2 and len(g2) >= 2:
                        _, p = stats.ttest_ind(g1, g2)
                        p_adj = min(float(p) * n_comparisons, 1.0)
                        tukey_results.append(
                            {
                                "group1": algo_names[i],
                                "group2": algo_names[j],
                                "p_adj": p_adj,
                                "reject": p_adj < 0.05,
                            }
                        )

    # Friedman bloqueado por instancia (usa medias por instancia para cada algoritmo)
    instance_matrix = (
        algo_data.groupby(["instance", "algorithm"], as_index=False)["z_value"]
        .mean()
        .pivot(index="instance", columns="algorithm", values="z_value")
    )
    ordered_cols = [a for a in meta_algos if a in instance_matrix.columns]
    friedman_chi2, friedman_p = float("nan"), float("nan")
    wilcoxon_holm: list[dict] = []

    if len(ordered_cols) >= 2 and len(instance_matrix) >= 3:
        arrays = [instance_matrix[c].values for c in ordered_cols]
        friedman = stats.friedmanchisquare(*arrays)
        friedman_chi2, friedman_p = float(friedman.statistic), float(friedman.pvalue)

        pair_stats = []
        for g1, g2 in itertools.combinations(ordered_cols, 2):
            diff = (instance_matrix[g1] - instance_matrix[g2]).values.astype(float)
            try:
                st, p = stats.wilcoxon(diff, alternative="two-sided")
            except ValueError:
                st, p = 0.0, 1.0
            pair_stats.append({"group1": g1, "group2": g2, "stat": float(st), "p": float(p)})

        if pair_stats:
            pvals = np.array([x["p"] for x in pair_stats], dtype=float)
            m = len(pvals)
            order = np.argsort(pvals)
            adj = np.empty_like(pvals)
            for rank, idx in enumerate(order):
                adj[idx] = min((m - rank) * pvals[idx], 1.0)

            for i, item in enumerate(pair_stats):
                wilcoxon_holm.append(
                    {
                        "group1": item["group1"],
                        "group2": item["group2"],
                        "statistic": item["stat"],
                        "p_raw": item["p"],
                        "p_adj_holm": float(adj[i]),
                        "reject": bool(adj[i] < 0.05),
                    }
                )

    return RankingResult(
        ranking=ranking,
        anova_f=float(f_stat),
        anova_p=float(anova_p),
        tukey_results=tukey_results,
        friedman_chi2=friedman_chi2,
        friedman_p=friedman_p,
        wilcoxon_holm=wilcoxon_holm,
    )


# ============================================================
# Funciones de reporte
# ============================================================


def print_hypothesis_results(results: list[HypothesisResult]) -> None:
    """Imprimir resultados de hipotesis en consola."""
    print("\n" + "=" * 80)
    print("RESULTADOS DE HIPOTESIS")
    print("=" * 80)

    current_h = ""
    for r in results:
        if r.hypothesis != current_h:
            current_h = r.hypothesis
            print(f"\n--- {r.hypothesis} ---")

        icon = "OK" if r.verdict == "SUPPORTED" else "NO"
        print(f"  [{icon}] {r.description}")
        print(f"      Metrica: {r.metric_value:.2f}% (umbral: {r.threshold}%)")
        print(f"      Test: {r.test_name}, p={r.p_value:.4f}")
        print(f"      Efecto: d={r.effect_size:.3f} ({r.effect_label})")
        print(f"      IC 95%: [{r.ci_lower:.2f}%, {r.ci_upper:.2f}%]")
        print(f"      Normalidad: p={r.normality_p:.4f}")


def print_ranking(ranking: RankingResult) -> None:
    """Imprimir ranking de algoritmos."""
    print("\n" + "=" * 80)
    print("RANKING DE ALGORITMOS")
    print("=" * 80)

    print(f"\nANOVA: F={ranking.anova_f:.2f}, p={ranking.anova_p:.6f}")
    print(
        f"Friedman (bloques por instancia): "
        f"chi2={ranking.friedman_chi2:.2f}, p={ranking.friedman_p:.6f}"
    )

    print(f"\n{'Rank':>4}  {'Algoritmo':<10}  {'Z medio':>15}  {'Std':>12}  {'N':>5}")
    print("-" * 55)
    for r in ranking.ranking:
        print(
            f"  {r['rank']:>2}   {r['algorithm']:<10}  {r['mean_z']:>15,.0f}  "
            f"{r['std_z']:>12,.0f}  {r['count']:>5}"
        )

    if ranking.tukey_results:
        print("\nComparaciones Tukey HSD:")
        for t in ranking.tukey_results:
            sig = "*" if t["reject"] else " "
            print(
                f"  {t['group1']:<8} vs {t['group2']:<8}: p_adj={t['p_adj']:.4f} {sig}"
            )

    if ranking.wilcoxon_holm:
        print("\nComparaciones Wilcoxon pareado + Holm (por instancia):")
        for t in ranking.wilcoxon_holm:
            sig = "*" if t["reject"] else " "
            print(
                f"  {t['group1']:<8} vs {t['group2']:<8}: "
                f"p_raw={t['p_raw']:.4f}, p_holm={t['p_adj_holm']:.4f} {sig}"
            )


def save_results(
    output_dir: Path,
    h1: list[HypothesisResult],
    h2: list[HypothesisResult],
    h3: list[HypothesisResult],
    ranking: RankingResult,
) -> None:
    """Guardar resultados en JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)

    all_hypotheses = h1 + h2 + h3
    payload = {
        "protocol": {
            "version": "v2.1",
            "updated_at": "2026-03-10",
            "alpha": 0.05,
            "primary_analysis_unit": "instance",
            "secondary_analysis_unit": "run",
            "multiple_testing": "Holm (pairwise Wilcoxon in ranking)",
            "h3_primary_endpoint": "avg_inventory",
            "h3_secondary_endpoint": "low_rotation_inventory (exploratory)",
            "h3_min_informative_n": 5,
        },
        "hypothesis_tests": [asdict(r) for r in all_hypotheses],
        "ranking": {
            "algorithms": ranking.ranking,
            "anova_f": ranking.anova_f,
            "anova_p": ranking.anova_p,
            "tukey": ranking.tukey_results,
            "friedman_chi2": ranking.friedman_chi2,
            "friedman_p": ranking.friedman_p,
            "wilcoxon_holm": ranking.wilcoxon_holm,
        },
        "summary": {
            "H1": next(
                (r.verdict for r in h1 if r.hypothesis == "H1"),
                "NO_DATA",
            ),
            "H2": next(
                (r.verdict for r in h2 if r.hypothesis == "H2"),
                "NO_DATA",
            ),
            "H3": next(
                (r.verdict for r in h3 if r.hypothesis == "H3"),
                "NO_DATA",
            ),
            "H3_lowrot": next(
                (r.verdict for r in h3 if r.hypothesis == "H3-lowrot"),
                "NO_DATA",
            ),
        },
    }

    path = output_dir / "statistical_tests.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)
    print(f"\nResultados guardados en: {path}")


# ============================================================
# Main
# ============================================================


def run_statistical_tests(
    csv_path: str = "experiments/results/comparison.csv",
    output_dir: str = "experiments/results",
) -> None:
    """Ejecutar todos los tests estadisticos."""
    csv_file = Path(csv_path)
    if not csv_file.exists():
        print(f"ERROR: No se encontro {csv_file}")
        print("Ejecute run_comparison.py primero.")
        sys.exit(1)

    df = pd.read_csv(csv_file)
    print(f"Datos cargados: {len(df)} filas, {df['algorithm'].nunique()} algoritmos")
    print(f"Instancias: {df['instance'].nunique()}")
    print(f"Algoritmos: {sorted(df['algorithm'].unique())}")

    # Ejecutar tests
    h1 = test_h1(df)
    h2 = test_h2(df)
    h3 = test_h3(df)
    ranking = compute_ranking(df)

    # Reportar
    print_hypothesis_results(h1 + h2 + h3)
    print_ranking(ranking)

    # Guardar
    save_results(Path(output_dir), h1, h2, h3, ranking)

    # Tabla resumen final
    print("\n" + "=" * 80)
    print("TABLA RESUMEN DE HIPOTESIS")
    print("=" * 80)
    print(
        f"\n{'Hipotesis':<12} {'Resultado':>10} {'p-valor':>10} {'Efecto':>10} {'Veredicto':>15}"
    )
    print("-" * 62)
    for r in h1 + h2 + h3:
        print(
            f"{r.hypothesis:<12} {r.metric_value:>9.2f}% {r.p_value:>10.4f} "
            f"d={r.effect_size:>6.3f}  {r.verdict:>15}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tests estadisticos para validacion de hipotesis (Sprint 4.3)"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="experiments/results/comparison.csv",
        help="Ruta al CSV de resultados de comparacion",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="experiments/results",
        help="Directorio para guardar resultados",
    )
    args = parser.parse_args()

    run_statistical_tests(csv_path=args.csv, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
