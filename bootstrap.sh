#!/usr/bin/env bash

apt-get update
apt-get dist-upgrade
apt-get install -yqq git
apt-get install -yqq tmux
apt-get install -yqq apache2
apt-get install -yqq optipng
apt-get install -yqq jpegoptim
# This has jpegtran
apt-get install -yqq libjpeg-progs
apt-get install -yqq python2-dev
apt-get install -yqq python-setuptools
apt-get install -yqq curl
apt-get install -yqq python-pip

pip2 install -r /vagrant/requirements.txt
pip2 install httpie

apt-get install -yqq nodejs
apt-get install -yqq npm

npm install uglify-js -g
npm install less -g

# The easiest way to get node binaries on the PATH
mkdir -p /home/vagrant/bin

for f in /vagrant/node_modules/.bin/*; do
  ln -fs $f /home/vagrant/bin/$(basename $f)
done

if [[ ! -a /home/vagrant/s3cmd ]]
then
  git clone https://github.com/s3tools/s3cmd
  cd s3cmd
  git checkout 6107af0a4dddfe21c556c64551153e7774db287f
  cd ..
  sudo ln -sf /home/vagrant/s3cmd/s3cmd /home/vagrant/bin/s3cmd
fi


rm -rf /var/www/html
ln -fs /vagrant/prod_deploy /var/www/html

# Set the system timezone
echo "America/Los_Angeles" | sudo tee /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata
