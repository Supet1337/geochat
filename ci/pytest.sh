#!/bin/bash

echo "Накатываем миграции"
python3 geochat/manage.py makemigrations
python3 geochat/manage.py migrate
cd geochat/

echo "Запускаем тесты"
pytest --cov -v -x | tee pytest.txt
coverage html

coverage=$(sed -n 's/^TOTAL *[0-9]* *[0-9]* *\([0-9]*\)%/\1/p' pytest.txt)
echo "Покрытие кода: $coverage%"

#anybadge --value=score --file=public/coverage.svg coverage

