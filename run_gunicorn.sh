#!/usr/bin/env bash

cd ask
gunicorn ask.wsgi --config ../etc/gunicorn.conf