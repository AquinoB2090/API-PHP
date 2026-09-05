from fastapi import HTTPException

from app.models.table_model import get_table_row, list_table


def list_resource(resource: str, limit: int, offset: int, q: str | None = None):
    return list_table(resource, limit, offset, q)


def get_resource_by_id(resource: str, row_id: int):
    row = get_table_row(resource, row_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado.")
    return row
