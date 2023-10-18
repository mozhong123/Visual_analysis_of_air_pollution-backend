#!/bin/bash
sudo su
sudo apt update

sudo apt install mysql-server
sudo /etc/init.d/mysql start
sudo mysql -u root -p
CREATE DATABASE visual_analysis_of_air_pollution;
CREATE USER 'handsome_boy'@'%' IDENTIFIED BY 'VAOAPmysql123！';
flush privileges;
exit;
sudo mysql_secure_installation
sudo systemctl restart mysql

sudo apt-get install -y redis-server
sudo vim /etc/redis/redis.conf
# 将daemonize修改为yes，将127.0.0.1改为0.0.0.0，将protect mode改为no
sudo chmod 777 /etc
sudo systemctl restart redis
redis-server --protected-mode no --daemonize yes