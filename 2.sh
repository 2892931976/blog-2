#!/bin/bash
set -x

bash linux_build.sh

yum install nginx -y

systemctl stop nginx
systemctl disable nginx
/usr/bin/gosuv shutdown
systemctl stop blogd
systemctl disable blogd

rm -rf /opt/blog/
 
echo y|cp tornado_ngnix.conf /etc/nginx/conf.d/tornado_ngnix.conf
sed -i -e  's/80 default_server/88 default_server/g'  /etc/nginx/nginx.conf 
 
systemctl restart nginx
systemctl enable nginx
systemctl status nginx
 
cp -r dist/blog    /opt/blog
cp -r static       /opt/blog
cp -r templates    /opt/blog
 
cp -rf blogd_8001.service /usr/lib/systemd/system/blogd.service
chmod 755 -R /usr/lib/systemd/system/blogd.service

systemctl daemon-reload
systemctl enable blogd
systemctl start  blogd    
systemctl status blogd  
 
exit 0
 
 



