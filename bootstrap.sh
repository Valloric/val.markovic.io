#!/usr/bin/env bash

apt-get update
apt-get dist-upgrade
apt-get install -yqq git
apt-get install -yqq tmux
apt-get install -yqq apache2
apt-get install -yqq optipng
apt-get install -yqq jpegoptim
# This has jpegtran
apt-get install -yqq libjpeg-turbo-progs
apt-get install -yqq python-dev
apt-get install -yqq python-setuptools
apt-get install -yqq curl

curl -O -L https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py

# PIL requires special handling, otherwise fetching fails.
pip install --allow-all-external --allow-unverified PIL -r /vagrant/requirements.txt
pip install httpie

apt-get install -yqq nodejs

# Needed so that the node binary is named 'node' and not 'nodejs'; necessary
# because of scripts that call 'node'.
apt-get install -yqq nodejs-legacy
apt-get install -yqq npm

# The easiest way to get node binaries on the PATH
mkdir -p /home/vagrant/bin

for f in /vagrant/node_modules/.bin/*; do
  ln -fs $f /home/vagrant/bin/$(basename $f)
done

if [[ ! -a /home/vagrant/s3cmd ]]
then
  git clone https://github.com/s3tools/s3cmd
  cd s3cmd
  git checkout 9ee3bdd320c82150a8d5c387dacc4d7f194cbecb
  cd ..
  sudo ln -sf /home/vagrant/s3cmd/s3cmd /home/vagrant/bin/s3cmd
fi


rm -rf /var/www/html
ln -fs /vagrant/prod_deploy /var/www/html

# Set the system timezone
echo "America/Los_Angeles" | sudo tee /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata
