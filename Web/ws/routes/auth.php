<?php

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    jsonResponse(['error' => 'Método no permitido'], 405);
}

$data = json_decode(file_get_contents('php://input'), true);

if (empty($data['email']) || empty($data['password'])) {
    jsonResponse(['error' => 'Datos incompletos'], 400);
}

// Aquí validarías contra BBDD

jsonResponse([
    'status' => 'ok',
    'token'  => 'token_de_ejemplo'
]);
?>
