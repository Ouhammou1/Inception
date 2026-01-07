FROM debian:12

RUN apt-get update -y && \
    apt-get install -y mariadb-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /run/mysqld && chown -R mysql:mysql /run/mysqld

COPY conf/50-server.cnf /etc/mysql/mariadb.conf.d/50-server.cnf
COPY tools/script.sh /script.sh

RUN chmod +x /script.sh

EXPOSE 3306

ENTRYPOINT ["/script.sh"]
CMD ["mysqld"]
