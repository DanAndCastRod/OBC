# Optimización del Balanceo de Carcasa (OBC)

Este repositorio centraliza la investigación y los prototipos de código para abordar el problema de **balanceo de carcasa** en la industria avícola. El objetivo es ajustar la oferta de cortes de pollo a la demanda real del mercado, minimizando costos y aprovechando al máximo cada ave procesada.

## Contenido principal

- Documentos en formato Markdown que describen el problema, la metodología de investigación y las guías de implementación.
- Código en `src/` para gestionar referencias bibliográficas: incluye un extractor de la API de Elsevier, un cliente para MyLoft y un módulo de base de datos SQLite.
- Pruebas automáticas en `test/` que verifican la inserción de artículos en la base de datos.

## Uso rápido

1. Instalar las dependencias listadas en `requirements.txt` (se requiere acceso a internet).
2. Definir las variables de entorno indicadas en `src/utils/config.py` para configurar las claves de API y la ruta de la base de datos.
3. Ejecutar `pytest` para correr las pruebas de integración.

Este proyecto sirve como punto de partida para desarrollar modelos de optimización que logren un balance productivo y comercial sostenible.

