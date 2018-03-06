# coding: utf-8
from __future__ import unicode_literals
from import_file import *
 
from view.base.base import BaseHandler
from util.common import *
from model.models import *
from constant import *
from util.function import login_required

logger = logging.getLogger(__name__)

class ArticleHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self, article_id):
        result = yield self.async_do(self.get_article_detail, article_id)
       
        if result:
            self.render("article_detials.html", **result )
        else:
            self.write("获取文章失败")
            
    def get_article_detail(self, article_id):
        data = self.db.query(Article).filter_by(uuid=article_id).first()
 
        if data.article_view:
            data.article_view.num_of_view = data.article_view.num_of_view + 1
        else:
            article_view = ArticleView(
                                article_id=article_id,
                                num_of_view=1,
                            )
            data.article_view = article_view
            
        self.db.commit()
        categories = self.db.query(Category).all()
 
        result = {
            'article':data,
            'categories':categories,
            'category_id':data.category_id,
        }
        return result
        
class RemoveArticleHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required
    def get(self, article_id):
        result = yield self.async_do(self.remove_article, article_id)
       
        if result:
            self.redirect(self.reverse_url('index'))
        else:
            self.write("删除文章失败")
            
    def remove_article(self, article_id):
        try:
            article = self.db.query(Article).filter_by(uuid=article_id).first()
            if article:
                # comments = db_session.query(Comment).filter(Comment.article_id == article_id).all()
                self.db.query(Comment).filter(Comment.article_id == article_id).delete()
                self.db.commit()  
                
                self.db.delete(article)
                self.db.commit()
            return True
        except Exception as e:
            print(e)
            return None
        
        
        self.db.query(Article).filter_by(uuid=article_id).delete()
        self.db.commit()
        return True
        
class ChangeCategoryHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required
    def post(self, article_id):
        result = yield self.async_do(self.change_category, article_id)
       
        if result:
            self.redirect(self.reverse_url('article', article_id))
        else:
            self.write("修改分类失败")
            
    def change_category(self, article_id):
        category_id = self.get_argument("category_id",None)
        article = self.db.query(Article).filter_by(uuid=article_id).first()
        article.category_id = category_id
        self.db.commit()
 
        return True
        
class QrcodeHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self, article_id):
        img_data = yield self.async_do(self.generate_qrcode, article_id)
        self.write(img_data.getvalue())
            
    def generate_qrcode(self, article_id):
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,#ERROR_CORRECT_L: 7%的字码可被容错
            box_size=10,#参数 box_size 表示二维码里每个格子的像素大小
            border=4,#参数 border 表示边框的格子厚度是多少（默认是4）
        )
 
        url = self.reverse_url('article', article_id)
        url = "%s://%s%s"%(self.request.protocol, self.request.host, url)
 
        qr.add_data( url )
        qr.make(fit=True)
        img = qr.make_image()
        img_data = StringIO()

        img.save(img_data)
        return img_data # 返回二维码的图片句柄
         
 
     