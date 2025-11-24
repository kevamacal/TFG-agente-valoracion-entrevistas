# Guía para Dockerizar la Base de Datos PostgreSQL

Este documento explica cómo levantar la base de datos PostgreSQL usando Docker y cómo ejecutar las migraciones.

## Prerrequisitos

- Docker y Docker Compose instalados.
- Python 3.x instalado.

## 1. Configuración de Variables de Entorno

Asegúrate de tener un archivo `.env` en la raíz del proyecto con las siguientes variables (ajusta las credenciales según prefieras):

```env
DB_NAME=mi_base_datos
DB_USER=usuario_postgres
DB_PASSWORD=mi_contrasena_segura
DB_HOST=localhost
DB_PORT=5433
```

> **Nota:** `DB_HOST` debe ser `localhost` para que el script de Python (ejecutándose en tu máquina) pueda conectar con el contenedor Docker.

## 2. Levantar la Base de Datos

Ejecuta el siguiente comando en la terminal para iniciar el contenedor de PostgreSQL en segundo plano:

```bash
docker-compose up -d
```

Para verificar que está corriendo:
```bash
docker ps
```

## 3. Instalar Dependencias de Python

Si aún no las tienes instaladas:

```bash
pip install -r requirements.txt
```

## 4. Ejecutar Migraciones

Una vez que la base de datos esté arriba, ejecuta el script de migración:

```bash
python migraciones_base_datos.py
```

Este script:
1. Conectará a la base de datos en Docker.
2. Creará la tabla `entrevistas` si no existe.
3. Leerá el dataset y poblará la base de datos.

## 5. Detener la Base de Datos

Cuando termines, puedes detener el contenedor con:

```bash
docker-compose down
```
