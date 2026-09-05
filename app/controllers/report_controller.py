from fastapi import HTTPException

from app.models import report_model


def clientes_top10(limit: int):
    return report_model.clientes_top10(limit)


def clientes_sin_compras(limit: int):
    return report_model.clientes_sin_compras(limit)


def cliente_mayor_consumo():
    return report_model.cliente_mayor_consumo()


def productos_top10(limit: int):
    return report_model.productos_top10(limit)


def productos_sin_ventas(limit: int):
    return report_model.productos_sin_ventas(limit)


def productos_por_categoria():
    return report_model.productos_por_categoria()


def compras_por_mes(anio: int | None):
    return report_model.compras_por_mes(anio)


def compras_por_anio():
    return report_model.compras_por_anio()


def compras_promedio(anio: int | None, mes: int | None):
    if mes and not anio:
        raise HTTPException(
            status_code=422,
            detail="El parametro 'anio' es obligatorio cuando se envia 'mes'.",
        )
    return report_model.compras_promedio(anio, mes)


def tarjetas_mas_utilizadas(limit: int):
    return report_model.tarjetas_mas_utilizadas(limit)


def tarjetas_credito_vs_debito():
    return report_model.tarjetas_credito_vs_debito()


def tarjetas_por_marca():
    return report_model.tarjetas_por_marca()
