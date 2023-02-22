FROM python:3.10

LABEL maintainer="woohaen88@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./run.sh /run.sh

ARG USER=wyatt88
WORKDIR /backend_app

RUN apt-get -y update && \
    apt-get -y install netcat-openbsd && \
    python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/

RUN adduser --disabled-password --no-create-home $USER

RUN mkdir -p /data/media && \
    mkdir -p /data/static && \
    chown -R $USER:$USER /data/media &&\
    chown -R $USER:$USER /data/static &&\
    chown -R $USER:$USER /venv &&\
    chown -R $USER:$USER /backend_app &&\
    chown -R $USER:$USER /run.sh


ENV PATH="/:/venv/bin/:$PATH"

USER $USER

RUN chmod +x /run.sh

CMD ["/run.sh"]