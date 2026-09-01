CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rol_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usuarios_roles FOREIGN KEY (rol_id) REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    estado TEXT NOT NULL DEFAULT 'activo',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_productos_categorias FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP,
    estado TEXT NOT NULL DEFAULT 'pendiente',
    total REAL NOT NULL DEFAULT 0,
    CONSTRAINT fk_pedidos_usuarios FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS detalle_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL DEFAULT 1,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    CONSTRAINT fk_detalle_pedido_pedido FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_pedido_producto FOREIGN KEY (producto_id) REFERENCES productos(id)
);

INSERT OR IGNORE INTO roles (nombre, descripcion) VALUES
('admin', 'Administrador del sistema'),
('cliente', 'Cliente de la tienda');

INSERT OR IGNORE INTO categorias (nombre, descripcion) VALUES
('Tecnologia', 'Productos tecnologicos'),
('Hogar', 'Productos para el hogar');

INSERT OR IGNORE INTO usuarios (rol_id, nombre, email, password)
SELECT id, 'Cliente Demo', 'cliente.demo@example.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2uheWG/igi.'
FROM roles
WHERE nombre = 'cliente';

INSERT INTO productos (categoria_id, nombre, descripcion, precio, stock, estado)
SELECT id, 'Laptop Demo', 'Producto de ejemplo para pruebas', 799.99, 10, 'activo'
FROM categorias
WHERE nombre = 'Tecnologia'
AND NOT EXISTS (
    SELECT 1
    FROM productos
    WHERE productos.nombre = 'Laptop Demo'
);

INSERT INTO pedidos (usuario_id, estado, total)
SELECT usuarios.id, 'pendiente', 799.99
FROM usuarios
WHERE usuarios.email = 'cliente.demo@example.com'
AND NOT EXISTS (
    SELECT 1
    FROM pedidos
    WHERE pedidos.usuario_id = usuarios.id
);

INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
SELECT pedidos.id, productos.id, 1, productos.precio, productos.precio
FROM pedidos
JOIN usuarios ON usuarios.id = pedidos.usuario_id
JOIN productos ON productos.nombre = 'Laptop Demo'
WHERE usuarios.email = 'cliente.demo@example.com'
AND NOT EXISTS (
    SELECT 1
    FROM detalle_pedido
    WHERE detalle_pedido.pedido_id = pedidos.id
    AND detalle_pedido.producto_id = productos.id
);
