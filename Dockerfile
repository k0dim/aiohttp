FROM python:3.11-alpine
COPY ./app /app

WORKDIR /app

RUN apk update && apk add bash

RUN pip install --no-cache-dir -r /app/requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

ENTRYPOINT /wait && bash ./entrypoint.sh