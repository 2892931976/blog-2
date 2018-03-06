# coding: utf-8
from __future__ import unicode_literals
from import_file import *

from view.user.user import *
 
user_urls=[
        url(r"/user/register/", RegisterHandler, name="register"),
        url(r"/user/login/", LoginHandler, name="login"),
        url(r"/user/logout/", LogoutHandler, name="logout"),
        url(r"/user/change_password/", ChangePasswordHandler, name="change_password"),
    ]