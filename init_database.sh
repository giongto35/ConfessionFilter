#!/bin/bash

# Ensure we are in project directory
cd "$(dirname "$0")"

# Clear old database
mysql -u root -p -e 'drop database Confession;'
mysql -u root -p -e 'create database Confession CHARACTER SET utf8;'

# Create new database
python manage.py migrate
