#!/usr/bin/env bash

apt-get update
apt-get install -y git
apt-get install -y tmux
apt-get install -y apache2
apt-get install -y optipng
apt-get install -y jpegoptim
# This has jpegtran
apt-get install -y libjpeg-turbo-progs
apt-get install -y python-dev
apt-get install -y python-setuptools
apt-get install -y curl

curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py

pip install -r /vagrant/requirements.txt
pip install httpie

apt-get install -y npm

# The easiest way to get node binaries on the PATH
ln -fs /vagrant/node_modules/.bin /home/vagrant/bin

rm -rf /var/www
ln -fs /vagrant/prod_deploy /var/www
