from app.database import fetch_all, fetch_one

TABLES = {
    "clientes": {
        "table": "tbl_clientes",
        "id": "id_cliente",
        "order": "id_cliente",
        "search": [
            "carnet",
            "primer_nombre",
            "segundo_nombre",
            "tercer_nombre",
            "primer_apellido",
            "segundo_apellido",
            "correo",
            "telefono",
        ],
    },
    "marcas": {
        "table": "tbl_marcas",
        "id": "id_marca",
        "order": "id_marca",
        "search": ["nombre_marca"],
    },
    "tarjetas": {
        "table": "tbl_tarjetas",
        "id": "id_tarjeta",
        "order": "id_tarjeta",
        "search": ["numero_tarjeta", "tipo_tarjeta"],
    },
    "categorias": {
        "table": "tbl_categorias",
        "id": "id_categoria",
        "order": "id_categoria",
        "search": ["nombre_categoria"],
    },
    "productos": {
        "table": "tbl_productos",
        "id": "id_producto",
        "order": "id_producto",
        "search": ["nombre_producto"],
    },
    "compras": {
        "table": "tbl_enc_compras",
        "id": "id_compra",
        "order": "id_compra",
        "search": [],
    },
    "detalle-compras": {
        "table": "tbl_det_compras",
        "id": "id_detalle",
        "order": "id_detalle",
        "search": [],
    },
}


def list_table(resource: str, limit: int, offset: int, q: str | None = None):
    metadata = TABLES[resource]
    params = {"limit": limit, "offset": offset}
    where = ""

    if q and metadata["search"]:
        search_conditions = [
            f"lower({column}) like '%' || lower(:q) || '%'"
            for column in metadata["search"]
        ]
        where = f"where {' or '.join(search_conditions)}"
        params["q"] = q

    return fetch_all(
        f"""
        select *
        from {metadata["table"]}
        {where}
        order by {metadata["order"]}
        offset :offset rows fetch next :limit rows only
        """,
        params,
    )


def get_table_row(resource: str, row_id: int):
    metadata = TABLES[resource]
    return fetch_one(
        f"""
        select *
        from {metadata["table"]}
        where {metadata["id"]} = :row_id
        """,
        {"row_id": row_id},
    )
