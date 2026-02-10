<?php

require_once __DIR__ . '/auth.php';
require_once __DIR__ . '/response.php';

$routes = [
    'auth/login' => __DIR__ . '/../routes/auth.php',
    'users'      => __DIR__ . '/../routes/users.php',
];

if (!isset($routes[$uri])) {
    jsonResponse(['error' => 'Ruta no encontrada'], 404);
}

$publicRoutes = ['auth/login'];

if (!in_array($uri, $publicRoutes)) {
    $headers = getallheaders();
    $authHeader = $headers['Authorization'] ?? '';

    if (!$authHeader || !str_starts_with($authHeader, 'Bearer ')) {
        jsonResponse(['error'=>'Token no proporcionado'], 401);
    }

    $token = substr($authHeader, 7);

    try {
        $userData = verifyToken($token);
    } catch (Exception $e) {
        jsonResponse(['error'=>'Token inválido o expirado'], 401);
    }
}

require $routes[$uri];
?>
