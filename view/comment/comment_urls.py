# coding: utf-8
from __future__ import unicode_literals
from import_file import *

from view.comment.comment import *
 
comment_urls=[
        url(r"/comment/(.+)/comment/", CommentHandler, name="article_comment"),
    ]