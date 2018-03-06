#!/bin/bash

rm -rf /opt/python3

# 没有会报错 zipimport.ZipImportError: can't decompress data; zlib not available
yum -y install zlib* 
yum -y install sqlite-devel  # 解决 sqlachemy sqlite 报错的问题：ModuleNotFoundError: No module named 'pysqlite2'
yum -y install python-devel  # 暂时无用
yum -y install openssl-devel # 不安装的话， https加密会报错 AssertionError: Python 2.6+ and OpenSSL required for SSL

rm -rf Python-3.6.4.tgz
# wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
wget http://172.19.105.177:2133/job/aim/Python-3.6.4.tgz

tar -xzf Python-3.6.4.tgz 

cd Python-3.6.4
# 不加 --enable-shared ， 编译不会报错。ldd里面还没有libpython3.6m.so.1.0关联信息。但是打包会报错。
# 安装多个python27的版本，如果不开启enable-shared，指定不同路径即可。
# 当开启enable-shared时，默认只有一个版本的python
./configure --prefix=/opt/python3  --enable-shared

make && make install
 
# 不加下面变量的话，打包会失败 libpython3.6m.so.1.0 => not found
# /opt/python3/bin/python3.6: error while loading shared libraries: libpython3.6m.so.1.0: cannot open shared object
echo export LD_LIBRARY_PATH=/opt/python3/lib >> /root/.bashrc
source /root/.bashrc

# ldd查看关联的库
ldd /opt/python3/bin/python3  

# 安装常用的库
export LD_LIBRARY_PATH=/opt/python3/lib 
cd ..
/opt/python3/bin/pip3 install -r requirements.txt  
/opt/python3/bin/pip3 install -r ../requirements.txt  

# 安装git
yum install git unzip -y

# 下载pyinstaller， 必须采用最新的。centos6 否则会无法产生临时目录。
# git clone --progress -v https://github.com/pyinstaller/pyinstaller 
rm -rf pyinstaller
wget http://172.19.105.177:2133/job/aim/pyinstaller.zip
unzip pyinstaller.zip

# 安装pyinstaller
cd pyinstaller 
/opt/python3/bin/python3 setup.py build
/opt/python3/bin/python3 setup.py install
cd ..

# 创建软连接
ln -s /opt/python3/bin/python3 /usr/bin/python3
ln -s /opt/python3/bin/pip3 /usr/bin/pip3
ln -s /opt/python3/bin/pyinstaller /usr/bin/pyinstaller3

 









