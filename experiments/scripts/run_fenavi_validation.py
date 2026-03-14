"""
Validacion de datos sinteticos frente a referencias FENAVI.

Objetivo:
  - Verificar cobertura de precios sinteticos dentro de rangos FENAVI.
  - Cuantificar comportamiento de demanda sintetica (dispersion/estacionalidad).
  - Opcionalmente contrastar contra una serie historica mensual FENAVI.

Uso:
    python experiments/scripts/run_fenavi_validation.py
    python experiments/scripts/run_fenavi_validation.py --fenavi-csv data/references/fenavi_monthly_reference.csv

CSV opcional (historico FENAVI) esperado:
    product,month,value[,variable_type]
    pechuga,1,12345
    pechuga,2,12700
    ...
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, ".")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from src.instances.calibration import PRICE_RANGES_COP
from src.model.parameters import ProblemInstance

# ------------------------------------------------------------
# Config
# ------------------------------------------------------------

CUTFORM_TO_REF = {
    "pechuga": "pechuga",
    "pechuga entera": "pechuga",
    "filete pechuga": "filete_pechuga",
    "pernil completo": "pernil_completo",
    "muslo solo": "muslo",
    "muslo": "muslo",
    "contramuslo solo": "contramuslo",
    "contramuslo": "contramuslo",
    "ala": "ala",
    "ala entera": "ala",
    "menudencias": "menudencias",
    "subproducto": "subproducto_fresco",
    "subproducto fresco": "subproducto_fresco",
    "harina avicola": "harina_avicola",
    "medio pollo": "medio_pollo",
    "pollo en canal": "medio_pollo",
    "pollo encanal": "medio_pollo",
    "pollo_en_canal": "medio_pollo",
    "pollo_encanal": "medio_pollo",
}

PROFILE_ORDER = ["toy", "small", "medium", "large", "industrial"]


@dataclass
class ValidationOutputs:
    price_detail: pd.DataFrame
    price_summary: pd.DataFrame
    demand_summary: pd.DataFrame
    demand_seasonality: pd.DataFrame
    external_monthly: pd.DataFrame
    external_monthly_summary: pd.DataFrame
    summary_payload: dict


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def _normalize_name(text: str) -> str:
    t = text.strip().lower()
    t = (
        t.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
    )
    t = re.sub(r"\s+", " ", t)
    return t


def _map_cut_form(name: str) -> str | None:
    key = _normalize_name(name)
    return CUTFORM_TO_REF.get(key)


def _discover_instances(
    instances_dir: Path, profiles: list[str] | None = None
) -> list[Path]:
    files = sorted(instances_dir.glob("*_seed*.yaml"))
    if profiles:
        prefixes = tuple(f"{p}_" for p in profiles)
        files = [p for p in files if p.name.startswith(prefixes)]
    return files


def _instance_to_price_rows(inst: ProblemInstance, instance_path: Path) -> list[dict]:
    rows = []
    for f_idx, cf_name in enumerate(inst.cut_form_names):
        ref_key = _map_cut_form(cf_name)
        if ref_key is None or ref_key not in PRICE_RANGES_COP:
            continue

        ref = PRICE_RANGES_COP[ref_key]
        val = float(inst.prices[f_idx])
        in_range = ref["min"] <= val <= ref["max"]
        dist = 0.0
        if val < ref["min"]:
            dist = (ref["min"] - val) / max(ref["min"], 1e-9) * 100.0
        elif val > ref["max"]:
            dist = (val - ref["max"]) / max(ref["max"], 1e-9) * 100.0

        rows.append(
            {
                "instance": inst.name,
                "profile": inst.profile,
                "seed": inst.seed,
                "instance_path": str(instance_path),
                "cut_form_name": cf_name,
                "ref_product": ref_key,
                "synthetic_price": val,
                "fenavi_min": float(ref["min"]),
                "fenavi_max": float(ref["max"]),
                "fenavi_default": float(ref["default"]),
                "within_fenavi_range": bool(in_range),
                "outside_distance_pct": float(dist),
                "deviation_vs_default_pct": (val - float(ref["default"]))
                / max(float(ref["default"]), 1e-9)
                * 100.0,
            }
        )
    return rows


def _instance_to_demand_rows(inst: ProblemInstance) -> list[dict]:
    rows: list[dict] = []
    n_f, n_t, n_w = inst.demand.shape
    for f_idx in range(n_f):
        cf_name = (
            inst.cut_form_names[f_idx]
            if f_idx < len(inst.cut_form_names)
            else f"F{f_idx}"
        )
        ref_key = _map_cut_form(cf_name)
        if ref_key is None:
            continue

        for t in range(n_t):
            month = int(np.floor((t / n_t) * 12.0)) + 1
            for w in range(n_w):
                rows.append(
                    {
                        "instance": inst.name,
                        "profile": inst.profile,
                        "seed": inst.seed,
                        "cut_form_name": cf_name,
                        "ref_product": ref_key,
                        "period": t + 1,
                        "month": min(max(month, 1), 12),
                        "scenario": w + 1,
                        "demand": float(inst.demand[f_idx, t, w]),
                    }
                )
    return rows


def _build_price_summary(price_df: pd.DataFrame) -> pd.DataFrame:
    if price_df.empty:
        return pd.DataFrame()

    out = (
        price_df.groupby("ref_product", as_index=False)
        .agg(
            n_obs=("synthetic_price", "count"),
            synthetic_min=("synthetic_price", "min"),
            synthetic_max=("synthetic_price", "max"),
            synthetic_mean=("synthetic_price", "mean"),
            fenavi_min=("fenavi_min", "first"),
            fenavi_max=("fenavi_max", "first"),
            fenavi_default=("fenavi_default", "first"),
            within_range_pct=(
                "within_fenavi_range",
                lambda x: 100.0 * float(np.mean(x)),
            ),
            mean_abs_dev_default_pct=(
                "deviation_vs_default_pct",
                lambda x: float(np.mean(np.abs(x))),
            ),
            max_outside_distance_pct=("outside_distance_pct", "max"),
        )
        .sort_values("ref_product")
    )
    return out


def _build_demand_summary(demand_df: pd.DataFrame) -> pd.DataFrame:
    if demand_df.empty:
        return pd.DataFrame()

    # Muestreo controlado para estadisticos robustos sin cargar demasiado.
    sampled_parts = []
    for _, grp in demand_df.groupby("profile", observed=False):
        sampled_parts.append(grp.sample(min(len(grp), 20000), random_state=42))
    sample = pd.concat(sampled_parts, ignore_index=True)

    def _safe_skew(x: pd.Series) -> float:
        if len(x) < 3:
            return float("nan")
        return float(stats.skew(x, bias=False))

    out = sample.groupby("profile", as_index=False).agg(
        n_obs=("demand", "count"),
        demand_mean=("demand", "mean"),
        demand_std=("demand", "std"),
        demand_median=("demand", "median"),
        demand_p05=("demand", lambda x: float(np.quantile(x, 0.05))),
        demand_p95=("demand", lambda x: float(np.quantile(x, 0.95))),
        demand_skew=("demand", _safe_skew),
    )
    out["demand_cv"] = out["demand_std"] / np.maximum(out["demand_mean"], 1e-9)
    out["profile"] = pd.Categorical(
        out["profile"], categories=PROFILE_ORDER, ordered=True
    )
    out = out.sort_values("profile").reset_index(drop=True)
    return out


def _build_seasonality_summary(demand_df: pd.DataFrame) -> pd.DataFrame:
    if demand_df.empty:
        return pd.DataFrame()

    rows = []
    by_run = demand_df.groupby(
        ["instance", "profile", "ref_product", "period"], as_index=False
    )["demand"].mean()
    for (instance, profile, ref_product), sub in by_run.groupby(
        ["instance", "profile", "ref_product"]
    ):
        vals = sub.sort_values("period")["demand"].values
        mean_val = float(np.mean(vals))
        if mean_val <= 1e-9:
            strength = 0.0
        else:
            strength = float((np.max(vals) - np.min(vals)) / mean_val)
        peak_period = int(sub.loc[sub["demand"].idxmax(), "period"])
        rows.append(
            {
                "instance": instance,
                "profile": profile,
                "ref_product": ref_product,
                "seasonality_strength": strength,
                "peak_period": peak_period,
            }
        )

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out = (
        out.groupby(["profile", "ref_product"], as_index=False)
        .agg(
            n_series=("seasonality_strength", "count"),
            seasonality_strength_mean=("seasonality_strength", "mean"),
            seasonality_strength_p95=(
                "seasonality_strength",
                lambda x: float(np.quantile(x, 0.95)),
            ),
            peak_period_median=("peak_period", "median"),
        )
        .sort_values(["profile", "ref_product"])
    )
    return out


def _load_external_fenavi_monthly(
    path: Path, variable_type: str | None = None
) -> pd.DataFrame:
    df = pd.read_csv(path)
    cols = {c.lower(): c for c in df.columns}
    if "product" not in cols:
        raise ValueError("CSV FENAVI debe incluir columna 'product'")
    if "value" not in cols:
        raise ValueError("CSV FENAVI debe incluir columna 'value'")

    vt_col = cols.get("variable_type")
    if variable_type is not None and variable_type.strip() != "" and vt_col is not None:
        target = variable_type.strip().lower()
        df = df.loc[
            df[vt_col]
            .astype(str)
            .str.lower()
            .str.contains(target, regex=False, na=False)
        ].copy()

    product_col = cols["product"]
    value_col = cols["value"]

    if "month" in cols:
        month = pd.to_numeric(df[cols["month"]], errors="coerce")
    elif "date" in cols:
        parsed = pd.to_datetime(df[cols["date"]], errors="coerce")
        month = parsed.dt.month
    else:
        raise ValueError("CSV FENAVI debe incluir 'month' o 'date'")

    out = pd.DataFrame(
        {
            "ref_product": df[product_col].astype(str).map(_normalize_name),
            "month": month.astype("Int64"),
            "value": pd.to_numeric(df[value_col], errors="coerce"),
            "variable_type": (
                df[vt_col].astype(str).str.strip().str.lower()
                if vt_col is not None
                else "unspecified"
            ),
        }
    )
    out["ref_product"] = out["ref_product"].map(lambda x: CUTFORM_TO_REF.get(x, x))
    out = out.dropna(subset=["month", "value"])
    out["month"] = out["month"].astype(int)
    out = out[(out["month"] >= 1) & (out["month"] <= 12)]
    out["variable_type"] = out["variable_type"].replace("", "unspecified")

    return out


def _build_external_monthly_comparison(
    demand_df: pd.DataFrame,
    fenavi_df: pd.DataFrame,
) -> pd.DataFrame:
    if demand_df.empty or fenavi_df.empty:
        return pd.DataFrame()

    def _best_lagged_spearman(
        x: np.ndarray,
        y: np.ndarray,
        max_lag: int = 3,
    ) -> tuple[int | None, float, float, int]:
        best_lag: int | None = None
        best_rho = float("nan")
        best_p = float("nan")
        best_pairs = 0
        best_abs = -1.0

        for lag in range(-max_lag, max_lag + 1):
            if lag < 0:
                x_l = x[-lag:]
                y_l = y[: len(y) + lag]
            elif lag > 0:
                x_l = x[: len(x) - lag]
                y_l = y[lag:]
            else:
                x_l = x
                y_l = y

            if len(x_l) < 6 or len(y_l) < 6:
                continue

            rho_l, p_l = stats.spearmanr(x_l, y_l)
            if not np.isfinite(rho_l):
                continue
            if abs(float(rho_l)) > best_abs:
                best_abs = abs(float(rho_l))
                best_lag = lag
                best_rho = float(rho_l)
                best_p = float(p_l)
                best_pairs = int(len(x_l))

        return best_lag, best_rho, best_p, best_pairs

    syn_month = (
        demand_df.groupby(["ref_product", "month"], as_index=False)["demand"]
        .mean()
        .rename(columns={"demand": "synthetic_value"})
    )
    fen_month = (
        fenavi_df.groupby(["ref_product", "variable_type", "month"], as_index=False)[
            "value"
        ]
        .mean()
        .rename(columns={"value": "fenavi_value"})
    )

    rows = []
    common_products = sorted(
        set(syn_month["ref_product"]).intersection(set(fen_month["ref_product"]))
    )
    for product in common_products:
        s = syn_month[syn_month["ref_product"] == product][["month", "synthetic_value"]]
        fen_types = sorted(
            fen_month[fen_month["ref_product"] == product]["variable_type"].unique()
        )
        for var_type in fen_types:
            f = fen_month[
                (fen_month["ref_product"] == product)
                & (fen_month["variable_type"] == var_type)
            ][["month", "fenavi_value"]]
            merged = s.merge(f, on="month", how="inner")
            if len(merged) < 6:
                continue

            syn_idx = merged["synthetic_value"] / max(
                float(merged["synthetic_value"].mean()), 1e-9
            )
            fen_idx = merged["fenavi_value"] / max(float(merged["fenavi_value"].mean()), 1e-9)

            rho, pval = stats.spearmanr(syn_idx.values, fen_idx.values)
            if np.std(syn_idx.values) > 1e-12 and np.std(fen_idx.values) > 1e-12:
                pearson_r, pearson_p = stats.pearsonr(syn_idx.values, fen_idx.values)
            else:
                pearson_r, pearson_p = float("nan"), float("nan")
            rmse = float(np.sqrt(np.mean((syn_idx.values - fen_idx.values) ** 2)))
            ks_stat, ks_p = stats.ks_2samp(syn_idx.values, fen_idx.values)
            wd = float(stats.wasserstein_distance(syn_idx.values, fen_idx.values))
            best_lag, best_lag_rho, best_lag_p, best_lag_pairs = _best_lagged_spearman(
                syn_idx.values.astype(float),
                fen_idx.values.astype(float),
                max_lag=3,
            )
            syn_peak_month = int(merged.loc[syn_idx.idxmax(), "month"])
            fen_peak_month = int(merged.loc[fen_idx.idxmax(), "month"])

            rows.append(
                {
                    "ref_product": product,
                    "variable_type": var_type,
                    "comparison_mode": "seasonal_monthly_index",
                    "n_months": int(len(merged)),
                    "spearman_rho": float(rho),
                    "spearman_p_value": float(pval),
                    "pearson_r": float(pearson_r),
                    "pearson_p_value": float(pearson_p),
                    "best_lag_months": (int(best_lag) if best_lag is not None else np.nan),
                    "best_lag_spearman_rho": float(best_lag_rho),
                    "best_lag_spearman_p_value": float(best_lag_p),
                    "best_lag_pairs": int(best_lag_pairs),
                    "synthetic_peak_month": syn_peak_month,
                    "fenavi_peak_month": fen_peak_month,
                    "peak_month_shift_abs": int(abs(syn_peak_month - fen_peak_month)),
                    "rmse_index": rmse,
                    "ks_statistic": float(ks_stat),
                    "ks_p_value": float(ks_p),
                    "wasserstein_distance": wd,
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(["variable_type", "ref_product"]).reset_index(drop=True)


def _build_external_monthly_summary(external_df: pd.DataFrame) -> pd.DataFrame:
    if external_df.empty:
        return pd.DataFrame()

    out = (
        external_df.groupby("variable_type", as_index=False)
        .agg(
            n_products=("ref_product", "nunique"),
            n_series=("ref_product", "count"),
            spearman_rho_mean=("spearman_rho", "mean"),
            spearman_rho_abs_mean=(
                "spearman_rho",
                lambda x: float(np.mean(np.abs(x))),
            ),
            pearson_r_mean=("pearson_r", "mean"),
            pearson_r_abs_mean=(
                "pearson_r",
                lambda x: float(np.mean(np.abs(x))),
            ),
            best_lag_spearman_abs_mean=(
                "best_lag_spearman_rho",
                lambda x: float(np.mean(np.abs(x))),
            ),
            mean_peak_month_shift_abs=("peak_month_shift_abs", "mean"),
            mean_rmse_index=("rmse_index", "mean"),
            mean_ks_statistic=("ks_statistic", "mean"),
            mean_wasserstein_distance=("wasserstein_distance", "mean"),
        )
        .sort_values("variable_type")
    )
    return out.reset_index(drop=True)


def _plot_price_coverage(price_df: pd.DataFrame, out_path: Path) -> None:
    if price_df.empty:
        return

    products = sorted(price_df["ref_product"].unique())
    x_pos = np.arange(len(products))
    fig, ax = plt.subplots(figsize=(14, 6))

    for i, product in enumerate(products):
        sub = price_df[price_df["ref_product"] == product]
        y = sub["synthetic_price"].values
        x = np.full_like(y, i, dtype=float) + np.random.uniform(
            -0.10, 0.10, size=len(y)
        )
        ax.scatter(x, y, s=18, alpha=0.75, color="#1f77b4")

        fenavi_min = float(sub["fenavi_min"].iloc[0])
        fenavi_max = float(sub["fenavi_max"].iloc[0])
        fenavi_def = float(sub["fenavi_default"].iloc[0])
        ax.fill_between(
            [i - 0.25, i + 0.25], fenavi_min, fenavi_max, alpha=0.18, color="#ff7f0e"
        )
        ax.hlines(
            fenavi_def,
            i - 0.25,
            i + 0.25,
            colors="#d62728",
            linestyles="--",
            linewidth=1.5,
        )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(products, rotation=30, ha="right")
    ax.set_ylabel("Precio (COP/kg)")
    ax.set_title("Cobertura de precios sinteticos vs rangos FENAVI")
    ax.grid(alpha=0.25, linestyle="--")
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def _plot_demand_profiles(demand_df: pd.DataFrame, out_path: Path) -> None:
    if demand_df.empty:
        return

    agg = demand_df.groupby(["profile", "month"], as_index=False)["demand"].agg(
        mean="mean",
        p05=lambda x: float(np.quantile(x, 0.05)),
        p95=lambda x: float(np.quantile(x, 0.95)),
    )
    agg["profile"] = pd.Categorical(
        agg["profile"], categories=PROFILE_ORDER, ordered=True
    )
    agg = agg.sort_values(["profile", "month"])

    fig, ax = plt.subplots(figsize=(12, 6))
    for profile, sub in agg.groupby("profile", observed=False):
        if sub.empty:
            continue
        ax.plot(sub["month"], sub["mean"], marker="o", linewidth=2, label=str(profile))
        ax.fill_between(sub["month"], sub["p05"], sub["p95"], alpha=0.12)

    ax.set_xticks(range(1, 13))
    ax.set_xlabel("Mes")
    ax.set_ylabel("Demanda media sintetica")
    ax.set_title("Perfil mensual sintetico (bandas P5-P95)")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend(title="Perfil")
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def _plot_external_monthly_comparison(
    demand_df: pd.DataFrame,
    fenavi_df: pd.DataFrame,
    out_path: Path,
) -> None:
    if demand_df.empty or fenavi_df.empty:
        return

    syn_month = (
        demand_df.groupby(["ref_product", "month"], as_index=False)["demand"]
        .mean()
        .rename(columns={"demand": "synthetic_value"})
    )
    fen_month = (
        fenavi_df.groupby(["ref_product", "variable_type", "month"], as_index=False)[
            "value"
        ]
        .mean()
        .rename(columns={"value": "fenavi_value"})
    )
    merged = syn_month.merge(fen_month, on=["ref_product", "month"], how="inner")
    if merged.empty:
        return

    merged["series_id"] = merged["ref_product"] + " | " + merged["variable_type"]
    series_ids = sorted(merged["series_id"].unique())[:6]
    n = len(series_ids)
    cols = 3
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(15, 4.5 * rows), sharex=True)
    axes_arr = np.array(axes).reshape(-1)

    for idx, series_id in enumerate(series_ids):
        ax = axes_arr[idx]
        sub = merged[merged["series_id"] == series_id].sort_values("month")
        s_idx = sub["synthetic_value"] / max(float(sub["synthetic_value"].mean()), 1e-9)
        f_idx = sub["fenavi_value"] / max(float(sub["fenavi_value"].mean()), 1e-9)
        ax.plot(sub["month"], s_idx, marker="o", label="Sintetico")
        ax.plot(sub["month"], f_idx, marker="s", label="FENAVI")
        ax.set_title(series_id)
        ax.grid(alpha=0.25, linestyle="--")
        ax.set_xticks(range(1, 13))
        if idx % cols == 0:
            ax.set_ylabel("Indice (media=1)")

    for j in range(n, len(axes_arr)):
        axes_arr[j].set_axis_off()

    handles, labels = axes_arr[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2)
    fig.suptitle("Comparacion mensual normalizada: sintetico vs FENAVI", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


def _write_report(
    output_dir: Path,
    outputs: ValidationOutputs,
    fenavi_csv: Path | None,
) -> None:
    report_path = output_dir / "fenavi_validation_report.md"

    lines = [
        "# Validacion Sintetico vs FENAVI",
        "",
        "## Resumen",
        "",
        f"- Instancias analizadas: **{outputs.summary_payload.get('n_instances', 0)}**",
        f"- Observaciones de precio evaluadas: **{outputs.summary_payload.get('n_price_obs', 0)}**",
        f"- Cobertura global de precios en rango FENAVI: **{outputs.summary_payload.get('price_within_range_pct', 0.0):.2f}%**",
        "",
        "## Archivos generados",
        "",
        "- `fenavi_price_validation.csv`",
        "- `fenavi_price_summary.csv`",
        "- `fenavi_demand_summary.csv`",
        "- `fenavi_demand_seasonality.csv`",
        "- `fenavi_validation_summary.json`",
        "- `price_range_coverage.png`",
        "- `synthetic_demand_monthly_profile.png`",
    ]

    if fenavi_csv is not None:
        lines.extend(
            [
                "- `fenavi_external_monthly_comparison.csv`",
                "- `fenavi_external_monthly_summary.csv`",
                "- `fenavi_external_monthly_comparison.png`",
            ]
        )

    lines.extend(
        [
            "",
            "## Lectura rapida",
            "",
            "- La validacion de precios se basa en rangos FENAVI documentados en `src/instances/calibration.py`.",
            "- La validacion de demanda sintetica reporta dispersion y fuerza estacional por perfil/producto.",
        ]
    )

    if fenavi_csv is None:
        lines.extend(
            [
                "- No se suministro serie mensual historica FENAVI, por lo que no se ejecuto comparacion temporal externa.",
                "",
                "Para activar comparacion externa:",
                "`python experiments/scripts/run_fenavi_validation.py --fenavi-csv data/references/fenavi_monthly_reference.csv`",
            ]
        )
    else:
        lines.extend(
            [
                "- Se ejecuto comparacion externa mensual por `variable_type` con Spearman/Pearson, desfase optimo (lag), KS y Wasserstein.",
            ]
        )

        ext_types = outputs.summary_payload.get("external_variable_types", [])
        if ext_types:
            lines.append(
                f"- Tipos de variable externos analizados: **{', '.join(ext_types)}**."
            )

        rho_abs = outputs.summary_payload.get("external_spearman_rho_abs_mean")
        lag_abs = outputs.summary_payload.get("external_best_lag_spearman_abs_mean")
        if rho_abs is not None:
            lines.append(
                f"- Correlacion Spearman absoluta media: **{float(rho_abs):.3f}**."
            )
        if lag_abs is not None:
            lines.append(
                f"- Correlacion Spearman absoluta media con lag optimo: **{float(lag_abs):.3f}**."
            )

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def run_validation(
    instances_dir: str = "data/instances",
    output_dir: str = "experiments/results/fenavi_validation",
    fenavi_csv: str | None = None,
    fenavi_variable_type: str | None = None,
    profiles: list[str] | None = None,
) -> ValidationOutputs:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    paths = _discover_instances(Path(instances_dir), profiles)
    if not paths:
        raise FileNotFoundError(f"No se encontraron instancias YAML en {instances_dir}")

    price_rows: list[dict] = []
    demand_rows: list[dict] = []
    for p in paths:
        inst = ProblemInstance.from_yaml(p)
        price_rows.extend(_instance_to_price_rows(inst, p))
        demand_rows.extend(_instance_to_demand_rows(inst))

    price_df = pd.DataFrame(price_rows)
    demand_df = pd.DataFrame(demand_rows)

    price_summary = _build_price_summary(price_df)
    demand_summary = _build_demand_summary(demand_df)
    seasonality = _build_seasonality_summary(demand_df)

    external_monthly = pd.DataFrame()
    external_monthly_summary = pd.DataFrame()
    fenavi_path = Path(fenavi_csv) if fenavi_csv else None
    if fenavi_path is not None and fenavi_path.exists():
        fenavi_df = _load_external_fenavi_monthly(
            fenavi_path, variable_type=fenavi_variable_type
        )
        external_monthly = _build_external_monthly_comparison(demand_df, fenavi_df)
        external_monthly_summary = _build_external_monthly_summary(external_monthly)
        _plot_external_monthly_comparison(
            demand_df=demand_df,
            fenavi_df=fenavi_df,
            out_path=out_dir / "fenavi_external_monthly_comparison.png",
        )
        external_monthly.to_csv(
            out_dir / "fenavi_external_monthly_comparison.csv", index=False
        )
        external_monthly_summary.to_csv(
            out_dir / "fenavi_external_monthly_summary.csv", index=False
        )
    else:
        for stale in [
            out_dir / "fenavi_external_monthly_comparison.csv",
            out_dir / "fenavi_external_monthly_summary.csv",
            out_dir / "fenavi_external_monthly_comparison.png",
        ]:
            if stale.exists():
                stale.unlink()

    price_df.to_csv(out_dir / "fenavi_price_validation.csv", index=False)
    price_summary.to_csv(out_dir / "fenavi_price_summary.csv", index=False)
    demand_summary.to_csv(out_dir / "fenavi_demand_summary.csv", index=False)
    seasonality.to_csv(out_dir / "fenavi_demand_seasonality.csv", index=False)

    _plot_price_coverage(price_df, out_dir / "price_range_coverage.png")
    _plot_demand_profiles(demand_df, out_dir / "synthetic_demand_monthly_profile.png")

    summary_payload = {
        "n_instances": int(len(paths)),
        "n_price_obs": int(len(price_df)),
        "n_demand_obs": int(len(demand_df)),
        "price_within_range_pct": (
            float(price_df["within_fenavi_range"].mean() * 100.0)
            if not price_df.empty
            else float("nan")
        ),
        "profiles": sorted({ProblemInstance.from_yaml(p).profile for p in paths}),
        "fenavi_csv_used": str(fenavi_path) if fenavi_path is not None else None,
        "fenavi_variable_type": fenavi_variable_type,
        "external_comparison_products": (
            int(external_monthly["ref_product"].nunique())
            if not external_monthly.empty
            else 0
        ),
        "external_comparison_series": int(len(external_monthly)),
        "external_variable_types": (
            sorted(external_monthly["variable_type"].dropna().unique().tolist())
            if not external_monthly.empty and "variable_type" in external_monthly.columns
            else []
        ),
        "external_spearman_rho_abs_mean": (
            float(external_monthly["spearman_rho"].abs().mean())
            if not external_monthly.empty and "spearman_rho" in external_monthly.columns
            else None
        ),
        "external_best_lag_spearman_abs_mean": (
            float(external_monthly["best_lag_spearman_rho"].abs().mean())
            if not external_monthly.empty
            and "best_lag_spearman_rho" in external_monthly.columns
            else None
        ),
        "external_peak_month_shift_abs_mean": (
            float(external_monthly["peak_month_shift_abs"].mean())
            if not external_monthly.empty and "peak_month_shift_abs" in external_monthly.columns
            else None
        ),
    }

    with open(out_dir / "fenavi_validation_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2, ensure_ascii=False)

    outputs = ValidationOutputs(
        price_detail=price_df,
        price_summary=price_summary,
        demand_summary=demand_summary,
        demand_seasonality=seasonality,
        external_monthly=external_monthly,
        external_monthly_summary=external_monthly_summary,
        summary_payload=summary_payload,
    )
    _write_report(
        out_dir, outputs, fenavi_path if fenavi_path and fenavi_path.exists() else None
    )
    return outputs


def _parse_profiles(raw: str | None) -> list[str] | None:
    if raw is None or raw.strip() == "":
        return None
    vals = [_normalize_name(v) for v in raw.split(",") if v.strip()]
    return vals or None


def main() -> None:
    parser = argparse.ArgumentParser(description="Validacion sintetico vs FENAVI")
    parser.add_argument(
        "--instances-dir",
        type=str,
        default="data/instances",
        help="Directorio con instancias YAML",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="experiments/results/fenavi_validation",
        help="Directorio de salida",
    )
    parser.add_argument(
        "--fenavi-csv",
        type=str,
        default=None,
        help="CSV mensual historico FENAVI (columnas: product,month,value[,variable_type])",
    )
    parser.add_argument(
        "--fenavi-variable-type",
        type=str,
        default=None,
        help=(
            "Filtro opcional por variable_type en CSV FENAVI "
            "(ej: price_cop_per_kg, production_tons)"
        ),
    )
    parser.add_argument(
        "--profiles",
        type=str,
        default=None,
        help="Perfiles a incluir separados por coma (ej: small,medium,large)",
    )
    args = parser.parse_args()

    outputs = run_validation(
        instances_dir=args.instances_dir,
        output_dir=args.output_dir,
        fenavi_csv=args.fenavi_csv,
        fenavi_variable_type=args.fenavi_variable_type,
        profiles=_parse_profiles(args.profiles),
    )

    print("=" * 80)
    print("VALIDACION SINTETICO VS FENAVI COMPLETADA")
    print("=" * 80)
    print(f"Instancias: {outputs.summary_payload['n_instances']}")
    print(
        f"Precio dentro de rango FENAVI: {outputs.summary_payload['price_within_range_pct']:.2f}%"
    )
    print(f"Output: {Path(args.output_dir)}")
    if args.fenavi_csv:
        print(
            f"Comparacion externa productos: {outputs.summary_payload['external_comparison_products']}"
        )
        print(
            f"Comparacion externa series: {outputs.summary_payload.get('external_comparison_series', 0)}"
        )


if __name__ == "__main__":
    main()
