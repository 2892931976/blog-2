# coding: utf-8
from __future__ import unicode_literals

from import_file import *
  
from util.common import *
from model.models import *
from constant import *
 
def show_float(self, data, length):
    return round(data, length)
    
def show_pv_uv(self):
    day = self.db.query(BlogView).order_by(BlogView.date.desc()).first()
    return day
    
def show_articles_comments(self):
    if self.current_user:
        articles = self.db.query(Article).count()
        comments = self.db.query(Comment).count()
    else:    
        articles = self.db.query(Article).filter(Category.uuid==Article.category_id, Category.hidden==False).count()
        comments = self.db.query(Comment).filter(Comment.article_id==Article.uuid, Category.uuid==Article.category_id, Category.hidden==False).count()

    return {'articles':articles, 'comments':comments}
    
def get_menus(self):
    menus = self.db.query(Menu).all()
    return menus
    
def get_category_not_under_menu(self):
    categories = self.db.query(Category).filter_by(menu_id=None).all()
    return categories
    
def mask_ipaddr(self, ipaddr):
    if '.' in str(ipaddr):
        list = ipaddr.split('.')
        return '%s.%s.%s.xxx'%(list[0],list[1],list[2])
    else:
        return ipaddr
        
def show_today_articles_comments(self):
    today = datetime.date.today()
    if self.current_user:
        articles = self.db.query(Article).filter( Article.create_time.like("%"+str(today)+"%")).count()
        comments = self.db.query(Comment).filter( Comment.create_time.like("%"+str(today)+"%")).count()
    else:
        articles = self.db.query(Article).filter(Category.uuid==Article.category_id, Category.hidden==False).filter( Article.create_time.like("%"+str(today)+"%")).count()
        comments = self.db.query(Comment).filter(Comment.article_id==Article.uuid, Category.uuid==Article.category_id, Category.hidden==False).filter( Comment.create_time.like("%"+str(today)+"%")).count()

    return {'articles':articles, 'comments':comments}
''' 
def get_category_name(self, category_id):
    category = self.db.query(Category).filter_by(uuid=category_id).first()
    if category:
        return category.name
    
    return "未分类"
'''

def show_blog_info(self):
    data = {
        'BLOG_TITLE'        : BLOG_TITLE,
        'BLOG_SMALL_TITLE'  : BLOG_SMALL_TITLE,
        'BLOG_INFO'         : BLOG_INFO,
        'BLOG_COPYRIGHT'    : BLOG_COPYRIGHT,
        'BLOG_ICP'          : BLOG_ICP,
        'SHOW_SEARCH'       : SHOW_SEARCH,
        'SHOW_COLLECTION'   : SHOW_COLLECTION,
        'SHOW_OPENSOURCE'   : SHOW_OPENSOURCE,
        'SHOW_WELCOME'      : SHOW_WELCOME,
        'SHOW_GROUP'        : SHOW_GROUP,
    }
    return data
    
    
    
    
    
    
    
    
    
    