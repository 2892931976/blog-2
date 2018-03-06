# coding: utf-8
from __future__ import unicode_literals
from import_file import *

from view.upload.upload import *
 
upload_urls=[
        url(r"/upload/", UploadHandler, name="upload"),
    ]