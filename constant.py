# coding: utf-8
from __future__ import unicode_literals
from import_file import *
  
#
# 配置 Mysql 信息
#
MYSQL_HOST='127.0.0.1'
MYSQL_PORT='3306'
MYSQL_USERNAME='asimp'
MYSQL_PASSWORD='123456'
MYSQL_DATABASE='mydb'
#
# 配置 Redis 信息
#
REDIS_HOST='127.0.0.1'
REDIS_PORT='6379'
REDIS_PASSWORD='123456'
REDIS_DB_SESSIONS=0
#
# 配置 分页 信息
#
PAGE_NUM=10  # 每页的数据个数
#
# 配置 上传图片保存路径
#
if system()=='Windows':
    PATH = r"C:\blog_data"
else:
    PATH = r"/opt/blog_data"

UPLOAD_SERVER='127.0.0.1'    
UPLOAD_SERVER='blog.wanghaiqing.com'
UPLOAD_SERVER=requests.get("http://www.3322.org/dyndns/getip").text.strip() # 不能采用 content， 显示 http://b"101.132.164.165"/share
#
# 配置 Blog 信息
#
BLOG_TITLE='王海庆的个人博客'
BLOG_SMALL_TITLE='每天努力一点点，成功就会在眼前'
BLOG_INFO='基于Tornado实现的个人博客系统'
BLOG_COPYRIGHT='王海庆'
BLOG_ICP='蜀ICP备17009560号'
#
# 配置 Nav 信息
#
SHOW_SEARCH="TRUE"
SHOW_COLLECTION="TRUE"
SHOW_OPENSOURCE="FALSE"
SHOW_WELCOME="FALSE"
SHOW_GROUP="FALSE"
 

def get_config_value(config_path,section,option,default):
    cfg=configparser.ConfigParser()
    cfg.optionxform = str
    cfg.read(config_path )
 
    if section in cfg.sections():
        if option in cfg.options(section):
            value = cfg.get(section,option)    
            return value
    return default
    
def set_config_value(config_path,section,option,value):
    cfg=configparser.ConfigParser()
    cfg.optionxform = str    
    cfg.read(config_path )
    
    if section not in cfg.sections():
        cfg.add_section(section) 
        
    cfg.set(section,option,value)
    cfg.write(open(config_path, "w"))

if system()=='Windows':
    config_path = os.path.join(os.environ['userprofile'], 'blog.ini')
else:
    config_path = '/etc/blog.ini'
    
if os.path.exists(config_path):
    #
    # 读取 Mysql 信息
    #
    MYSQL_HOST          = get_config_value(config_path,'MYSQL','MYSQL_HOST', MYSQL_HOST)
    MYSQL_PORT          = get_config_value(config_path,'MYSQL','MYSQL_PORT', MYSQL_PORT)
    MYSQL_USERNAME      = get_config_value(config_path,'MYSQL','MYSQL_USERNAME', MYSQL_USERNAME)
    MYSQL_PASSWORD      = get_config_value(config_path,'MYSQL','MYSQL_PASSWORD', MYSQL_PASSWORD)
    MYSQL_DATABASE      = get_config_value(config_path,'MYSQL','MYSQL_DATABASE', MYSQL_DATABASE)
    #
    # 读取 Redis 信息
    #
    REDIS_HOST          = get_config_value(config_path,'REDIS','REDIS_HOST', REDIS_HOST)
    REDIS_PORT          = get_config_value(config_path,'REDIS','REDIS_PORT', REDIS_PORT)
    REDIS_PASSWORD      = get_config_value(config_path,'REDIS','REDIS_PASSWORD', REDIS_PASSWORD)
    #
    # 读取 Blog 信息
    #
    BLOG_TITLE          = get_config_value(config_path,'BLOG','BLOG_TITLE', BLOG_TITLE)
    BLOG_SMALL_TITLE    = get_config_value(config_path,'BLOG','BLOG_SMALL_TITLE', BLOG_SMALL_TITLE)
    BLOG_INFO           = get_config_value(config_path,'BLOG','BLOG_INFO', BLOG_INFO)
    BLOG_COPYRIGHT      = get_config_value(config_path,'BLOG','BLOG_COPYRIGHT', BLOG_COPYRIGHT)
    BLOG_ICP            = get_config_value(config_path,'BLOG','BLOG_ICP', BLOG_ICP)
    #
    # 读取 Nav 信息
    #
    SHOW_SEARCH         = get_config_value(config_path,'NAV','SHOW_SEARCH', SHOW_SEARCH)
    SHOW_COLLECTION     = get_config_value(config_path,'NAV','SHOW_COLLECTION', SHOW_COLLECTION)
    SHOW_OPENSOURCE     = get_config_value(config_path,'NAV','SHOW_OPENSOURCE', SHOW_OPENSOURCE)
    SHOW_WELCOME        = get_config_value(config_path,'NAV','SHOW_WELCOME', SHOW_WELCOME)
    SHOW_GROUP          = get_config_value(config_path,'NAV','SHOW_GROUP', SHOW_GROUP)
else:
    #
    # 写入 Mysql 信息
    #
    set_config_value(config_path, 'MYSQL', 'MYSQL_HOST', MYSQL_HOST)
    set_config_value(config_path, 'MYSQL', 'MYSQL_PORT', MYSQL_PORT)
    set_config_value(config_path, 'MYSQL', 'MYSQL_USERNAME', MYSQL_USERNAME)
    set_config_value(config_path, 'MYSQL', 'MYSQL_PASSWORD', MYSQL_PASSWORD)
    set_config_value(config_path, 'MYSQL', 'MYSQL_DATABASE', MYSQL_DATABASE)
    #
    # 写入 Redis 信息
    #
    set_config_value(config_path, 'REDIS', 'REDIS_HOST', REDIS_HOST)
    set_config_value(config_path, 'REDIS', 'REDIS_PORT', REDIS_PORT)
    set_config_value(config_path, 'REDIS', 'REDIS_PASSWORD', REDIS_PASSWORD)
    #
    # 写入 Blog 信息
    #
    set_config_value(config_path, 'BLOG', 'BLOG_TITLE', BLOG_TITLE)
    set_config_value(config_path, 'BLOG', 'BLOG_SMALL_TITLE', BLOG_SMALL_TITLE)
    set_config_value(config_path, 'BLOG', 'BLOG_INFO', BLOG_INFO)
    set_config_value(config_path, 'BLOG', 'BLOG_COPYRIGHT', BLOG_COPYRIGHT)
    set_config_value(config_path, 'BLOG', 'BLOG_ICP', BLOG_ICP)
    #
    # 写入 Nav 信息
    #
    set_config_value(config_path, 'NAV', 'SHOW_SEARCH', SHOW_SEARCH)
    set_config_value(config_path, 'NAV', 'SHOW_COLLECTION', SHOW_COLLECTION)
    set_config_value(config_path, 'NAV', 'SHOW_OPENSOURCE', SHOW_OPENSOURCE)
    set_config_value(config_path, 'NAV', 'SHOW_WELCOME', SHOW_WELCOME)
    set_config_value(config_path, 'NAV', 'SHOW_GROUP', SHOW_GROUP)

    
