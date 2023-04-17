# site-packages/iniconfig/__init__.py中编码问题未解决
# 未配置邮件和数据库参数 sql未执行
FROM python:3.10-alpine

WORKDIR /src

COPY ../ ./

RUN chmod ugo+x start.sh && pip install -r requirements_dev.txt

ENTRYPOINT sh ./debug/start.sh