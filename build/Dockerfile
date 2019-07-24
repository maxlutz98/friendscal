FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get upgrade -y && pip install --upgrade pip
RUN pip install -r requirements.txt && pip install mysqlclient && rm requirements.txt