#!/bin/sh
set -e


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
    if mysqladmin  ping -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent 2>/dev/null; then
        echo "MariaDB is ready!"
        break
    fi
    echo "Attempt $i/40 .."
    sleep 2
done

if [ ! -f wp-config.php ]; then
    echo "Creating wp-config.php..."
    wp config create \
    --allow-root \
    --dbname="$MYSQL_DATABASE" \
    --dbuser="$MYSQL_USER" \
    --dbpass="$MYSQL_PASSWORD" \
    --dbhost="$MYSQL_HOST" \
    --force 
    echo "wp-config.php created"
fi


if !  wp core is-installed --allow-root 2>/dev/null; then
    echo "Installing WordPress..."
    wp core install \
    --allow-root \
    --url="https://$DOMAIN_NAME" \
    --title="BRAHIM OUHAMMOU" \
    --admin_user="$WP_ADMIN_USER" \
    --admin_password="$WP_ADMIN_PASSWORD" \
    --admin_email="$WP_ADMIN_EMAIL" \
    --skip-email
    echo "WordPress installed"
else
    echo "WordPress is already installed"
fi

if [ -n "$WP_USER" ] && [ -n "$WP_USER_EMAIL" ] && [ -n "$WP_USER_PASSWORD" ]; then
    if  ! wp user get  "$WP_USER" --allow-root >/dev/null 2>&1; then
    echo "Creating user: $WP_USER"
        wp user create \
        "$WP_USER" "$WP_USER_EMAIL" --user_pass="$WP_USER_PASSWORD" --role=subscriber --allow-root
        echo "User created"
    else
        echo "User $WP_USER already exists"
    fi
fi


echo "=== WordPress ready ==="

chown -R www-data:www-data /var/www/html

exec php-fpm8.2 -F

