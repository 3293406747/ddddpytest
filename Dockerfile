FROM python:3.10-alpine

WORKDIR /src

COPY ../ ./

RUN chmod ugo+x start.sh && pip install -r requirements_dev.txt

ENTRYPOINT sh start.sh