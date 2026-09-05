from app.database import fetch_all


def clientes_top10(limit: int):
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


def clientes_sin_compras(limit: int):
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


def productos_top10(limit: int):
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


def productos_sin_ventas(limit: int):
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


def compras_por_mes(anio: int | None):
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


def compras_promedio(anio: int | None, mes: int | None):
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


def tarjetas_mas_utilizadas(limit: int):
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
