#!/bin/sh
set -e

echo "=== WordPress entrypoint ==="

cd /var/www/html || exit 1

# 1. Download WordPress if not exists
if [ ! -f wp-includes/version.php ]; then
    echo "Downloading WordPress..."
    rm -rf /var/www/html/*
    curl -s https://wordpress.org/latest.tar.gz | tar -xz --strip-components=1
    chown -R www-data:www-data /var/www/html
    echo "WordPress downloaded"
fi

# 2. Wait for MariaDB
echo "Waiting for MariaDB..."
for i in $(seq 1 30); do
    if mysqladmin ping -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent 2>/dev/null; then
        echo "MariaDB is ready!"
        break
    fi
    echo "Attempt $i/30..."
    sleep 2
done

sleep 3

# 3. Create wp-config.php
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

# 4. Install WordPress
if ! wp core is-installed --allow-root 2>/dev/null; then
    echo "Installing WordPress..."
    wp core install \
        --allow-root \
        --url="https://$DOMAIN_NAME" \
        --title="Inception" \
        --admin_user="$WP_ADMIN_USER" \
        --admin_password="$WP_ADMIN_PASSWORD" \
        --admin_email="$WP_ADMIN_EMAIL" \
        --skip-email
    echo "WordPress installed"
fi

# 5. Create second user
if ! wp user get "$WP_USER" --allow-root >/dev/null 2>&1; then
    echo "Creating user: $WP_USER"
    wp user create \
        "$WP_USER" "$WP_USER_EMAIL" \
        --user_pass="$WP_USER_PASSWORD" \
        --role=subscriber \
        --allow-root
    echo "User created"
fi

echo "=== WordPress ready ==="

# Fix permissions
chown -R www-data:www-data /var/www/html

# Start PHP-FPM
exec php-fpm7.4 -F