from typing import Annotated

import oracledb
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import fetch_all, fetch_one

Limit = Annotated[int, Query(ge=1, le=100)]
Year = Annotated[int | None, Query(ge=1900, le=2100)]
Month = Annotated[int | None, Query(ge=1, le=12)]
Offset = Annotated[int, Query(ge=0, le=10000)]
Search = Annotated[str | None, Query(min_length=1, max_length=100)]

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


@app.get("/")
def root():
    return {
        "message": "API RESTful de compras conectada a Oracle",
        "endpoints": {
            "clientes": [
                "/api/clientes",
                "/api/clientes/{id_cliente}",
                "/api/clientes/top10",
                "/api/clientes/sin-compras",
                "/api/clientes/mayor-consumo",
            ],
            "marcas": ["/api/marcas", "/api/marcas/{id_marca}"],
            "tarjetas_crud": ["/api/tarjetas", "/api/tarjetas/{id_tarjeta}"],
            "categorias": ["/api/categorias", "/api/categorias/{id_categoria}"],
            "productos": [
                "/api/productos",
                "/api/productos/{id_producto}",
                "/api/productos/top10",
                "/api/productos/sin-ventas",
                "/api/productos/por-categoria",
            ],
            "compras": [
                "/api/compras",
                "/api/compras/{id_compra}",
                "/api/compras/por-mes",
                "/api/compras/por-anio",
                "/api/compras/promedio",
            ],
            "detalle_compras": [
                "/api/detalle-compras",
                "/api/detalle-compras/{id_detalle}",
            ],
            "tarjetas": [
                "/api/tarjetas/mas-utilizadas",
                "/api/tarjetas/credito-vs-debito",
                "/api/tarjetas/por-marca",
            ],
        },
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-check")
def db_check():
    result = fetch_one("select 'connected' as status, sysdate as checked_at from dual")
    return result or {"status": "unknown"}


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
    row = fetch_one(
        f"""
        select *
        from {metadata["table"]}
        where {metadata["id"]} = :row_id
        """,
        {"row_id": row_id},
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Registro no encontrado.")
    return row


@app.get("/api/clientes")
def clientes(limit: Limit = 50, offset: Offset = 0, q: Search = None):
    return list_table("clientes", limit, offset, q)


@app.get("/api/clientes/{id_cliente:int}")
def cliente_por_id(id_cliente: int):
    return get_table_row("clientes", id_cliente)


@app.get("/api/marcas")
def marcas(limit: Limit = 50, offset: Offset = 0, q: Search = None):
    return list_table("marcas", limit, offset, q)


@app.get("/api/marcas/{id_marca:int}")
def marca_por_id(id_marca: int):
    return get_table_row("marcas", id_marca)


@app.get("/api/tarjetas")
def tarjetas(limit: Limit = 50, offset: Offset = 0, q: Search = None):
    return list_table("tarjetas", limit, offset, q)


@app.get("/api/tarjetas/{id_tarjeta:int}")
def tarjeta_por_id(id_tarjeta: int):
    return get_table_row("tarjetas", id_tarjeta)


@app.get("/api/categorias")
def categorias(limit: Limit = 50, offset: Offset = 0, q: Search = None):
    return list_table("categorias", limit, offset, q)


@app.get("/api/categorias/{id_categoria:int}")
def categoria_por_id(id_categoria: int):
    return get_table_row("categorias", id_categoria)


@app.get("/api/productos")
def productos(limit: Limit = 50, offset: Offset = 0, q: Search = None):
    return list_table("productos", limit, offset, q)


@app.get("/api/productos/{id_producto:int}")
def producto_por_id(id_producto: int):
    return get_table_row("productos", id_producto)


@app.get("/api/compras")
def compras(limit: Limit = 50, offset: Offset = 0):
    return list_table("compras", limit, offset)


@app.get("/api/compras/{id_compra:int}")
def compra_por_id(id_compra: int):
    return get_table_row("compras", id_compra)


@app.get("/api/detalle-compras")
def detalle_compras(limit: Limit = 50, offset: Offset = 0):
    return list_table("detalle-compras", limit, offset)


@app.get("/api/detalle-compras/{id_detalle:int}")
def detalle_compra_por_id(id_detalle: int):
    return get_table_row("detalle-compras", id_detalle)


@app.get("/api/clientes/top10")
def clientes_top10(limit: Limit = 10):
    return fetch_all(
        """
        select *
        from (
            select
                c.id_cliente,
                c.carnet,
                trim(
                    c.primer_nombre || ' ' ||
                    nvl(c.segundo_nombre || ' ', '') ||
                    nvl(c.tercer_nombre || ' ', '') ||
                    c.primer_apellido || ' ' ||
                    nvl(c.segundo_apellido, '')
                ) as cliente,
                c.correo,
                count(e.id_compra) as total_compras,
                nvl(sum(e.total_compra), 0) as total_consumido
            from tbl_clientes c
            join tbl_enc_compras e on e.id_cliente = c.id_cliente
            group by
                c.id_cliente, c.carnet, c.primer_nombre, c.segundo_nombre,
                c.tercer_nombre, c.primer_apellido, c.segundo_apellido, c.correo
            order by total_consumido desc
        )
        where rownum <= :limit
        """,
        {"limit": limit},
    )


@app.get("/api/clientes/sin-compras")
def clientes_sin_compras(limit: Limit = 50):
    return fetch_all(
        """
        select *
        from (
            select
                c.id_cliente,
                c.carnet,
                trim(
                    c.primer_nombre || ' ' ||
                    nvl(c.segundo_nombre || ' ', '') ||
                    nvl(c.tercer_nombre || ' ', '') ||
                    c.primer_apellido || ' ' ||
                    nvl(c.segundo_apellido, '')
                ) as cliente,
                c.correo,
                c.telefono
            from tbl_clientes c
            where not exists (
                select 1
                from tbl_enc_compras e
                where e.id_cliente = c.id_cliente
            )
            order by c.primer_apellido, c.primer_nombre
        )
        where rownum <= :limit
        """,
        {"limit": limit},
    )


@app.get("/api/clientes/mayor-consumo")
def cliente_mayor_consumo():
    return fetch_all(
        """
        select *
        from (
            select
                c.id_cliente,
                c.carnet,
                trim(
                    c.primer_nombre || ' ' ||
                    nvl(c.segundo_nombre || ' ', '') ||
                    nvl(c.tercer_nombre || ' ', '') ||
                    c.primer_apellido || ' ' ||
                    nvl(c.segundo_apellido, '')
                ) as cliente,
                c.correo,
                count(e.id_compra) as total_compras,
                nvl(sum(e.total_compra), 0) as total_consumido
            from tbl_clientes c
            join tbl_enc_compras e on e.id_cliente = c.id_cliente
            group by
                c.id_cliente, c.carnet, c.primer_nombre, c.segundo_nombre,
                c.tercer_nombre, c.primer_apellido, c.segundo_apellido, c.correo
            order by total_consumido desc
        )
        where rownum = 1
        """
    )


@app.get("/api/productos/top10")
def productos_top10(limit: Limit = 10):
    return fetch_all(
        """
        select *
        from (
            select
                p.id_producto,
                p.nombre_producto,
                cat.nombre_categoria,
                sum(d.cantidad) as unidades_vendidas,
                sum(d.subtotal) as total_vendido
            from tbl_productos p
            join tbl_det_compras d on d.id_producto = p.id_producto
            join tbl_categorias cat on cat.id_categoria = p.id_categoria
            group by p.id_producto, p.nombre_producto, cat.nombre_categoria
            order by unidades_vendidas desc, total_vendido desc
        )
        where rownum <= :limit
        """,
        {"limit": limit},
    )


@app.get("/api/productos/sin-ventas")
def productos_sin_ventas(limit: Limit = 50):
    return fetch_all(
        """
        select *
        from (
            select
                p.id_producto,
                p.nombre_producto,
                p.precio_sugerido,
                cat.nombre_categoria
            from tbl_productos p
            join tbl_categorias cat on cat.id_categoria = p.id_categoria
            where not exists (
                select 1
                from tbl_det_compras d
                where d.id_producto = p.id_producto
            )
            order by cat.nombre_categoria, p.nombre_producto
        )
        where rownum <= :limit
        """,
        {"limit": limit},
    )


@app.get("/api/productos/por-categoria")
def productos_por_categoria():
    return fetch_all(
        """
        select
            cat.id_categoria,
            cat.nombre_categoria,
            count(p.id_producto) as total_productos,
            nvl(sum(d.cantidad), 0) as unidades_vendidas,
            nvl(sum(d.subtotal), 0) as total_vendido
        from tbl_categorias cat
        left join tbl_productos p on p.id_categoria = cat.id_categoria
        left join tbl_det_compras d on d.id_producto = p.id_producto
        group by cat.id_categoria, cat.nombre_categoria
        order by cat.nombre_categoria
        """
    )


@app.get("/api/compras/por-mes")
def compras_por_mes(anio: Year = None):
    where = "where extract(year from e.fecha_compra) = :anio" if anio else ""
    params = {"anio": anio} if anio else {}
    return fetch_all(
        f"""
        select
            extract(year from e.fecha_compra) as anio,
            extract(month from e.fecha_compra) as mes,
            count(*) as total_compras,
            sum(e.total_compra) as total_facturado
        from tbl_enc_compras e
        {where}
        group by extract(year from e.fecha_compra), extract(month from e.fecha_compra)
        order by anio, mes
        """,
        params,
    )


@app.get("/api/compras/por-anio")
def compras_por_anio():
    return fetch_all(
        """
        select
            extract(year from e.fecha_compra) as anio,
            count(*) as total_compras,
            sum(e.total_compra) as total_facturado
        from tbl_enc_compras e
        group by extract(year from e.fecha_compra)
        order by anio
        """
    )


@app.get("/api/compras/promedio")
def compras_promedio(anio: Year = None, mes: Month = None):
    if mes and not anio:
        raise HTTPException(
            status_code=422,
            detail="El parametro 'anio' es obligatorio cuando se envia 'mes'.",
        )

    filters = []
    params = {}
    if anio:
        filters.append("extract(year from e.fecha_compra) = :anio")
        params["anio"] = anio
    if mes:
        filters.append("extract(month from e.fecha_compra) = :mes")
        params["mes"] = mes

    where = f"where {' and '.join(filters)}" if filters else ""
    return fetch_all(
        f"""
        select
            count(*) as total_compras,
            nvl(avg(e.total_compra), 0) as promedio_compra,
            nvl(min(e.total_compra), 0) as compra_minima,
            nvl(max(e.total_compra), 0) as compra_maxima
        from tbl_enc_compras e
        {where}
        """,
        params,
    )


@app.get("/api/tarjetas/mas-utilizadas")
def tarjetas_mas_utilizadas(limit: Limit = 10):
    return fetch_all(
        """
        select *
        from (
            select
                t.id_tarjeta,
                t.tipo_tarjeta,
                m.nombre_marca,
                substr(t.numero_tarjeta, -4) as ultimos_digitos,
                count(e.id_compra) as veces_utilizada,
                sum(e.total_compra) as total_comprado
            from tbl_tarjetas t
            join tbl_marcas m on m.id_marca = t.id_marca
            join tbl_enc_compras e on e.id_tarjeta = t.id_tarjeta
            group by t.id_tarjeta, t.tipo_tarjeta, m.nombre_marca, substr(t.numero_tarjeta, -4)
            order by veces_utilizada desc, total_comprado desc
        )
        where rownum <= :limit
        """,
        {"limit": limit},
    )


@app.get("/api/tarjetas/credito-vs-debito")
def tarjetas_credito_vs_debito():
    return fetch_all(
        """
        select
            t.tipo_tarjeta,
            count(distinct t.id_tarjeta) as total_tarjetas,
            count(e.id_compra) as total_compras,
            nvl(sum(e.total_compra), 0) as total_comprado
        from tbl_tarjetas t
        left join tbl_enc_compras e on e.id_tarjeta = t.id_tarjeta
        group by t.tipo_tarjeta
        order by t.tipo_tarjeta
        """
    )


@app.get("/api/tarjetas/por-marca")
def tarjetas_por_marca():
    return fetch_all(
        """
        select
            m.id_marca,
            m.nombre_marca,
            count(distinct t.id_tarjeta) as total_tarjetas,
            count(e.id_compra) as total_compras,
            nvl(sum(e.total_compra), 0) as total_comprado
        from tbl_marcas m
        left join tbl_tarjetas t on t.id_marca = m.id_marca
        left join tbl_enc_compras e on e.id_tarjeta = t.id_tarjeta
        group by m.id_marca, m.nombre_marca
        order by m.nombre_marca
        """
    )
