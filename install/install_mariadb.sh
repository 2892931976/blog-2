#!/bin/bash

set -x

install_mysql () {
    yum remove  mariadb mariadb-server -y
    rm -rf /var/lib/mysql 
    rm -rf /etc/rc.d/init.d/mysql
    rm -rf /etc/my.cnf
    rm -rf /var/run/yum.pid

    yum install mariadb mariadb-server -y    
    systemctl start mariadb.service    
    systemctl enable mariadb.service     
    systemctl status  mariadb.service 
     
    mysql -e "create   database asimp_db;"
    mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'asimp'@'%' identified by '123456';"
    mysql -e "flush privileges; "
    mysql -e "use mysql;select host ,user from user;"
    
    
# mysql_secure_installation

# echo -e "\nn\ny\nn\ny\ny\n" | mysql_secure_installation

mysql_secure_installation <<EOF

n
y
n
y
y
EOF

}

install_mysql

 
