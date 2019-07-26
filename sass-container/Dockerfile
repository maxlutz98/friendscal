FROM ubuntu:18.04 as build
ARG UPSTREAM_VERSION=1.22.8
ADD https://github.com/sass/dart-sass/releases/download/${UPSTREAM_VERSION}/dart-sass-${UPSTREAM_VERSION}-linux-x64.tar.gz /opt/
RUN tar -C /opt/ -xzvf /opt/dart-sass-${UPSTREAM_VERSION}-linux-x64.tar.gz
COPY ./docker-entrypoint.sh /opt/dart-sass

FROM ubuntu:18.04 as final
COPY --from=build /opt/dart-sass /opt/dart-sass

ENTRYPOINT [ "sh", "/opt/dart-sass/docker-entrypoint.sh" ]
