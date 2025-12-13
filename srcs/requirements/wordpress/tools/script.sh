#!/bin/sh
set -e

cd /var/www/html

# Install WordPress only if not already installed
if [ ! -f wp-config.php ]; then
    echo "Installing WordPress..."

    curl -O https://wordpress.org/latest.tar.gz
    tar -xzf latest.tar.gz
    rm latest.tar.gz

    cp -r wordpress/* .
    rm -rf wordpress

    chown -R www-data:www-data /var/www/html
    chmod -R 755 /var/www/html
else
    echo "WordPress already installed, skipping."
fi

exec "$@"
