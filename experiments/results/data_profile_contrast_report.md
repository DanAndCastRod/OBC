# Contraste Stable vs Seasonal

## Configuracion

- Nombre: `data_profile_contrast_v1`
- Size profiles: `['small', 'medium']`
- Demand profiles: `['stable', 'seasonal']`
- Instance seeds: `[42]`
- Run seeds (n_replicas): `5`

## Totales

- Filas en runs CSV: **104**
- Algoritmos: **6**

## Resumen por perfil y algoritmo

- `seasonal` / `baseline`: n=10, Z_mean=629,129,833, service_mean=64.63%, feasible=100.0%
- `seasonal` / `cbc_exact`: n=2, Z_mean=650,239,223, service_mean=64.40%, feasible=100.0%
- `seasonal` / `de`: n=10, Z_mean=629,128,286, service_mean=64.63%, feasible=100.0%
- `seasonal` / `ga`: n=10, Z_mean=629,129,833, service_mean=64.63%, feasible=100.0%
- `seasonal` / `ga_sa`: n=10, Z_mean=629,129,833, service_mean=64.63%, feasible=100.0%
- `seasonal` / `sa`: n=10, Z_mean=581,234,906, service_mean=62.13%, feasible=100.0%
- `stable` / `baseline`: n=10, Z_mean=551,944,642, service_mean=56.48%, feasible=100.0%
- `stable` / `cbc_exact`: n=2, Z_mean=571,399,847, service_mean=56.24%, feasible=100.0%
- `stable` / `de`: n=10, Z_mean=551,939,217, service_mean=56.48%, feasible=100.0%
- `stable` / `ga`: n=10, Z_mean=551,944,642, service_mean=56.48%, feasible=100.0%
- `stable` / `ga_sa`: n=10, Z_mean=551,944,642, service_mean=56.48%, feasible=100.0%
- `stable` / `sa`: n=10, Z_mean=504,292,762, service_mean=54.41%, feasible=100.0%

## Delta seasonal vs stable

- `baseline` / `medium`: delta Z mean=14.08%, delta service=8.17 pp, delta low-rotation=-100.00%
- `baseline` / `small`: delta Z mean=13.89%, delta service=8.13 pp, delta low-rotation=-100.00%
- `cbc_exact` / `medium`: delta Z mean=13.87%, delta service=8.19 pp, delta low-rotation=-100.00%
- `cbc_exact` / `small`: delta Z mean=13.72%, delta service=8.14 pp, delta low-rotation=-100.00%
- `de` / `medium`: delta Z mean=14.08%, delta service=8.17 pp, delta low-rotation=-100.00%
- `de` / `small`: delta Z mean=13.89%, delta service=8.13 pp, delta low-rotation=-100.00%
- `ga` / `medium`: delta Z mean=14.08%, delta service=8.17 pp, delta low-rotation=-100.00%
- `ga` / `small`: delta Z mean=13.89%, delta service=8.13 pp, delta low-rotation=-100.00%
- `ga_sa` / `medium`: delta Z mean=14.08%, delta service=8.17 pp, delta low-rotation=-100.00%
- `ga_sa` / `small`: delta Z mean=13.89%, delta service=8.13 pp, delta low-rotation=-100.00%
- `sa` / `medium`: delta Z mean=15.11%, delta service=7.66 pp, delta low-rotation=-100.00%
- `sa` / `small`: delta Z mean=15.74%, delta service=7.78 pp, delta low-rotation=-100.00%

## Hipotesis por perfil

- `seasonal`: H1 soportadas=0, H2 soportadas=1, H3 soportadas=0
- `stable`: H1 soportadas=0, H2 soportadas=1, H3 soportadas=0