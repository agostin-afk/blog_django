#!/bin/sh
echo 'Executando o makemigrations e migrate'

python manage.py makemigrations --noinput
python manage.py migrate --noinput