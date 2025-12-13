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
    && rm -rf /var/lib/apt/lists/*

# Force PHP-FPM to listen on TCP 9000 (needed for Nginx)
RUN sed -i 's|listen = .*|listen = 9000|' /etc/php/7.4/fpm/pool.d/www.conf

# Create runtime directory
RUN mkdir -p /run/php

# Set working directory (this is the VOLUME)
WORKDIR /var/www/html

# Copy entrypoint script
COPY tools/script.sh /script.sh
RUN chmod +x /script.sh

# Start WordPress installer then PHP-FPM
ENTRYPOINT ["/script.sh"]
CMD ["php-fpm7.4", "-F"]
