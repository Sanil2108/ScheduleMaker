#!/bin/bash
ls -lat
sudo unzip -o backend.zip

sudo apt-get install -y python3 python3-pip
sudo apt-get install -y virtualenv
sudo apt-get install -y mysql-server
sudo apt-get install -y libmysqlclient-dev

sudo virtualenv -p python3 venv
sudo chown -R ubuntu venv
source venv/bin/activate

pip3 install -r backend/requirements.txt
python3 backend/manage.py runserver
