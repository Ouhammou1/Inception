#!/bin/sh
# sed -e


cd /var/www/html || exit 1

if [ ! -f wp-includes/version.php ]; then
    echo "Downloading WordPress..."
    rm -rf /var/www/html/*
    curl -s  https://wordpress.org/latest.tar.gz | tar -xz  --strip-components=1
    chown -R www-data:www-data /var/www/html 
    echo "WordPress downloaded"
fi


echo "Waiting for MariaDb..."

for i in $(seq 1 40 );do
    if mysqladmin  ping -h"$MYSQL_HOST" -u"MYSQL-USER" -p"MYSQL_PASSWORD" --silent 2>/dev/null; then
        echo "MariaDB is ready!"
        break
    fi
    echo "Attempt $i/40 .."
    sleep 2
done


if[! -f wp-config.php]; then
    echo "Creating wp-config.php..."
    