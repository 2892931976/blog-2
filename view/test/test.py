# coding: utf-8
from __future__ import unicode_literals
from import_file import *
 
from view.base.base import BaseHandler
from util.common import *
from model.models import *
from constant import *

logger = logging.getLogger(__name__)

class TestHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        # self.write(r'<a href="http://blog.wanghaiqing.com/">点击我进入博客</a>')
        self.render('test.html')
 