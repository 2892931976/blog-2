# coding: utf-8
from __future__ import unicode_literals
from import_file import *

from view.cms.cms import *
 
cms_urls=[
        url(r"/cms/", CMSHandler, name="cms"),
        url(r"/cms/article/submit/", ArticleSubmitHandler, name="article_submit"),
        url(r"/cms/article/(.+)/update/", ArticleUpdateHandler, name="article_update"),
    ]