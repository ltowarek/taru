#!/bin/sh
curl -sSL https://get.docker.com | sh
sudo systemctl enable docker
sudo usermod -aG docker pi

