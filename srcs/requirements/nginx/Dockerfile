FROM debian:12

RUN  apt update && apt install -y nginx openssl

RUN mkdir -p  /etc/nginx/ssl


RUN  openssl req -x509  -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout etc/nginx/ssl/nginx.key \
    -out etc/nginx/ssl/nginx.crt  \
    -subj "/C=MA/ST=TE/L=TE/O=1337/OU=student/CN=localhost"


COPY conf/nginx.conf /etc/nginx/nginx.conf

# RUN rm -rf /var/www/html/*
# COPY conf/index.html /var/www/html/index.html
# COPY conf/index.html /etc/nginx/index.html

CMD ["nginx" , "-g" , "daemon off;"]
