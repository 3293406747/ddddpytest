#!/bin/bash
if [ -e "flask_app" ]; then
    cd flask_app
    flask run &
    cd ..

    if [ -e "main.py" ]; then
        python3 main.py
    fi
else
    echo flask_app目录不存在
fi

