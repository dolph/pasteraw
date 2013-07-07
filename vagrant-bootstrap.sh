#!/bin/bash
sudo apt-get update
sudo apt-get -y -V install apache2 libapache2-mod-wsgi python-setuptools screen
cd /vagrant/
sudo python setup.py install
screen -d -m python runserver.py
rm /etc/apache2/sites-enabled/*
cp config/apache2/flaskr /etc/apache2/sites-enabled/
