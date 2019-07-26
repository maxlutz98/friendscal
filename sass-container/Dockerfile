FROM ubuntu

RUN mkdir /src && mkdir /work
WORKDIR /work
RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install curl wget
RUN curl -s https://api.github.com/repos/sass/dart-sass/releases/latest \
    | grep browser_download_url \
    | grep linux-x64 \
    | cut -d '"' -f 4 \
    | wget -qi -
RUN tar -xzvf dart-sass*.tar.gz && rm dart-sass*.tar.gz && apt-get purge -y curl wget && apt autoremove -y --purge && apt-get clean -y
COPY ./docker-entrypoint.sh /work/docker-entrypoint.sh
ENTRYPOINT [ "sh", "/work/docker-entrypoint.sh" ]