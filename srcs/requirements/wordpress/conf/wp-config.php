<?php

define('DB_NAME' , getenv("MYSQL_DATABASE"));
define('DB_USER', getenv('MYSQL_USER'));
define('DB_PASSWORD' , getenv('MYSQL_PASSWORD'));
define('DB_HOST' , getenv('MYSQL_HOST'));


define('DB_CHARSET' , 'utf8');
define('DB_COLLATE' '');

$table_prefix= 'wp_';
define('WP_DEBUG' , true);


if( ! define('ABSPATH') )
    define('ABSPATH' , __DIR__ . '/');


require_once ABSPATH . 'wp-config.php';
