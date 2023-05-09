#!bin/bash
if [ -e "./debug/flask_app" ]; then
    cd ./debug/flask_app
    flask run &
    cd ..
    if [ -e "main.py" ]; then
        python3 main.py
    fi
else
    echo debug/flask_app目录不存在
fi

