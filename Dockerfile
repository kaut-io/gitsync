FROM alpine

RUN apk update && \
apk add python3 py3-pip git bash curl openssh-client && \
pip3 install gitpython

CMD ["/usr/bin/python3", "main.py"]
