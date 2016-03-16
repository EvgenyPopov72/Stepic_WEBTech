#!/usr/bin/env bash

cd ask
gunicorn ask.wsgi --config ../etc/gunicorn.conf
#--error-logfile /home/box/web/etc/gunicorn.err.log --log-level debug --access-logfile /home/box/web/etc/gunicorn.access.log
