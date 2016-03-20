#!/usr/bin/env bash

sudo apt-get update && sudo apt-get install -y mc && sudo pip install --upgrade django

# Настройка базы mysql
sudo ln -s /home/box/web/etc/mysql.cnf /etc/mysql/conf.d/stepic.cnf
sudo /etc/init.d/mysql restart
sudo sh manage_mysql.sh

# Создание таблиц в базе и пользователя
cd /home/box/web/ask
python manage.py migrate
#python manage.py shell  from django.contrib.auth.models import User \n user = User.objects.create_user('TheJohnLennon', 'lennon@thebeatles.com', 'johnpassword').save()
echo "Create user.."
#python manage.py shell
python manage.py createsuperuser --username=joe --email=joe@example.com

# Настройка nginx
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart

# Настройка gunicorn
sudo ln -s /home/box/web/etc/gunicorn.conf.old /etc/gunicorn.d/test
sudo /etc/init.d/gunicorn restart