FROM debian:bullseye

RUN  apt-get update && apt-get install -y \
    mariadb-server \
    mariadb-client \
    && rm -rf /var/lib/apt/mysql/mariadb

# COPY  conf/50-server.cnf /etc/mysql/mariadb/mariadb.conf.d/


RUN chmod +x /init_db.sh

EXPOSE 3306

# ENTERPOINT ["/init_db.sh"]