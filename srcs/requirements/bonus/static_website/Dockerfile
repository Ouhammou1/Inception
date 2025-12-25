FROM  debian:12
 
RUN apt update && apt install -y nginx 


COPY index.html    /var/www/html/index.html
COPY styles.css    /var/www/html/styles.css
COPY script.js    /var/www/html/script.js


EXPOSE  80

CMD ["nginx", "-g", "daemon off;"]