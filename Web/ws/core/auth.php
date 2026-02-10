<?php

require_once __DIR__ . '/jwt.php';

function generateToken(int $userId): string {
    return jwt_encode(['user_id'=>$userId], $_ENV['APP_SECRET'], 3600);
}

function verifyToken(string $jwt): array {
    return jwt_decode($jwt, $_ENV['APP_SECRET']);
}
?>
