# Guía de Contribución

Gracias por tu interés en mejorar **Optimización del Balanceo de Carcasa (OBC)**. Sigue estos pasos para colaborar de forma efectiva.

## 1. Requisitos previos

1. Clona este repositorio y crea una rama a partir de `main`.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Configura las variables de entorno descritas en `src/utils/config.py` si vas a ejecutar los ejemplos.

## 2. Estilo de código y commits

* Utiliza [Conventional Commits](https://www.conventionalcommits.org/es/) para los mensajes de commit.
  Ejemplo: `feat: agregar prueba de integración para SQLite`.
* Procura mantener el código formateado con herramientas como `black` y `flake8`.

## 3. Flujo de trabajo

1. Desarrolla tus cambios en ramas `feature/` o `fix/`.
2. Ejecuta `pytest` y asegúrate de que todas las pruebas pasen antes de abrir un Pull Request.
3. Describe de forma breve los cambios realizados y enlaza el Issue relacionado.

## 4. Revisión y fusión

Las propuestas se revisarán para verificar estilo, funcionalidad y documentación. Una vez aprobadas, se fusionarán en `main`.

## 5. Código de conducta

Se requiere mantener un trato respetuoso y profesional en todo momento. Cualquier comportamiento inapropiado podrá ser motivo de cierre del Issue o Pull Request.
