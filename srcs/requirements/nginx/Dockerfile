FROM debian:bullseye

RUN apt update && apt install -y nginx openssl


RUN mkdir -p  /etc/nginx/ssl

RUN openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt  \
     -subj "/C=MA/ST=TE/L=TE/O=1337/OU=student/CN=localhost"

COPY conf/nginx.conf /etc/nginx/nginx.conf


CMD ["nginx", "-g" , "daemon off;"]