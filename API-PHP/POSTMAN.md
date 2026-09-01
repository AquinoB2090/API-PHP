# API PHP - Endpoints para Postman

Base URL de la API:

http://localhost:8080

## 1) Health check

### GET /health

- URL: http://localhost:8080/health
- Método: GET

Respuesta esperada:

```json
{
  "status": "ok"
}
```

---

## 2) Roles

### GET /roles

- URL: http://localhost:8080/roles
- Método: GET

### GET /roles/{id}

- URL: http://localhost:8080/roles/1
- Método: GET

### POST /roles

- URL: http://localhost:8080/roles
- Método: POST
- Body (raw JSON):

```json
{
  "nombre": "vendedor",
  "descripcion": "Encargado de ventas"
}
```

### PUT /roles/{id}

- URL: http://localhost:8080/roles/1
- Método: PUT
- Body (raw JSON):

```json
{
  "nombre": "superadmin",
  "descripcion": "Administrador con permisos completos"
}
```

### DELETE /roles/{id}

- URL: http://localhost:8080/roles/1
- Método: DELETE

---

## 3) Usuarios

### GET /usuarios

- URL: http://localhost:8080/usuarios
- Método: GET

### GET /usuarios/{id}

- URL: http://localhost:8080/usuarios/1
- Método: GET

### POST /usuarios

- URL: http://localhost:8080/usuarios
- Método: POST
- Body (raw JSON):

```json
{
  "rol_id": 2,
  "nombre": "Ana López",
  "email": "ana@test.com",
  "password": "123456"
}
```

### PUT /usuarios/{id}

- URL: http://localhost:8080/usuarios/1
- Método: PUT
- Body (raw JSON):

```json
{
  "rol_id": 2,
  "nombre": "Ana García",
  "email": "ana.nueva@test.com"
}
```

### DELETE /usuarios/{id}

- URL: http://localhost:8080/usuarios/1
- Método: DELETE

---

## 4) Categorías

### GET /categorias

- URL: http://localhost:8080/categorias
- Método: GET

### GET /categorias/{id}

- URL: http://localhost:8080/categorias/1
- Método: GET

### POST /categorias

- URL: http://localhost:8080/categorias
- Método: POST
- Body (raw JSON):

```json
{
  "nombre": "Electrónica",
  "descripcion": "Productos electrónicos"
}
```

### PUT /categorias/{id}

- URL: http://localhost:8080/categorias/1
- Método: PUT
- Body (raw JSON):

```json
{
  "nombre": "Tecnología",
  "descripcion": "Productos de tecnología"
}
```

### DELETE /categorias/{id}

- URL: http://localhost:8080/categorias/1
- Método: DELETE

---

## 5) Productos

### GET /productos

- URL: http://localhost:8080/productos
- Método: GET

### GET /productos/{id}

- URL: http://localhost:8080/productos/1
- Método: GET

### POST /productos

- URL: http://localhost:8080/productos
- Método: POST
- Body (raw JSON):

```json
{
  "categoria_id": 1,
  "nombre": "Laptop HP",
  "descripcion": "Laptop para oficina",
  "precio": 899.99,
  "stock": 10,
  "estado": "activo"
}
```

### PUT /productos/{id}

- URL: http://localhost:8080/productos/1
- Método: PUT
- Body (raw JSON):

```json
{
  "categoria_id": 1,
  "nombre": "Laptop Dell",
  "descripcion": "Laptop actualizada",
  "precio": 999.99,
  "stock": 8,
  "estado": "activo"
}
```

### DELETE /productos/{id}

- URL: http://localhost:8080/productos/1
- Método: DELETE

---

## 6) Pedidos

### GET /pedidos

- URL: http://localhost:8080/pedidos
- Método: GET

### GET /pedidos/{id}

- URL: http://localhost:8080/pedidos/1
- Método: GET

### POST /pedidos

- URL: http://localhost:8080/pedidos
- Método: POST
- Body (raw JSON):

```json
{
  "usuario_id": 1,
  "fecha": "2026-09-01 12:00:00",
  "estado": "pendiente",
  "total": 1500.0
}
```

### PUT /pedidos/{id}

- URL: http://localhost:8080/pedidos/1
- Método: PUT
- Body (raw JSON):

```json
{
  "usuario_id": 1,
  "estado": "confirmado",
  "total": 1800.0
}
```

### DELETE /pedidos/{id}

- URL: http://localhost:8080/pedidos/1
- Método: DELETE

---

## 7) Detalle de pedido

### GET /detalle-pedido

- URL: http://localhost:8080/detalle-pedido
- Método: GET

### GET /detalle-pedido/{id}

- URL: http://localhost:8080/detalle-pedido/1
- Método: GET

### POST /detalle-pedido

- URL: http://localhost:8080/detalle-pedido
- Método: POST
- Body (raw JSON):

```json
{
  "pedido_id": 1,
  "producto_id": 1,
  "cantidad": 2,
  "precio_unitario": 499.99
}
```

### PUT /detalle-pedido/{id}

- URL: http://localhost:8080/detalle-pedido/1
- Método: PUT
- Body (raw JSON):

```json
{
  "pedido_id": 1,
  "producto_id": 1,
  "cantidad": 3,
  "precio_unitario": 499.99
}
```

### DELETE /detalle-pedido/{id}

- URL: http://localhost:8080/detalle-pedido/1
- Método: DELETE

---

## Tips para Postman

- En la pestaña Body, seleccionar raw y JSON.
- Para GET, no hace falta enviar body.
- Para PUT/DELETE, usa la URL con el id.
- Si aparece error 404, revisa que la ruta exacta esté escrita igual.
- Si aparece 500, revisa que la base de datos esté levantada y la migración aplicada.

---

## Comandos para levantar la API

```powershell
cd "c:\Users\brand\OneDrive\Escritorio\API PHP"
docker compose up -d --build
```

Y luego probar en navegador o Postman:

```text
http://localhost:8080/health
```
