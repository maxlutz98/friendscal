# pull official base image
FROM python:3.7-alpine

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# build environment variables
ARG USER=django
ENV UID=1000
ENV GID=1000

# set work directory and create user
WORKDIR /code
# RUN addgroup -S --gid ${GID} ${USER} && adduser -S -u ${UID} ${USER} -G ${USER}

# install dependencies
RUN apk update \
    && apk upgrade \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev postgresql-dev curl \
    && pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt 

# cleanup
RUN rm requirements.txt \
    && apk del build-deps

# copy entrypoint.sh
COPY --chown=django:django docker-entrypoint.sh /docker-entrypoint.sh

# set user
# USER ${USER}

# expose port
EXPOSE 8000

# run docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]