#!/bin/bash

cd geochat
echo "======Собираем статику======"
if [ "$DEBUG" == "False" ]; then
    echo "======Загружаем в S3 облако, это займет некоторое время======"
fi
python manage.py collectstatic --noinput


#echo "======Таки ждем, пока постгра поднимется======"
#while ! curl http://web_db:5432/ 2>&1 | grep '52'
#do
#  echo "Таки ждем....."
#  sleep 1
#done
#echo "Таки дождались..........."

echo "======Накатываем миграции======"
python manage.py makemigrations
python manage.py migrate


echo "======Стартуем сервер======"
if [ "$DEBUG" == "True" ]; then
    ./manage.py runserver 0.0.0.0:81
else


    daphne -e ssl:443:privateKey=../config/ssl_keys/privkey.pem:certKey=../config/ssl_keys/fullchain.pem  -b 0.0.0.0 -p 81 geochat.asgi:application

fi
