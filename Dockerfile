FROM python:3.10-alpine

WORKDIR /src

COPY ../ ./

# current pytest lasted version 7.3.1
RUN chmod ugo+x ./debug/start.sh \
    && pip install -r requirements_dev.txt \
    && sed -i '113s/        encoding: str = "utf-8",/        encoding: str = "gbk",/' '/usr/local/lib/python3.10/site-packages/iniconfig/__init__.py'

ENTRYPOINT sh ./debug/start.sh