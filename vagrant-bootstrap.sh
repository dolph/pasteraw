#!/bin/bash
sudo apt-get update
sudo apt-get -y -V install rabbitmq-server python-setuptools screen gunicorn
cd /vagrant/
sudo python setup.py install
screen -d -m python runserver.py
