# coding: utf8
from import_file import *

from constant import *

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")
 
def create_db():
    try:
        conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USERNAME, password=MYSQL_PASSWORD, port=int(MYSQL_PORT))
        cursor = conn.cursor()
        cursor.execute("create database if not exists %s default charset utf8 COLLATE utf8_general_ci;"%MYSQL_DATABASE )
        cursor.close()
    except Exception as e:
        print(e)
        
def checkout_listener(dbapi_con, con_record, con_proxy):
    try:
        try:
            logger.info('mysql listener start')
            dbapi_con.ping(False)
            logger.info('mysql listener end')
        except TypeError:
            dbapi_con.ping()
    except dbapi_con.OperationalError as exc:
        if exc.args[0] in (2006, 2013, 2014, 2045, 2055):
            raise DisconnectionError()
        else:
            raise
 
db_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE,
)
 
engine_setting=dict(
    echo=False,  # print sql
    echo_pool=False,
    # 设置7*60*60秒后回收连接池，默认-1，从不重置
    # 该参数会在每个session调用执行sql前校验当前时间与上一次连接时间间隔是否超过pool_recycle，如果超过就会重置。
    # 这里设置7小时是为了避免mysql默认会断开超过8小时未活跃过的连接，避免"MySQL server has gone away”错误
    # 如果mysql重启或断开过连接，那么依然会在第一次时报"MySQL server has gone away"，
    # 假如需要非常严格的mysql断线重连策略，可以设置心跳。
    # 心跳设置参考https://stackoverflow.com/questions/18054224/python-sqlalchemy-mysql-server-has-gone-away
    pool_recycle=7*3600,
    pool_size=20,
    max_overflow=20,
)

engine_setting = dict()
engine_setting['echo'] = False
engine_setting['echo_pool'] = False
engine_setting['pool_recycle'] = 7*3600
engine_setting['pool_size'] = 20
engine_setting['max_overflow'] = 20

print(db_url)

engine = create_engine(db_url, **engine_setting)
 
# event.listen(engine, 'checkout', checkout_listener)

# DBSession = sessionmaker(bind=engine)
# session = DBSession()

session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=True,
                                         bind=engine))
# autocommit=False 直接调用的话， 修改数据库，查询不会生效
# 但是设置为True是生效的。要是从self.session用的话， 为False也是生效的，每次都初始化

BaseModel = declarative_base()
BaseModel.query = session.query_property()

def create_tables():
    # 创建数据库表: view 下面会调用model里面的内容
    BaseModel.metadata.create_all(bind=engine)
 
    

 


