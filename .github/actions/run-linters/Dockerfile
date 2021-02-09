FROM python:latest

RUN apt update && \
    apt -y install jq

RUN pip install --upgrade pip
RUN pip install autopep8 flake8

COPY entrypoint.sh /entrypoint.sh
RUN chmod 700 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]