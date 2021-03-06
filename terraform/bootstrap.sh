#!/bin/sh

# Install and start Docker
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo usermod -aG docker ec2-user

# Install docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/bin/docker-compose
sudo chmod +x /usr/bin/docker-compose

# Install repo
git clone https://github.com/bingyangli/load-test.git
