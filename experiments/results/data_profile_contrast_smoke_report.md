# Contraste Stable vs Seasonal

## Configuracion

- Nombre: `data_profile_contrast_smoke`
- Size profiles: `['small']`
- Demand profiles: `['stable', 'seasonal']`
- Instance seeds: `[42]`
- Run seeds (n_replicas): `2`

## Totales

- Filas en runs CSV: **10**
- Algoritmos: **3**

## Resumen por perfil y algoritmo

- `seasonal` / `baseline`: n=2, Z_mean=628,998,736, service_mean=64.61%, feasible=100.0%
- `seasonal` / `cbc_exact`: n=1, Z_mean=649,963,169, service_mean=64.31%, feasible=100.0%
- `seasonal` / `ga_sa`: n=2, Z_mean=584,110,236, service_mean=62.29%, feasible=100.0%
- `stable` / `baseline`: n=2, Z_mean=552,277,687, service_mean=56.48%, feasible=100.0%
- `stable` / `cbc_exact`: n=1, Z_mean=571,535,747, service_mean=56.17%, feasible=100.0%
- `stable` / `ga_sa`: n=2, Z_mean=491,316,104, service_mean=53.86%, feasible=100.0%

## Delta seasonal vs stable

- `baseline` / `small`: delta Z mean=13.89%, delta service=8.13 pp, delta low-rotation=-100.00%
- `cbc_exact` / `small`: delta Z mean=13.72%, delta service=8.14 pp, delta low-rotation=-100.00%
- `ga_sa` / `small`: delta Z mean=18.82%, delta service=8.44 pp, delta low-rotation=-100.00%

## Hipotesis por perfil

- `seasonal`: H1 soportadas=0, H2 soportadas=0, H3 soportadas=0
- `stable`: H1 soportadas=0, H2 soportadas=0, H3 soportadas=0