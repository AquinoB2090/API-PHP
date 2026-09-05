from functools import lru_cache
from pydantic import BaseModel
import os


class Settings(BaseModel):
    oracle_host: str = os.getenv("ORACLE_HOST", "52.171.58.51")
    oracle_port: int = int(os.getenv("ORACLE_PORT", "1521"))
    oracle_service_name: str = os.getenv("ORACLE_SERVICE_NAME", "FREEPDB1")
    oracle_user: str = os.getenv("ORACLE_USER", "DBA_COMPRAS")
    oracle_password: str = os.getenv("ORACLE_PASSWORD", "DBA_COMPRAS")
    oracle_pool_min: int = int(os.getenv("ORACLE_POOL_MIN", "0"))
    oracle_pool_max: int = int(os.getenv("ORACLE_POOL_MAX", "1"))
    oracle_pool_increment: int = int(os.getenv("ORACLE_POOL_INCREMENT", "1"))
    app_name: str = os.getenv("APP_NAME", "API Compras")


@lru_cache
def get_settings() -> Settings:
    return Settings()
