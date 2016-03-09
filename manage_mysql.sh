#!/usr/bin/env bash

sudo /etc/init.d/mysql restart

mysql -uroot -e "CREATE DATABASE stepic_django;"
mysql -uroot -e "CREATE USER 'box'@'localhost' IDENTIFIED BY '1234';"
mysql -uroot -e "GRANT ALL ON stepic_django.* TO 'box';"
# mysql -uroot -e "FLUSH PRIVILEGES;"
