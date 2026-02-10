<?php

$uri = trim(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH), '/');

$routes = [
    'auth/login' => __DIR__ . '/../routes/auth.php',
    'users'      => __DIR__ . '/../routes/users.php',
];

if (!isset($routes[$uri])) {
    jsonResponse(['error' => 'Ruta no encontrada'], 404);
}

require $routes[$uri];
?>
