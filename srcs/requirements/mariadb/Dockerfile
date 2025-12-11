FROM debian:bullseye

RUN apt-get update && apt-get install  mariadb-server -y 

COPY conf/mariadb.cnf /etc/mysql/mariadb.conf.d/50-server.cnf
COPY tools/script.sh /script.sh

RUN chmod +x /script.sh \
    && mkdir -p /run/mysqld \
    && chown -R mysql:mysql /run/mysqld \
    && chown -R mysql:mysql /var/lib/mysql

EXPOSE 3306

CMD ["/script.sh"]
