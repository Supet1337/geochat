#!/bin/bash

cd geochat
echo "======Собираем статику======"
python manage.py collectstatic --noinput

#echo "======Таки ждем, пока постгра поднимется======"
#while ! curl http://web_db:5432/ 2>&1 | grep '52'
#do
#  echo "Таки ждем....."
#  sleep 1
#done
#echo "Таки дождались..........."

echo "======Накатываем миграции======"
#python manage.py makemigrations
python manage.py migrate

echo "======Стартуем сервер======"

gunicorn --certfile=../config/nginx/certs/localhost.crt --keyfile=../config/nginx/certs/localhost.key geochat.wsgi:application --bind 0.0.0.0:443
#python manage.py runserver 0.0.0.0:80