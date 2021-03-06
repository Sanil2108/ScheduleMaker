#!/bin/bash
root=/home/ubuntu/schedulemaker

touch $root/log;

sudo unzip -o $root/backend.zip -d $root/

sudo apt-get install -y python3 python3-pip
sudo apt-get install -y virtualenv
sudo apt-get install -y mysql-server
sudo apt-get install -y libmysqlclient-dev
sudo apt-get install -y apt-xapian-index
sudo apt-get install -y gunicorn

sudo virtualenv -p python3 $root/venv
sudo chown -R ubuntu $root/venv
source $root/venv/bin/activate

# Database setup
export DATABASE_USER=$(cat ~/DB_CREDENTIALS.csv | cut -d"," -f1)
export DATABASE_PASSWORD=$(cat ~/DB_CREDENTIALS.csv | cut -d"," -f2)
sudo mysql -e "CREATE DATABASE schedulemaker;" >> $root/log;
sudo mysql -e "GRANT ALL PRIVILEGES ON schedulemaker.* TO $(echo $DATABASE_USER)@'localhost'" >> $root/log;
# https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost
sudo mysql -D "sql" -e "UPDATE user SET plugin='mysql_native_password' WHERE User='root';";
sudo mysql -D "sql" -e "UPDATE user SET plugin='mysql_native_password' WHERE User='$DATABASE_USER';";
sudo mysql -D "sql" -e "FLUSH PRIVILEGES;";
sudo service mysql restart;
python3 $root/backend/manage.py makemigrations
python3 $root/backend/manage.py migrate

pip3 install -r $root/backend/requirements.txt
sudo fuser -k 8001/tcp;
sudo su ubuntu
gunicorn --chdir $root/backend/ -b 127.0.0.1:8001 schedulemaker.wsgi:application  --timeout 900 --daemon