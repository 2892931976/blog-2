#!/bin/bash

set -x

yum install redis -y
 
sed -i  -e  's/^bind 127.0.0.1/bind 0.0.0.0/g' /etc/redis.conf
sed -i  -e  's/^# requirepass.*/requirepass 123456/g' /etc/redis.conf
 
systemctl enable redis
systemctl start redis
systemctl status redis

chkconfig redis on
service redis start
service redis status

redis-cli -h 127.0.0.1 -p 6379 -a 123456 --version
 
 


