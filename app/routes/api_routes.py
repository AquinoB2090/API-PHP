from fastapi import APIRouter

from app.controllers import health_controller, report_controller, table_controller
from app.types import Limit, Month, Offset, Search, Year

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "API RESTful de compras conectada a Oracle",
        "docs": "/docs",
        "endpoints": "/ENDPOINTS.md",
    }


@router.get("/health")
def health():
    return health_controller.health()


@router.get("/db-check")
def db_check():
    return health_controller.db_check()


@router.get("/api/clientes")
def clientes(limit: Limit = 50, offset: Offset = 0, q: Search = None):
    return table_controller.list_resource("clientes", limit, offset, q)


@router.get("/api/clientes/top10")
def clientes_top10(limit: Limit = 10):
    return report_controller.clientes_top10(limit)


@router.get("/api/clientes/sin-compras")
def clientes_sin_compras(limit: Limit = 50):
    return report_controller.clientes_sin_compras(limit)


@router.get("/api/clientes/mayor-consumo")
def cliente_mayor_consumo():
    return report_controller.cliente_mayor_consumo()


@router.get("/api/clientes/{id_cliente:int}")
def cliente_por_id(id_cliente: int):
    return table_controller.get_resource_by_id("clientes", id_cliente)


@router.get("/api/marcas")
def marcas(limit: Limit = 50, offset: Offset = 0, q: Search = None):
    return table_controller.list_resource("marcas", limit, offset, q)


@router.get("/api/marcas/{id_marca:int}")
def marca_por_id(id_marca: int):
    return table_controller.get_resource_by_id("marcas", id_marca)


@router.get("/api/tarjetas")
def tarjetas(limit: Limit = 50, offset: Offset = 0, q: Search = None):
    return table_controller.list_resource("tarjetas", limit, offset, q)


@router.get("/api/tarjetas/mas-utilizadas")
def tarjetas_mas_utilizadas(limit: Limit = 10):
    return report_controller.tarjetas_mas_utilizadas(limit)


@router.get("/api/tarjetas/credito-vs-debito")
def tarjetas_credito_vs_debito():
    return report_controller.tarjetas_credito_vs_debito()


@router.get("/api/tarjetas/por-marca")
def tarjetas_por_marca():
    return report_controller.tarjetas_por_marca()


@router.get("/api/tarjetas/{id_tarjeta:int}")
def tarjeta_por_id(id_tarjeta: int):
    return table_controller.get_resource_by_id("tarjetas", id_tarjeta)


@router.get("/api/categorias")
def categorias(limit: Limit = 50, offset: Offset = 0, q: Search = None):
    return table_controller.list_resource("categorias", limit, offset, q)


@router.get("/api/categorias/{id_categoria:int}")
def categoria_por_id(id_categoria: int):
    return table_controller.get_resource_by_id("categorias", id_categoria)


@router.get("/api/productos")
def productos(limit: Limit = 50, offset: Offset = 0, q: Search = None):
    return table_controller.list_resource("productos", limit, offset, q)


@router.get("/api/productos/top10")
def productos_top10(limit: Limit = 10):
    return report_controller.productos_top10(limit)


@router.get("/api/productos/sin-ventas")
def productos_sin_ventas(limit: Limit = 50):
    return report_controller.productos_sin_ventas(limit)


@router.get("/api/productos/por-categoria")
def productos_por_categoria():
    return report_controller.productos_por_categoria()


@router.get("/api/productos/{id_producto:int}")
def producto_por_id(id_producto: int):
    return table_controller.get_resource_by_id("productos", id_producto)


@router.get("/api/compras")
def compras(limit: Limit = 50, offset: Offset = 0):
    return table_controller.list_resource("compras", limit, offset)


@router.get("/api/compras/por-mes")
def compras_por_mes(anio: Year = None):
    return report_controller.compras_por_mes(anio)


@router.get("/api/compras/por-anio")
def compras_por_anio():
    return report_controller.compras_por_anio()


@router.get("/api/compras/promedio")
def compras_promedio(anio: Year = None, mes: Month = None):
    return report_controller.compras_promedio(anio, mes)


@router.get("/api/compras/{id_compra:int}")
def compra_por_id(id_compra: int):
    return table_controller.get_resource_by_id("compras", id_compra)


@router.get("/api/detalle-compras")
def detalle_compras(limit: Limit = 50, offset: Offset = 0):
    return table_controller.list_resource("detalle-compras", limit, offset)


@router.get("/api/detalle-compras/{id_detalle:int}")
def detalle_compra_por_id(id_detalle: int):
    return table_controller.get_resource_by_id("detalle-compras", id_detalle)
