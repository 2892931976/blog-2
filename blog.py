# coding: utf-8
from __future__ import unicode_literals
from import_file import *

# for pyinstaller 
if hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)
 
logger = logging.getLogger(__name__)
from util import log_config
log_config.init( )  # 必须放在app初始化的前面， 否则别的模块识别不到
 
from application import Application
from model.connect import create_db,create_tables 

define("port", default=80, help="run on the given port", type=int)
 
if __name__=='__main__':  
    tornado.options.parse_command_line()
   
    tornado_app = Application()     
    http_server = tornado.httpserver.HTTPServer(
        request_callback=tornado_app,
        xheaders=True,# 采用反向代理时，获取正确的ip，nginx里面也需要设置。此功能暂未验证。
        max_buffer_size=6 * 1024 * 1024 * 1024,   #6G Size file upload, default 100M
    )
 
    http_server.bind(options.port, "0.0.0.0")    
    http_server.start(num_processes=1 if system()=="Windows" else 0) 
    
    create_db()
    create_tables()
 
    server = tornado.ioloop.IOLoop.instance()
    print('service start running on 0.0.0.0:{0}'.format(options.port))
    server.start()
 

 
 