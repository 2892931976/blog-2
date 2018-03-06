# coding: utf-8
from __future__ import unicode_literals
from import_file import *

from view.base.base import BaseHandler
from util.common import *
from model.models import *
from constant import *

logger = logging.getLogger(__name__)

class CommentHandler(BaseHandler):
    @tornado.gen.coroutine
    def post(self, article_id):
        comment_saved = yield self.async_do(self.add_comment, article_id)
       
        if comment_saved:
            self.redirect( self.reverse_url('article', article_id) )
        else:
            self.write_error(403)
            
    def add_comment(self, article_id):
        comment = dict(
            content=self.get_argument('content'),
            author_name=self.get_argument('author_name'),
            author_email=self.get_argument('author_email', None),
            article_id=article_id,
            comment_type=self.get_argument('comment_type', None),
            # rank=Constants.COMMENT_RANK_ADMIN if self.current_user else Constants.COMMENT_RANK_NORMAL,
            rank='normal',
            reply_to_id=self.get_argument('reply_to_id', None),
            reply_to_floor=self.get_argument('reply_to_floor', None),
        )
        
        max_floor = self.db.query(Comment).filter_by(article_id=article_id).count()
        floor = max_floor + 1
 
        try:
            comment = Comment(  content=comment['content'], 
                                author_name=comment['author_name'],
                                author_email=comment['author_email'], 
                                article_id=article_id,
                                comment_type=comment['comment_type'], 
                                rank=comment['rank'], 
                                floor=floor,
                                ipaddr=self.request.remote_ip,
                                reply_to_id=comment['reply_to_id'], 
                                reply_to_floor=comment['reply_to_floor'],
                             )
            self.db.add(comment)
            self.db.commit()
 
            return True
        except Exception as e:
            print(e)
            return False
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
 
     