# coding: utf-8
from __future__ import unicode_literals
from import_file import *

from view.index.index import *
 
index_urls=[
        url(r"/", IndexHandler, name="index"),
        url(r"/page/(.+)/", IndexHandler, name="index_list"),
        
        url(r"/create_category/", CreateCategoryHandler, name="create_category"),
        url(r"/create_menu/", CreateMenuHandler, name="create_menu"),
    ]