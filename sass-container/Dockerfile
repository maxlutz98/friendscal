# pull official base image
FROM ubuntu

# set work directory and create user
WORKDIR /work
RUN groupadd -r sass && useradd -r -g sass sass

# install dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install curl wget

# install sass
RUN curl -s https://api.github.com/repos/sass/dart-sass/releases/latest \
    | grep browser_download_url \
    | grep linux-x64 \
    | cut -d '"' -f 4 \
    | wget -qi -
RUN tar -xzvf dart-sass*.tar.gz 

# cleanup
RUN rm dart-sass*.tar.gz && apt-get purge -y curl wget && apt autoremove -y --purge && apt-get clean -y

# copy entrypoint.sh
COPY --chown=sass:sass ./docker-entrypoint.sh /work/docker-entrypoint.sh

# set user
USER sass

# run docker-entrypoint.sh
ENTRYPOINT [ "sh", "/work/docker-entrypoint.sh" ]