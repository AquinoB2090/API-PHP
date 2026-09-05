# API Compras Python

API RESTful en Python/FastAPI conectada a Oracle.

## Requisitos

- Python 3.11+
- Dependencias de `requirements.txt`
- Acceso al servidor Oracle `52.171.58.51:1521/FREEPDB1`

## Variables de entorno

La app usa estos valores por defecto, pero en Azure App Service conviene configurarlos como App Settings:

```bash
ORACLE_HOST=52.171.58.51
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=FREEPDB1
ORACLE_USER=DBA_COMPRAS
ORACLE_PASSWORD=DBA_COMPRAS
```

## Ejecutar localmente

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger/OpenAPI queda disponible en:

```text
http://localhost:8000/docs
```

## Endpoints

El catalogo completo esta en `ENDPOINTS.md`.

- `GET /api/clientes/top10?limit=10`
- `GET /api/clientes/sin-compras?limit=50`
- `GET /api/clientes/mayor-consumo`
- `GET /api/productos/top10?limit=10`
- `GET /api/productos/sin-ventas?limit=50`
- `GET /api/productos/por-categoria`
- `GET /api/compras/por-mes?anio=2026`
- `GET /api/compras/por-anio`
- `GET /api/compras/promedio?anio=2026&mes=9`
- `GET /api/tarjetas/mas-utilizadas?limit=10`
- `GET /api/tarjetas/credito-vs-debito`
- `GET /api/tarjetas/por-marca`

## Azure App Service

Configura estas variables en `Settings > Environment variables`:

```bash
ORACLE_HOST=52.171.58.51
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=FREEPDB1
ORACLE_USER=DBA_COMPRAS
ORACLE_PASSWORD=DBA_COMPRAS
ORACLE_POOL_MIN=0
ORACLE_POOL_MAX=1
ORACLE_POOL_INCREMENT=1
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

Startup command sugerido en `Settings > Configuration > General settings`:

```bash
python -m gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

Tambien puedes usar el script si Azure lo reconoce correctamente:

```bash
startup.sh
```
