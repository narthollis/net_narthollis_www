FROM ghcr.io/getzola/zola:v0.22.0 AS builder

COPY . /project
WORKDIR /project
RUN ["zola", "build"]

FROM ghcr.io/static-web-server/static-web-server:3.0.0-beta.1-alpine AS server

FROM scratch

COPY --from=server /usr/local/bin/static-web-server /

COPY --from=builder /project/public /public

# K8s environment variables replace config files
ENV SERVER_ROOT=/public \
    SERVER_PORT=8080 \
    SERVER_HEALTH_CHECK=true \
    SERVER_LOG_REMOTE_ADDRESS=false

EXPOSE 8080

STOPSIGNAL SIGQUIT

ENTRYPOINT ["/static-web-server"]

