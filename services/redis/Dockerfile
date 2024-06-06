FROM redis:latest

RUN mkdir -p /etc/ssl /etc/redis

COPY ./services/redis/redis.conf /etc/redis/redis.conf
COPY ./build/ssl/redis-cert.pem /etc/ssl/internal/redis-cert.pem
COPY ./build/ssl/redis-key.pem /etc/ssl/internal/redis-key.pem
COPY ./build/ssl/ca.pem /etc/ssl/internal/ca.pem

COPY ./services/redis/docker-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +rx /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

RUN chown -R redis:redis /etc/ssl /etc/redis

EXPOSE 6379

CMD ["redis-server", "/etc/redis/redis.conf"]
