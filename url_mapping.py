# coding: utf-8
from __future__ import unicode_literals
from import_file import *

from view.test.test_urls import test_urls
from view.user.user_urls import user_urls
from view.index.index_urls import index_urls
from view.article.article_urls import article_urls
from view.comment.comment_urls import comment_urls
from view.cms.cms_urls import cms_urls
from view.upload.upload_urls import upload_urls

from constant import *

test_handlers=[
                (re.escape('/share/') + r"(.*)", StaticFileHandler, {"path": PATH}),
              ]
test_handlers += test_urls





handlers=[
                (re.escape('/share/') + r"(.*)", StaticFileHandler, {"path": PATH}),
         ]
handlers += user_urls
handlers += index_urls
handlers += comment_urls
handlers += cms_urls # article_urls 需要放在 cms_urls 后面
handlers += article_urls
handlers += upload_urls
 