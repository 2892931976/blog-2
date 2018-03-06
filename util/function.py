#coding=utf-8
from import_file import *

from model.models import *

def not_user_exists(self, User):
	if self.db.query(User).first():
		return False
	else:
		return True

def register_required(func):
	@wraps(func)
	def wrapper(self, *args, **kwargs):
		if not_user_exists(self, User):
			# 没有用户，就让跳到注册页面
			self.redirect(self.reverse_url('register'))
			return
		# 执行post方法或get方法
		return func(self, *args, **kwargs)
	return wrapper

def login_required(func):
	@wraps(func)
	def wrapper(self, *args, **kwargs):
		# if not self.get_secure_cookie('user'):
		if not self.session.get('user', None):
			# 没有登录，就跳到登录页面
			self.redirect(self.reverse_url('login'))
			return
		# 执行post方法或get方法
		return func(self, *args, **kwargs)
	return wrapper