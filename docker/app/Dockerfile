FROM python:3.10.6-bullseye as builder
WORKDIR /app
COPY . /app
RUN apt-get update && \
    apt-get install -y build-essential rustc autoconf && \
    apt-get install -y libldap2-dev libsasl2-dev python3-dev libpq-dev python3-psycopg2 postgresql cron
RUN python3 -m pip install -r ./requirements.txt --disable-pip-version-check
RUN apt-get install -y ffmpeg

COPY docker/app/crontab /etc/
RUN chmod 644 /etc/crontab
