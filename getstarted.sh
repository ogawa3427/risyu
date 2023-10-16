#!/bin/bash

sudo apt update -y
sudo apt upgrade -y
sudo apt install python3-pip -y
pip install flask
sudo apt install python3-flask -y
sudo apt install apache2 -y
sudo apt -y install python3-pip libapache2-mod-wsgi-py3
sudo apt install gunicorn -y
sudo ln -sT ~/risyu /var/www/html/risyu
cat conf_template.txt | sudo tee /etc/apache2/sites-enabled/000-default.conf > /dev/null
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2