FROM debian:12

RUN apt update && apt install -y \
    php8.2-fpm \
    php8.2-mysql \
    php8.2-curl \
    php8.2-gd \
    php8.2-intl \
    php8.2-mbstring \
    curl \
    mariadb-client \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar \
    -o /usr/local/bin/wp \
    && chmod +x /usr/local/bin/wp

RUN sed -i 's|listen = .*|listen = 9000|' /etc/php/8.2/fpm/pool.d/www.conf

RUN mkdir -p /run/php

WORKDIR /var/www/html

COPY tools/script.sh /script.sh

RUN chmod +x /script.sh

EXPOSE 9000
ENTRYPOINT ["/script.sh"]
