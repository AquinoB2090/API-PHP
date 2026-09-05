from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from datetime import date, datetime
from decimal import Decimal
from typing import Any

import oracledb

from app.config import get_settings

_pool: oracledb.ConnectionPool | None = None


def make_dsn() -> str:
    settings = get_settings()
    return oracledb.makedsn(
        settings.oracle_host,
        settings.oracle_port,
        service_name=settings.oracle_service_name,
    )


def get_pool() -> oracledb.ConnectionPool:
    global _pool
    if _pool is None:
        settings = get_settings()
        _pool = oracledb.create_pool(
            user=settings.oracle_user,
            password=settings.oracle_password,
            dsn=make_dsn(),
            min=settings.oracle_pool_min,
            max=settings.oracle_pool_max,
            increment=settings.oracle_pool_increment,
        )
    return _pool


@contextmanager
def get_connection() -> Iterator[oracledb.Connection]:
    connection = get_pool().acquire()
    try:
        yield connection
    finally:
        get_pool().release(connection)


def json_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def rows_to_dicts(cursor: oracledb.Cursor) -> list[dict[str, Any]]:
    columns = [column[0].lower() for column in cursor.description or []]
    return [
        {column: json_value(value) for column, value in zip(columns, row)}
        for row in cursor.fetchall()
    ]


def fetch_all(sql: str, params: Mapping[str, Any] | None = None) -> list[dict[str, Any]]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params or {})
            return rows_to_dicts(cursor)


def fetch_one(sql: str, params: Mapping[str, Any] | None = None) -> dict[str, Any] | None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params or {})
            columns = [column[0].lower() for column in cursor.description or []]
            row = cursor.fetchone()
            if row is None:
                return None
            return {column: json_value(value) for column, value in zip(columns, row)}
