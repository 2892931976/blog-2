# coding: utf-8
from __future__ import unicode_literals
from import_file import *

import util.uimethods
# import util.uimodules
from url_mapping import handlers
from url_mapping import test_handlers
from constant import *

# 继承tornado.web.Application类，可以在构造函数里做站点初始化（初始数据库连接池，初始站点配置，初始异步线程池，加载站点缓存等）
class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            handlers=handlers,
            debug=False,
            autoreload=True if system()=="Windows" else False ,  # 应用程序将会观察它的源文件是否改变，并且当任何文件改变的时候便重载它自己。 
            compiled_template_cache=False,  # False html修改， 立即生效
            static_hash_cache=True, # False 静态文件哈希 (被 static_url 函数使用) 将不会被缓存。 True  不会每次都下载静态文件
            template_path="templates",
            static_path="static",
            cookie_secret=os.urandom(64),# 注释掉后， get_secure_cookie 不能用了
            xsrf_cookies=True, # 目前开启后， python3 会报错，2不会。api POST 调用失败，报错：'_xsrf' argument missing from POST. 已经解决了， tornado.escape.to_unicode(self.xsrf_token)
            ui_methods=util.uimethods,
            # ui_modules=util.uimodules,
            # ui_modules={'Hello': HelloModule},
            test='whq',
            login_url='/user/login/',
            pycket={
                'engine':'redis',
                'storage':{
                    'host':REDIS_HOST,
                    'password':REDIS_PASSWORD,
                    'port':int(REDIS_PORT),
                    'db_sessions':int(REDIS_DB_SESSIONS),
                    'db_notifications':11,
                    'max_connections':2**31,
                },
                'cookies': {
                    'expires_days': 1,
                    # 'expires': 100,
                },
            },
        )
        tornado.web.Application.__init__(self, **settings)
        
        # 域名解析里面必须添加 blog，花生壳、万网等
        # 本地的话，请在hosts里面添加域名解析
        self.add_handlers(r"^blog.*", handlers)

