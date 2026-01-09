#!/bin/sh
set -e

chown -R mysql:mysql /var/lib/mysql 
chown -R mysql:mysql /run/mysqld


if [ ! -f "/var/lib/mysql/.initialized" ]; then

    echo "Initializing MariaDB data directory..."
    mysql_install_db  --user=mysql --datadir=/var/lib/mysql

    echo "Starting temporary MariaDB instance..."
    mysqld --user=mysql --datadir=/var/lib/mysql --skip-networking & pid="$!"


    for i in $(seq 30); do 
        if mysqladmin ping  --silent 2>/dev/null; then
            break
        fi
        sleep 1
    done
    
    echo "Configuring database..."
    mysql <<EOF
CREATE DATABASE IF NOT EXISTS \`${MYSQL_DATABASE}\`;
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';
GRANT ALL PRIVILEGES ON \`${MYSQL_DATABASE}\`.* TO '${MYSQL_USER}'@'%';
ALTER USER 'root'@'localhost' IDENTIFIED BY '${MYSQL_ROOT_PASSWORD}';
FLUSH PRIVILEGES;
EOF

    echo "Shutting down temporary instance..."
    mysqladmin -u root -p"${MYSQL_ROOT_PASSWORD}" shutdown
    wait "$pid"

    echo "Database initialization complete!"
    touch /var/lib/mysql/.initialized

fi

echo "Starting MariaDB..."
exec mysqld --user=mysql --bind-address=0.0.0.0 --datadir=/var/lib/mysql