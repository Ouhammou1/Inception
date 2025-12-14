FROM debian:bullseye

# Install PHP and required extensions
RUN apt update && apt install -y \
    php7.4-fpm \
    php7.4-mysql \
    php7.4-curl \
    php7.4-gd \
    php7.4-intl \
    php7.4-mbstring \
    curl \
    mariadb-client \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install wp-cli
RUN curl -fsSL https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar \
    -o /usr/local/bin/wp \
    && chmod +x /usr/local/bin/wp

# PHP-FPM config
RUN sed -i 's|listen = .*|listen = 9000|' /etc/php/7.4/fpm/pool.d/www.conf

RUN mkdir -p /run/php

WORKDIR /var/www/html

COPY tools/script.sh /script.sh
RUN chmod +x /script.sh

ENTRYPOINT ["/script.sh"]
CMD ["php-fpm", "-F"]
