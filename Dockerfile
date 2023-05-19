FROM python:3.10-alpine

WORKDIR /src

COPY ../ ./

# current pytest lasted version 7.3.1
RUN chmod +x ./debug/start.sh \
    && pip install -r requirements_dev.txt \
    && sed -i '113s/        encoding: str = "utf-8",/        encoding: str = "gbk",/' '/usr/local/lib/python3.10/site-packages/iniconfig/__init__.py'

WORKDIR ./debug

# 启动前需要先在debug/config/local.yaml文件中配置数据库参数和在debug/db目录中找到user.sql并运行初始化数据库。
ENTRYPOINT sh start.sh