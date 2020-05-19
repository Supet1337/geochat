#!/bin/bash

echo "Накатываем миграции"
python geochat/geochat/manage.py makemigrations
python geochat/geochat/manage.py migrate


echo "Запускаем тесты"
pytest --cov -v -x | tee pytest.txt
coverage html

coverage=$(sed -n 's/^TOTAL *[0-9]* *[0-9]* *\([0-9]*\)%/\1/p' pytest.txt)
echo "Покрытие кода: $coverage%"

