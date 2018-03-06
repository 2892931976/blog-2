# coding: utf-8
from __future__ import unicode_literals
from import_file import *

from constant import *
from model.connect import engine
from model.models import *

logger = logging.getLogger(__name__)

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    # 这个并发库在python3自带;在python2需要安装sudo pip install futures
    executor = ThreadPoolExecutor(max_workers=200)

    def get_current_user(self):
        # current_user = self.get_secure_cookie('user',None) # 必须开启 xsrf_cookies
        current_user = self.session.get('user',None) # 必须开启 xsrf_cookies
        return current_user
 
    def initialize(self):
        DBSession = sessionmaker(bind=engine)
        self.db = DBSession()
        self.thread_executor = ThreadPoolExecutor(200)
        self.async_do = self.thread_executor.submit
        
        # self.redis = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), password=REDIS_PASSWORD, db=REDIS_DB_SESSIONS)
        # pool = redis.ConnectionPool(host=REDIS_HOST, port=int(REDIS_PORT), password=REDIS_PASSWORD, db=REDIS_DB_SESSIONS)  #配置连接池连接信息
        # self.redis = redis.Redis(connection_pool=pool) 
 
    @tornado.gen.coroutine
    def prepare(self):
        logger.info("请求:")
        logger.info("   remote_ip   : " + self.request.remote_ip)
        logger.info("   method      : " + self.request.method)
        logger.info("   uri         : " + self.request.uri)
        logger.info("   time        : " + time.strftime("%Y-%m-%d %H:%M:%S ",time.localtime(time.time())))
        
        yield self.async_do(self.add_pv_uv)
        self.urllib = urllib
        self.PY3 = PY3
        
        user = self.session.get('user', None)
        
        if user:
            self.current_user = user
        else:
            self.current_user = None
 
    def add_pv_uv(self):
        add_pv = 1
        add_uv = 0
        
        date = datetime.date.today()
        last_view_day = self.get_secure_cookie('uv_tag', None)
        if not last_view_day or int(last_view_day) != date.day:
            add_uv = 1
            self.set_secure_cookie('uv_tag', str(date.day), 1)
            
        blog_view = self.db.query(BlogView).get(date)
        if blog_view:
            blog_view.pv = BlogView.pv + add_pv
            blog_view.uv = BlogView.uv + add_uv
        else:
            blog_view = BlogView(date=date, pv=add_pv, uv=add_uv)
            self.db.add(blog_view)
        self.db.commit()
 
    @tornado.gen.coroutine
    def on_finish(self):
        if self.db:
            self.db.close()
   
    def write_error(self, status_code, **kwargs):
        if status_code == 403:
            self.render("403.html")
        elif status_code == 404 or 405:
            self.render("404.html")
        elif status_code == 500:
            self.render("500.html")
            
class JsonHandler(tornado.web.RequestHandler, SessionMixin):
    executor = ThreadPoolExecutor(max_workers=200)

    def get_current_user(self):
        current_user = self.session.get('user',None) # 必须开启 xsrf_cookies
        return current_user
 
    def initialize(self):
        self.request.headers['X-Xsrftoken'] = tornado.escape.to_unicode(self.xsrf_token)
                                         
        self.thread_executor = ThreadPoolExecutor(200)
        self.async_do = self.thread_executor.submit

    @tornado.gen.coroutine
    def prepare(self): 
        user = self.session.get('user', None)        
        if user:
            self.current_user = user
        else:
            self.current_user = None
  
    @tornado.gen.coroutine
    def on_finish(self):
        pass
            
    def write_json(self, object):
        object = tornado.escape.json_encode(object)
        # object = tornado.escape.json_encode(object).decode('unicode_escape')
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(object)
        raise Finish  # 确保后面的代码不会执行

    def write_success(self, data={}, message=''):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write({"status": True, "data": data, "message": message})
        raise Finish  # 确保后面的代码不会执行

    def write_fail(self, data={}, message=''):
        """ 抛出结束异常来确保代码不会继续执行 """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write({"status": False, "data": data, "message": message})
        raise Finish  # 确保后面的代码不会执行
   
 