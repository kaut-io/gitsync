FROM alpine:latest

RUN apk update && \
apk add python3 py3-pip git bash curl openssh-client

RUN apk add py3-setuptools

RUN adduser -D -u 1000 git

USER git

RUN python3 -m venv /tmp/gitsync/venv

COPY requirements.txt /tmp/gitsync/
RUN . /tmp/gitsync/venv/bin/activate && \
pip3 install --upgrade pip && \
pip3 install -r /tmp/gitsync/requirements.txt && \
mkdir ~/.ssh && touch ~/.ssh/known_hosts

COPY main.py /tmp/gitsync/

CMD . /tmp/gitsync/venv/bin/activate && exec python3 -u /tmp/gitsync/main.py
