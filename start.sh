#!/bin/bash
ls -lat
root=/home/ubuntu/schedulemaker

sudo unzip -o $root/backend.zip -d $root/

sudo apt-get install -y python3 python3-pip
sudo apt-get install -y virtualenv
sudo apt-get install -y mysql-server
sudo apt-get install -y libmysqlclient-dev
sudo apt-get install -y apt-xapian-index

sudo virtualenv -p python3 $root/venv
sudo chown -R ubuntu $root/venv
source $root/venv/bin/activate

pip3 install -r $root/backend/requirements.txt
gunicorn --chdir ./backend/ schedulemaker.wsgi:application  --timeout 900