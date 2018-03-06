# coding: utf8
from import_file import *

from model.connect import session, BaseModel, engine

def generate_uuid():
    uuid4 = uuid.uuid4()
    return str(uuid4)
   
class User(BaseModel):
    __tablename__ = 'users'
    uuid        = Column(String(64), primary_key=True, nullable=False, default=generate_uuid)
    email       = Column(String(64), unique=True, index=True)
    username    = Column(String(64), unique=True, index=True)
    password    = Column(String(128))
    created_at  = Column(DateTime, default=datetime.datetime.now)
    
class Menu(BaseModel):
    __tablename__ = 'menus'
    uuid        = Column(String(64), primary_key=True, nullable=False, default=generate_uuid)
    name        = Column(String(64), unique=True)
    categories  = relationship('Category', backref='menu', lazy='dynamic')
    order       = Column(Integer, default=0 )
   
class Category(BaseModel):
    __tablename__ = 'categories'
    uuid            = Column(String(64), primary_key=True, nullable=False, default=generate_uuid)
    name            = Column(String(64), unique=True)
    introduction    = Column(Text, default=None)
    hidden          = Column(Boolean, default=False)
    articles        = relationship('Article', backref='category', lazy='dynamic')
    menu_id         = Column(String(64), ForeignKey('menus.uuid'), default=None)
 
class Article(BaseModel):
    __tablename__ = 'articles'
    uuid            = Column(String(64), primary_key=True, nullable=False, default=generate_uuid)
    title           = Column(String(64))
    content         = deferred(Column(Text))  # 延迟加载,避免在列表查询时查询该字段,我们完全不必读取这个大的字段到内存里
    summary         = Column(Text)    
    create_time     = Column(DateTime, index=True, default=datetime.datetime.now)
    update_time     = Column(DateTime, index=True, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    category_id     = Column(String(64), ForeignKey('categories.uuid'))
    comments        = relationship('Comment', backref='article', lazy='dynamic')
    
    article_view    = relationship('ArticleView' , uselist=False) # 一对一的关系
    
class Comment(BaseModel):
    __tablename__ = 'comments'
    uuid            = Column(String(64), primary_key=True, nullable=False, default=generate_uuid)
    content         = deferred(Column(Text))
    create_time     = Column(DateTime, default=datetime.datetime.now)
    author_name     = Column(String(64))
    ipaddr          = Column(String(64))
    author_email    = Column(String(64))
    article_id      = Column(String(64), ForeignKey('articles.uuid'))
    disabled        = Column(Boolean, default=False)
    floor           = Column(Integer, nullable=False)
    reply_to_id     = Column(Integer)
    reply_to_floor  = Column(String(64))
    comment_type    = Column(String(64), default='comment')
    rank            = Column(String(64), default='normal')

class ArticleView(BaseModel):
    __tablename__ = 'article_view'
    uuid            = Column(String(64), primary_key=True, nullable=False, default=generate_uuid)
    article_id      = Column(String(64), ForeignKey('articles.uuid'))
    num_of_view     = Column(Integer, default=0)
    article         = relationship('Article') # 一对一的关系
    
class BlogView(BaseModel):
    __tablename__ = 'blog_view'
    date = Column(DATE, primary_key=True)
    pv = Column(BigInteger, default=0)
    uv = Column(BigInteger, default=0)