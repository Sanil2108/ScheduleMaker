#!/bin/bash
unzip -o backend.zip

apt-get install python3 python3-pip
apt-get install virtualenv

virtualenv -p python3 venv
source venv/bin/activate

pip3 install -r backend/requirements.txt
python3 backend/manage.py runserver
