# coding: utf-8
from __future__ import unicode_literals
from import_file import *

from view.test.test import *
 
test_urls=[
        url(r"/", TestHandler, name="test"),
    ]