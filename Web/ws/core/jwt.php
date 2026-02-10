<?php
require_once __DIR__ . '/../config/config.php';

function jwt_encode(array $payload, string $secret, int $exp = 3600): string {

    $header = json_encode(['typ'=>'JWT','alg'=>'HS256']);
    $payload['exp'] = time() + $exp;

    $base64UrlHeader = rtrim(strtr(base64_encode($header), '+/', '-_'), '=');
    $base64UrlPayload = rtrim(strtr(base64_encode(json_encode($payload)), '+/', '-_'), '=');

    $signature = hash_hmac('sha256', "$base64UrlHeader.$base64UrlPayload", $secret, true);
    $base64UrlSignature = rtrim(strtr(base64_encode($signature), '+/', '-_'), '=');

    return "$base64UrlHeader.$base64UrlPayload.$base64UrlSignature";
}

function jwt_decode(string $jwt, string $secret): array {

    $parts = explode('.', $jwt);
    if(count($parts) !== 3) throw new Exception("Token malformado");

    [$headerB64, $payloadB64, $sigB64] = $parts;

    $signatureCheck = hash_hmac('sha256', "$headerB64.$payloadB64", $secret, true);
    $signatureCheckB64 = rtrim(strtr(base64_encode($signatureCheck), '+/', '-_'), '=');

    if(!hash_equals($signatureCheckB64, $sigB64)) throw new Exception("Firma inválida");

    $payload = json_decode(base64_decode($payloadB64), true);
    if(!$payload) throw new Exception("Payload no válido");

    if(!isset($payload['exp'])) throw new Exception("Expiración no definida");
    if($payload['exp'] < time()) throw new Exception("Token expirado");

    return $payload;
}

?>
