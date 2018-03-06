# coding: utf-8
from __future__ import unicode_literals
from import_file import *
 
from view.base.base import BaseHandler
from util.common import *
from model.models import *
from constant import *
from util.function import register_required, login_required
 
logger = logging.getLogger(__name__)

if not PY3: # 添加这几行解决 搜索关键字包含中文时， page.html里面 urllib.urlencode(dict(keyword=keyword)) 报错的 bug
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

class IndexHandler(BaseHandler):
    @tornado.gen.coroutine
    # @register_required  # 开启之后， 并发就卡死
    def get(self, page=1):
        data = yield self.async_do(self.get_articles, page) 
        self.render('index.html', **data)
 
    def get_articles(self, page):
        category_id = self.get_argument("category_id",None)
        keyword = self.get_argument("keyword",None)
        current_user = True if self.current_user else False
        articles  = get_page(self.db, page, category_id, keyword, current_user)
        if category_id:
            category_name = self.db.query(Category).filter_by(uuid=category_id).first().name
        else:
            category_name = "首页"
        data = {
            'result':articles ,
            'category_id':category_id ,
            'keyword':keyword ,
            'category_name':category_name ,
        }
 
        return data
        
class CreateCategoryHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required   
    def post(self):
        data = yield self.async_do(self.create_category) 
        self.redirect(self.reverse_url('index'))
 
    def create_category(self):
        category_name = self.get_argument("category_name",None)
        menu_id = self.get_argument("menu_id",None)
        category = Category(
            name=category_name,
            introduction="",
            hidden=False,
            menu_id=menu_id if menu_id else None,
        )
        
        self.db.add(category)
        self.db.commit()
        
        return True
     
class CreateMenuHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required   
    def post(self):
        data = yield self.async_do(self.create_menu) 
        self.redirect(self.reverse_url('index'))
 
    def create_menu(self):
        menu_name = self.get_argument("menu_name",None)
        menu = Menu(
            name=menu_name,
        )
        
        self.db.add(menu)
        self.db.commit()
        
        return True