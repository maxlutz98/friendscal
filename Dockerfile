# pull official base image
FROM python:3.7-alpine

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory and create user
WORKDIR /code

# install dependencies
RUN apk update \
    && apk upgrade \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --virtual build-deps2 jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev postgresql-dev \
    && pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt 

# cleanup
RUN rm requirements.txt \
    && apk del build-deps build-deps2

# copy entrypoint.sh
COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY project /code


# expose port
EXPOSE 8000

# run docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]