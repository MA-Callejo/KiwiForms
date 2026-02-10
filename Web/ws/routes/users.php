<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../core/response.php';
require_once __DIR__ . '/../core/auth.php';

// GET: listar usuarios
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
	// Comprobar token
    try {
		$headers = getallheaders();
		$authHeader = $headers['Authorization'] ?? '';
		if (!$authHeader || !str_starts_with($authHeader, 'Bearer ')) {
			jsonResponse(['error'=>'Token no proporcionado'], 401);
		}
		$token = substr($authHeader, 7);
		$userData = verifyToken($token);
		if(!$userData) {
			jsonResponse(['error'=>'Token inválido o expirado'], 401);
		}
        $stmt = db()->query("SELECT id, nombre, correo FROM usuarios");
        $users = $stmt->fetchAll(PDO::FETCH_ASSOC);

        jsonResponse(['users' => $users]);
    } catch (Exception $e) {
        jsonResponse(['error' => 'Error al obtener usuarios',
        'detalle' => $e->getMessage()], 500);
    }
}

// POST: crear usuario
elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);

    if (empty($data['name']) || empty($data['email']) || empty($data['password'])) {
        jsonResponse(['error' => 'Faltan datos'], 400);
    }

    try {
        $stmt = db()->prepare("INSERT INTO usuarios (nombre, correo, hashPass) VALUES (?, ?, ?)");
        $hashed = password_hash($data['password'], PASSWORD_DEFAULT);
        $stmt->execute([$data['name'], $data['email'], $hashed]);

        jsonResponse(['status' => 'ok', 'id' => db()->lastInsertId()]);
    } catch (Exception $e) {
        jsonResponse([
        'error' => 'No se pudo crear usuario',
        'detalle' => $e->getMessage()
    ], 500);
    }
}

// Otro método no permitido
else {
    jsonResponse(['error' => 'Método no permitido'], 405);
}
?>
