# coding: utf-8
from __future__ import unicode_literals
from import_file import *
 
from view.base.base import BaseHandler
from util.common import *
from model.models import *
from constant import *
from util.function import login_required

logger = logging.getLogger(__name__)

class RegisterHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        result = yield self.async_do(self.check_user) 
        # 只能注册一次用户
        if result:
            self.write("已经存在管理员用户， 无法再注册！")
        else:
            self.render('user/register.html')
 
    def check_user(self):
        if self.db.query(User).all():
            return True
        else:
            return False
            
    @tornado.gen.coroutine
    def post(self):
        result, msg = yield self.async_do(self.post_asynchronous) 
        if result:
            self.redirect(self.reverse_url('index'))
        else:
            self.redirect(self.reverse_url('register'))
 
    def post_asynchronous(self):
        email           =   self.get_argument('email')
        username        =   self.get_argument('username')
        password        =   self.get_argument('password')
        password_repeat =   self.get_argument('password_repeat')
        
        if password != password_repeat:
            msg = u'两次密码不一致'
            result = False
        else:
            if self.db.query(User).filter_by(username=username).first():
                msg = u'用户%s已经存在'%username
                result = False
            else:
                if self.register(username, password, email):
                    msg = u'用户%s注册成功！'%username
                    result = True
                    # self.session.set("user", username)
                else:
                    msg = u'用户%s注册失败！' % username
                    result = False
        return result, msg
        
    def register(self, username, password, email):
        try:
            user = User(
                username=username,
                password=PBKDF2.crypt(password),
                email=email,
            )
            self.db.add(user)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False
            
class LoginHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render("user/login.html")
 
    @tornado.gen.coroutine
    def post(self):
        username = yield self.async_do(self.post_asynchronous) 
        if username:
            self.session.set("user", username)
            # self.set_secure_cookie('user', username)
            self.redirect(self.reverse_url('index'))
        else:
            self.render("user/login.html", message="用户名或密码错误！")
 
    def post_asynchronous(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if self.check_login(username, password):
            return username
        return None
        
    def check_login(self, username, password):
        user = self.db.query(User).filter_by(username=username).first()
        if user:
            return PBKDF2.crypt(password, user.password) == user.password
        else:
            return False
            
class LogoutHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required
    def get(self):
        # self.clear_cookie("user")
        self.session.set("user", None)
        self.redirect(self.reverse_url('index'))
        
class ChangePasswordHandler(BaseHandler):
    @tornado.gen.coroutine
    @login_required
    def post(self):
        result = yield self.async_do(self.post_asynchronous) 
 
        if result:
            self.redirect(self.reverse_url('index'))
        else:
            self.write("密码修改失败！")
 
    def post_asynchronous(self):
        username = self.current_user
        old_password = self.get_argument('old_password')
        password = self.get_argument('password')
 
        if self.check_login(username, old_password):
            user = self.db.query(User).filter_by(username=username).first()
            user.password = PBKDF2.crypt(password)
            self.db.commit()
            return True
        return None
        
    def check_login(self, username, password):
        user = self.db.query(User).filter_by(username=username).first()
        if user:
            return PBKDF2.crypt(password, user.password) == user.password
        else:
            return False
        
        
        
        
        
        
        
        
        
        
        
 