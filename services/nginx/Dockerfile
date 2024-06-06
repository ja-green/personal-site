FROM nginx:latest

RUN mkdir -p /etc/ssl
RUN rm -rf /usr/share/nginx/html/*

COPY ./services/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./services/nginx/error-pages /usr/share/nginx/html/error-pages
COPY ./build/ssl/ca.pem /etc/ssl/internal/ca.pem
COPY ./jackgreen_co/core/static /usr/share/nginx/html/assets

RUN chown -R nginx:nginx /usr/share/nginx/html /etc/ssl /var/log/nginx

COPY ./services/nginx/docker-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +rx /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;", "-c", "/etc/nginx/nginx.conf"]
