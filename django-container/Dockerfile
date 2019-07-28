# pull official base image
FROM python:3.7

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set work directory and create user
WORKDIR /code
RUN groupadd -r django && useradd -r -g django django

# install dependencies
RUN apt-get update && apt-get upgrade -y && pip install --upgrade pip
RUN apt-get install -y netcat curl 
COPY requirements.txt /code/
RUN pip install -r requirements.txt && pip install mysqlclient && rm requirements.txt

# copy entrypoint.sh
COPY --chown=django:django docker-entrypoint.sh /docker-entrypoint.sh

# set user
USER django

# healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:8000/ || exit 1

# run docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]