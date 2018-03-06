# coding: utf-8
from __future__ import unicode_literals
from import_file import *
 
from view.base.base import BaseHandler, JsonHandler
from util.common import *
from constant import *
from util.function import login_required

logger = logging.getLogger(__name__)

class UploadHandler(JsonHandler):
    @tornado.gen.coroutine
    @login_required
    def post(self):
        result = yield self.async_do(self.upload_file)

        if result:
            message = "上传成功"
            self.write_success(result, message)
        else:
            message = "上传失败"
            self.write_fail(result, message)
 
    def upload_file(self):
        result = []
        try:
            for file in self.request.files['file']:
                temp = {}
                body = file.body 
                filename = file.filename
                content_type = file.content_type
 
                if 'image/' in content_type:
                    content_type = 'image'
                elif 'video/' in content_type:
                    content_type = 'video'
                else:
                    content_type = 'file'
                
                uuid4 = str(uuid.uuid4())            
                time_folder=time.strftime("%Y_%m_%d",time.localtime(time.time()))            
                dir_path = os.path.join(PATH, time_folder, uuid4)
                file_path = os.path.join(PATH, time_folder, uuid4, filename)
         
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
            
                with open(file_path,'wb') as f:      
                    f.write(body)
                
                # if content_type == 'image':
                    # im = Image.open(file_path)  
                    # text_watermark(im, 'www.wanghaiqing.com', file_path) 
     
                url = 'http://%s/share/%s/%s/%s'%(UPLOAD_SERVER, time_folder, uuid4, filename)
                
                # 上传文件， 不采用http，多台机器可以分布流量，但是每台机器都需要有这个问题
                # url = '/share/%s/%s/%s'%(time_folder, uuid4, filename) 
                temp['url'] = url
                temp['filename'] = filename
                temp['content_type'] = content_type
                result.append(temp)
            return result
        except Exception as e:
            print(e)
            return result
 