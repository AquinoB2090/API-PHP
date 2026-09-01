<?php

require __DIR__ . '/config/database.php';
require __DIR__ . '/models/Rol.php';
require __DIR__ . '/models/Usuario.php';
require __DIR__ . '/models/Categoria.php';
require __DIR__ . '/models/Producto.php';
require __DIR__ . '/models/Pedido.php';
require __DIR__ . '/models/DetallePedido.php';
require __DIR__ . '/controllers/BaseController.php';
require __DIR__ . '/controllers/HomeController.php';
require __DIR__ . '/controllers/RolController.php';
require __DIR__ . '/controllers/UsuarioController.php';
require __DIR__ . '/controllers/CategoriaController.php';
require __DIR__ . '/controllers/ProductoController.php';
require __DIR__ . '/controllers/PedidoController.php';
require __DIR__ . '/controllers/DetallePedidoController.php';
require __DIR__ . '/routes/routes.php';
