# site-packages/iniconfig/__init__.py中编码问题未解决
FROM python:3.10-alpine

WORKDIR /src

COPY ../ ./

RUN chmod ugo+x start.sh && pip install -r requirements_dev.txt

ENTRYPOINT sh ./debug/start.sh