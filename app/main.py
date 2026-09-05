import oracledb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.routes.api_routes import router

app = FastAPI(title=get_settings().app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.exception_handler(oracledb.Error)
async def oracle_error_handler(_request, exc: oracledb.Error):
    return JSONResponse(
        status_code=503,
        content={"detail": f"Error de Oracle: {exc}"},
    )


app.include_router(router)
