# coding: utf-8
from __future__ import unicode_literals
from import_file import *
 
from view.base.base import BaseHandler
from util.common import *
from model.models import *
from constant import *
from util.function import login_required

logger = logging.getLogger(__name__)

class CMSHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required
    def get(self): 
        self.render('cms/cms_base.html')
 
class ArticleSubmitHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required
    def get(self): 
        data = yield self.async_do(self.get_article_submit)
        self.render('cms/submit_articles.html', **data)
 
    def get_article_submit(self):
        categories = self.db.query(Category).all()
        data = {
            'title':None,
            'content':None,
            'summary':None,
            'categories':categories,
            'article_id':None,
            'category_id':None,
            'entry_title':"发表文章",
        }    
        return data
        
    @tornado.gen.coroutine
    @login_required
    def post(self): 
        article_saved = yield self.async_do(self.article_submit)
        if article_saved:
            self.write( str(article_saved.uuid) ) # ajax 方式 ， 提交数据， 返回 文章id， 供跳转使用
            #self.redirect( self.reverse_url('article', article_saved.uuid) )# 表单提交方式 ， 有上传图片bug， 图片下面必须回车才能显示。
        else:
            self.write("文章提交失败！")
 
    def article_submit(self):
        try:
            title=self.get_argument("title") 
            category_id=self.get_argument("category_id", None) 
            content=self.get_argument("content") 
            summary=self.get_argument("summary")  
 
            article_to_add = Article(title=title if title else "Ta很懒什么也没留下",
                                    content=content,
                                    summary=summary if summary else "Ta很懒什么也没留下", 
                                    category_id=category_id if category_id else None,
                                    )
            self.db.add(article_to_add)
            self.db.commit()
            
            return article_to_add
        except Exception as e:
            print(e)
            return None
        
class ArticleUpdateHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required
    def get(self, article_id): 
        # article_id = int(article_id)
        data = yield self.async_do(self.get_article_update, article_id)
        self.render('cms/submit_articles.html', **data)
 
    def get_article_update(self, article_id):
        article = self.db.query(Article).filter_by(uuid=article_id).first()
        categories = self.db.query(Category).all()
        data = {
            'title':article.title,
            'content':article.content,
            'summary':article.summary,
            'categories':categories,
            'article_id':article_id,
            'category_id':article.category_id,
            'entry_title':"编辑文章",
        }    
        return data
        
    @tornado.gen.coroutine
    @login_required
    def post(self, article_id): 
        article_id = yield self.async_do(self.article_submit , article_id)
        if article_id:
           
            self.write( str(article_id) ) # ajax 方式 ， 提交数据， 返回 文章id， 供跳转使用
            # self.redirect( self.reverse_url('article', article_id) )
        else:
            self.write("文章更新失败！")
 
    def article_submit(self, article_id):
        try:
            title=self.get_argument("title") 
            category_id=self.get_argument("category_id", None) 
            content=self.get_argument("content") 
            summary=self.get_argument("summary") 

            article = self.db.query(Article).filter_by(uuid=article_id).first()
            article.title = title
            article.content = content
            article.summary = summary if summary else "作者很懒，没有填写概要信息", 
            article.category_id = category_id
 
            self.db.commit()
            
            return article_id
        except Exception as e:
            print(e)
            return None
     