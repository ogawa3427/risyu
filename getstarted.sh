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
cat sv_admin/conf_template.txt | sudo tee /etc/apache2/sites-enabled/000-default.conf > /dev/null
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2

echo "Congratulations! You can get comleated successfully starting the Risyu Server by few steps! \n Please excuse this command /"gunicorn app:app" and access the server at http://your-global\ip \nNext, consider setting up a domain name and SSL certificate for your server. \nThey are not necessary, but they will make your server more secure and easier to access. \nYou can find instructions for setting up a domain name and SSL certificate at man-page of mine.:)"
exit