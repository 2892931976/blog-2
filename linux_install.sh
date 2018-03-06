#!/bin/bash
set -x
 
sed -n -e '1,/^exit 0$/!p' $0 > "packages.tar.gz" 2>/dev/null

rm -rf packages
mkdir packages

tar xzf packages.tar.gz -C packages/
 
systemctl stop nginx
systemctl disable nginx
/usr/bin/gosuv shutdown
systemctl stop blogd
systemctl disable blogd

rm -rf /opt/blog
 
cp -r packages/dist/blog    /opt/blog
cp -r packages/static       /opt/blog
cp -r packages/templates    /opt/blog
 
cp -rf packages/blogd_80.service /usr/lib/systemd/system/blogd.service
chmod 755 -R /usr/lib/systemd/system/blogd.service

systemctl daemon-reload
systemctl enable blogd
systemctl start  blogd    
systemctl status blogd  
 
rm -rf packages
 
# exit 0 下面必须有一个空行， 而且不能有任何内容
exit 0
