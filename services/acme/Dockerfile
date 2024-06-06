FROM alpine:latest

RUN apk add --no-cache curl socat openssl
RUN curl --silent https://raw.githubusercontent.com/acmesh-official/acme.sh/master/acme.sh | \
    sh -s -- --install-online

COPY ./services/acme/docker-entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +rx /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

EXPOSE 443
