#!/bin/bash

set -e

FOLDER_NAME=main

if [ ! -d $FOLDER_NAME ]; then
  django-admin startproject main .
fi

while ! nc $DB_HOST $DB_PORT; do
  echo "MARIADB is unavailable -- sleeping"
  sleep 1
done

python manage.py runserver 0.0.0.0:8000