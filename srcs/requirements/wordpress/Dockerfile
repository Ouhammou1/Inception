FROM  debian:bullseye


RUN  apt update && apt install -y \
    php-fpm \
    php-mysql \
    php-curl \
    php-gd \
    php-intl \
    php-mbstring \
    php-soap \
    php-xml \
    php-xmlrpc \
    php-zip \
    curl \
    mariadb-client \
    tar \
    && rm -rf /var/lib/apt/lists/*

WORKDIR  /var/www/html

RUN curl -O https://wordpress.org/latest.tar.gz && \
    tar -xzf latest.tar.gz && \
    rm latest.tar.gz && \
    chown -R www-data:www-data /var/www/html



COPY conf/wp-config.php /var/www/html/wordpress/wp-config.php

# RUN sed -i 's|listen = .*|listen = 9000|' /etc/php/*/fpm/pool.d/www.conf

# RUN mkdir -p /run/php

EXPOSE 9000

CMD ["sh", "-c", "mkdir -p /run/php && php-fpm7.4 -F"]
