#!/bin/sh
set -e

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y wget
wget -O mosquitto-repo.gpg.key http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
sudo apt-key add mosquitto-repo.gpg.key
rm mosquitto-repo.gpg.key
sudo wget -O /etc/apt/sources.list.d/mosquitto-stretch.list http://repo.mosquitto.org/debian/mosquitto-stretch.list
sudo apt-get update
sudo apt-get install -y mosquitto
sudo systemctl disable mosquitto

sudo apt-get install -y python3 python3-pip python3-virtualenv
python3 -m virtualenv -p python3 venv

