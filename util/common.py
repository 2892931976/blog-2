# coding: utf8
from import_file import *
 
from model.models import * 
from constant import *
from model.models import User 
from model.connect import engine
 
logger = logging.getLogger(__name__)
 
def get_page(db, page=None, category_id=None, keyword=None, current_user=False):
    my_page_num = PAGE_NUM

    page_num = int(my_page_num)
    page = int(page)

    start = (page-1) * page_num
    end = start + page_num
 
    if keyword:
        my_query = db.query(Article).filter(or_(Article.title.like("%"+keyword+"%"), Article.content.like("%"+keyword+"%"), Article.summary.like("%"+keyword+"%"),))
        if not current_user:
            my_query = my_query.filter(Category.uuid==Article.category_id, Category.hidden==False) 
    
        if category_id:
            db_result = my_query.filter_by(category_id=category_id).order_by(desc(Article.create_time)).slice(start,end).all()
        else:
            db_result = my_query.order_by(desc(Article.create_time)).slice(start,end).all()
            
        if category_id:
            total_count = len(my_query.filter_by(category_id=category_id).all())
        else:
            total_count = len(my_query.all())
    else:   
        my_query = db.query(Article) 
        if not current_user:
            my_query = my_query.filter(Category.uuid==Article.category_id, Category.hidden==False) 
     
        if category_id:
            db_result = my_query.filter_by(category_id=category_id).order_by(desc(Article.create_time)).slice(start,end).all()
        else:
            db_result = my_query.order_by(desc(Article.create_time)).slice(start,end).all()
        if category_id:
            total_count = len(my_query.filter_by(category_id=category_id).all())
        else:
            total_count = len(my_query.all())

    
    total_page = total_count / page_num
    if total_count%page_num > 0:
        total_page += 1
 
    pages = []
   
    tmp_page = page - 1
    while tmp_page >= 1:
        if tmp_page%5 == 0:
            break
        pages.append(tmp_page)
        tmp_page -= 1

    tmp_page = page
    while tmp_page <= total_page:
        if tmp_page%5 == 0:
            pages.append(tmp_page)
            break
        else:
            pages.append(tmp_page)
            tmp_page += 1

    pages.sort()
 
    result = {
            'result':db_result,
            'pages':pages,
            'page_num':page_num,
            'c_page':page,
            't_page':int(total_page),
    }
    return result
 
def create_user():
    DBSession = sessionmaker(bind=engine)
    db = DBSession()
    
    if not db.query(User).first():
        user = User(
            email       = 'admin@163.com',
            username    = 'admin',
            password    = '123456',
        )
        
        db.add(user)
        db.commit()
 
def text_watermark(img, text, out_file="test4.jpg", angle=23, opacity=0.2):  
    #Pillow通过安装来解决 pip install Pillow 
  
    # watermark = Image.new('RGBA', img.size, (255,255,255)) #我这里有一层白色的膜，去掉(255,255,255) 这个参数就好了  
    watermark = Image.new('RGBA', img.size ) #我这里有一层白色的膜，去掉(255,255,255) 这个参数就好了  
  
    FONT = r"static/verdana.ttf"  
    size = 2  
  
    n_font = ImageFont.truetype(FONT, size)                                       #得到字体  
    n_width, n_height = n_font.getsize(text)  
    text_box = min(watermark.size[0], watermark.size[1])  
    while (n_width+n_height <  text_box):  
        size += 2  
        n_font = ImageFont.truetype(FONT, size=size)  
        n_width, n_height = n_font.getsize(text)                                   #文字逐渐放大，但是要小于图片的宽高最小值  
  
    text_width = (watermark.size[0] - n_width) / 2  
    text_height = (watermark.size[1] - n_height) / 2  
    draw = ImageDraw.Draw(watermark, 'RGBA')                                       #在水印层加画笔  
    draw.text((text_width,text_height),  
              text, font=n_font, fill="#21ACDA")  
    watermark = watermark.rotate(angle, Image.BICUBIC)  
    alpha = watermark.split()[3]  
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)  
    watermark.putalpha(alpha)  
    # Image.composite(watermark, img, watermark).save(out_file, 'JPEG') 
    Image.composite(watermark, img, watermark).save(out_file ) 
