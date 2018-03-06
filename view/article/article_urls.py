# coding: utf-8
from __future__ import unicode_literals
from import_file import *

from view.article.article import *
 
article_urls=[
        # RemoveArticleHandler 要放在 ArticleHandler 前面
        url(r"/article/(.+)/remove/", RemoveArticleHandler, name="remove_article"),
        url(r"/article/(.+)/", ArticleHandler, name="article"),
        
        url(r"/change_category/(.+)/", ChangeCategoryHandler, name="change_category"),
        url(r"/qrcode/(.+)/", QrcodeHandler, name="qrcode"),
    ]