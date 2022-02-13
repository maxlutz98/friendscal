# pull official base image
FROM python:3.10.2-alpine

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory and create user
WORKDIR /code

# install dependencies
RUN apk update \
    && apk upgrade \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev harfbuzz-dev fribidi-dev postgresql-dev \
    && pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt 

# cleanup
RUN rm requirements.txt \
    && apk del build-deps

# copy entrypoint.sh
COPY docker-entrypoint.sh /docker-entrypoint.sh
COPY project /code

# create additional user
RUN adduser -D django
# set created user as used
USER django

# expose port
EXPOSE 8000

# run docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]