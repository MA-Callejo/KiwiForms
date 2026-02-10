<?php

function generateToken(int $userId): string
{
    return hash_hmac(
        'sha256',
        $userId . '|' . time(),
        $_ENV['APP_SECRET']
    );
}
?>
