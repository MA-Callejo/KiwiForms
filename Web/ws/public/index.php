<?php

require_once __DIR__ . '/../config/config.php';
require_once __DIR__ . '/../core/response.php';

$uri = $_GET['route'] ?? '';
require_once __DIR__ . '/../core/router.php';
?>
