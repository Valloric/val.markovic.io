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
mkdir /home/vagrant/bin

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


rm -rf /var/www
ln -fs /vagrant/prod_deploy /var/www
