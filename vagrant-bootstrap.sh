#!/bin/bash
sudo apt-get update
sudo apt-get -y -V install python-setuptools screen
cd /vagrant/
sudo python setup.py install
screen -d -m python runserver.py
