<?php

$uri = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$scriptName = dirname($_SERVER['SCRIPT_NAME']);

if ($scriptName !== '/' && strpos($uri, $scriptName) === 0) {
    $uri = substr($uri, strlen($scriptName));
    if ($uri === '') {
        $uri = '/';
    }
}

$routes = [
    '/' => ['controller' => HomeController::class, 'action' => 'index'],
    '/health' => ['controller' => null, 'action' => null, 'handler' => function () {
        http_response_code(200);
        echo json_encode(['status' => 'ok']);
    }],
    '/roles' => ['controller' => RolController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/roles/' => ['controller' => RolController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/usuarios' => ['controller' => UsuarioController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/usuarios/' => ['controller' => UsuarioController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/categorias' => ['controller' => CategoriaController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/categorias/' => ['controller' => CategoriaController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/productos' => ['controller' => ProductoController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/productos/' => ['controller' => ProductoController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/pedidos' => ['controller' => PedidoController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/pedidos/' => ['controller' => PedidoController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/detalle-pedido' => ['controller' => DetallePedidoController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
    '/detalle-pedido/' => ['controller' => DetallePedidoController::class, 'action' => 'index', 'methods' => ['GET', 'POST']],
];

foreach ($routes as $pattern => $route) {
    if ($pattern === $uri) {
        if (isset($route['handler'])) {
            $route['handler']();
            return;
        }

        if (isset($route['methods']) && !in_array($method, $route['methods'], true)) {
            http_response_code(405);
            echo json_encode(['error' => 'Method not allowed']);
            return;
        }

        $controller = new $route['controller']();

        if ($method === 'POST' && method_exists($controller, 'store')) {
            $controller->store();
            return;
        }

        $controller->{$route['action']}();
        return;
    }
}

$match = preg_match('#^/(roles|usuarios|categorias|productos|pedidos|detalle-pedido)/([0-9]+)$#', $uri, $matches);
if ($match === 1) {
    $resource = $matches[1];
    $id = (int) $matches[2];

    $map = [
        'roles' => RolController::class,
        'usuarios' => UsuarioController::class,
        'categorias' => CategoriaController::class,
        'productos' => ProductoController::class,
        'pedidos' => PedidoController::class,
        'detalle-pedido' => DetallePedidoController::class,
    ];

    if (!isset($map[$resource])) {
        http_response_code(404);
        echo json_encode(['error' => 'Not found']);
        return;
    }

    $controller = new $map[$resource]();

    if ($method === 'GET') {
        $controller->show($id);
        return;
    }

    if ($method === 'PUT' || $method === 'PATCH') {
        $controller->update($id);
        return;
    }

    if ($method === 'DELETE') {
        $controller->delete($id);
        return;
    }

    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    return;
}

if ($uri === '/' || $uri === '/index.php') {
    $controller = new HomeController();
    $controller->index();
    return;
}

if ($uri === '/health') {
    http_response_code(200);
    echo json_encode(['status' => 'ok']);
    return;
}

http_response_code(404);
echo json_encode(['error' => 'Not found']);
