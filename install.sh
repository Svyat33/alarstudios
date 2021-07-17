#!/bin/sh
set -e
echo "Start containers"
docker-compose up -d > /dev/null 2>&1
sleep 5
echo "start cunsumers"
docker-compose up -d > /dev/null 2>&1
sleep 3
echo "Create database tables"
docker-compose exec account python manage.py migrate > /dev/null 2>&1
docker-compose exec dots python manage.py migrate > /dev/null 2>&1
echo "Create test users"
docker-compose exec account python manage.py create_users
echo "Generate 500000 dots"
docker-compose exec dots python manage.py populate
echo "Copy dots to redis DB"
docker-compose exec dots python manage.py dottoredis
date