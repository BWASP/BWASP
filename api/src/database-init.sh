#!/bin/sh

dockerize -wait tcp://bwasp-database-1:3306 -timeout 20s

# Apply database migrations
echo "Apply database migrations"
cd /usr/src/app; flask db upgrade; python3 app.py