FROM mongo:latest

RUN mkdir -p /etc/ssl /var/log/mongo

COPY ./build/initdb.js /docker-entrypoint-initdb.d/initdb.js
COPY ./services/mongo/mongod.conf /etc/mongo/mongod.conf
COPY ./build/ssl/mongo.pem /etc/ssl/internal/mongo.pem
COPY ./build/ssl/ca.pem /etc/ssl/internal/ca.pem

RUN rm -rf /data/db
RUN chown -R mongodb:mongodb /etc/ssl /var/log/mongo /etc/mongo /docker-entrypoint-initdb.d

EXPOSE 27017

CMD ["mongod", "--quiet", "--config", "/etc/mongo/mongod.conf"]
