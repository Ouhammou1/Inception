#!/bin/sh
set -e

# Ensure correct permissions
chown -R mysql:mysql /var/lib/mysql
chown -R mysql:mysql /run/mysqld

# Initialize database directory if empty
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "Initializing MariaDB data directory..."
    mysql_install_db --user=mysql --datadir=/var/lib/mysql
fi

# Start MariaDB in background (NO skip-grant-tables)
mysqld --user=mysql --bind-address=0.0.0.0 &
pid="$!"

# Wait for MariaDB to be ready
echo "Waiting for MariaDB..."
until mysqladmin ping --silent; do
    sleep 1
done

echo "Configuring database..."

mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE}\`;
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE}\`.* TO '${MYSQL_USER}'@'%';
ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';
FLUSH PRIVILEGES;
EOF

# Bring MariaDB back to foreground
wait "$pid"
