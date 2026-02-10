<?php
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../core/response.php';
require_once __DIR__ . '/../core/auth.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    jsonResponse(['error'=>'Método no permitido'], 405);
}

$data = json_decode(file_get_contents('php://input'), true);
if(empty($data['email']) || empty($data['password'])) {
    jsonResponse(['error'=>'Faltan datos'], 400);
}

try {
    $stmt = db()->prepare("SELECT id, hashPass FROM usuarios WHERE correo = ?");
    $stmt->execute([$data['email']]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);

    if(!$user || !password_verify($data['password'], $user['hashPass'])) {
        jsonResponse(['error'=>'Usuario o contraseña incorrectos'], 401);
    }

    $token = generateToken($user['id']);

    jsonResponse([
        'status'=>'ok',
        'user_id'=>$user['id'],
        'token'=>$token
    ]);

} catch(Exception $e) {
    jsonResponse(['error'=>'Error al autenticar','detalle'=>$e->getMessage()], 500);
}
?>
