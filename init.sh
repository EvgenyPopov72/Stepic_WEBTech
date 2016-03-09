#!/usr/bin/env bash

sudo ln -s /home/box/web/etc/mysql.cnf /etc/mysql/conf.d/stepic.cnf
sudo /etc/init.d/mysql restart

sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo /etc/init.d/nginx restart

sudo ln -s /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/test
sudo /etc/init.d/gunicorn restart