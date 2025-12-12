#!/bin/bash

# set -e

# # Ensure correct permissions for the mysqld runtime directory
# mkdir -p /run/mysqld
# chown -R mysql:mysql /run/mysqld

# # Initialize MariaDB data directory if empty
# if [ ! -d "/var/lib/mysql/mysql" ]; then
#     echo "Initializing MariaDB data directory..."
#     mysql_install_db --user=mysql --ldata=/var/lib/mysql > /dev/null
# fi

# # Start MariaDB temporarily (safe mode)
# echo "Starting MariaDB in bootstrap mode..."
# mysqld --bootstrap --user=mysql <<-EOF
# USE mysql;

# FLUSH PRIVILEGES;

# CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE}\`;

# CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
# GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE}\`.* TO '${MYSQL_USER}'@'%';

# ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';

# FLUSH PRIVILEGES;
# EOF

# echo "MariaDB configured successfully."

# # Start MariaDB normally (foreground mode)
# exec mysqld --user=mysql


set -e

# Ensure correct permissions for the mysqld runtime directory
mkdir -p /run/mysqld
chown -R mysql:mysql /run/mysqld

# Initialize MariaDB data directory if empty
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "Initializing MariaDB data directory..."
    mysql_install_db --user=mysql --ldata=/var/lib/mysql > /dev/null
fi

echo "Starting MariaDB in bootstrap mode..."
mysqld --bootstrap --user=mysql <<-EOF
USE mysql;

FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE};

CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';

ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';

FLUSH PRIVILEGES;
EOF

echo "MariaDB configured successfully."

exec mysqld --user=mysql
