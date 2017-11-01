# TecentCOSPic2Markdown
利用腾讯云（万象优图？？）作为图床，上传图片并返回markdown格式的链接。
因为腾讯SDK只支持到python2.7，所以学了点python2，不过tkinter的拖放（drag and drop/dnd）功能我就不会弄了：（，要是python3就好了。
写的不是很规范，先用起来再说。

# 使用说明
1. 安装python2环境
2. 安装qcloud_cos_v4 `pip install -U qcloud_cos_v4`
   或者按[腾讯SDK（python）的官方文档](https://github.com/tencentyun/cos-python-sdk-v4)进行操作
3. 下载主程序`COS2Markdown.py`
4. 文本打开主程序，配置一下：
   - 4.1. COS信息配置
![COS-bucket查找](http://picpool-1255373220.cossh.myqcloud.com/Blog_Hexo_CodingNet/2017-11-01_COS-bucket.png)
![COS-API查找](http://picpool-1255373220.cossh.myqcloud.com/Blog_Hexo_CodingNet/2017-11-01_COS-API.png)
   ~~~ python
        #上传前信息
        # 设置用户属性, 包括appid, secret_id和secret_key config bucket
        # 这些属性可以在cos控制台获取(https://console.qcloud.com/cos)  
        self.appid = u'...'                                        # 把...替换为用户的appid
        self.secret_id = u'...'                                    # 把...替换为用户的secret_id
        self.secret_key = u'...'                                   # 把...替换为用户的secret_key
        self.region = "shanghai"                                   # 把...替换为用户的region，目前可以为 shanghai/guangzhou
        self.bucket = u'...'                                       # 把...替换为用户的bucket
        self.remote_folder =  u'...'                               # 把...替换为用户的远程路径（如果新建了文件夹）
        self.replace_flag = 1                                      # 0表示可以覆盖？
   ~~~
   - 4.2. 启始文件夹配置
   ~~~ python
       def filePathSelect(self):
        # 定义参数
        defaultFileOpenPath = u'...'  #默认打开的文件路径            #注意win下的路径格式，eg:‘d://Share//blog//hexo//source//_img//’
        # 因为没法拖放所以用一下打开起始位置的功能：一来方便，二来可以养成本地图片保存的习惯
   ~~~
5. 保存好，用`python 路径 + COS2Markdown.py`运行即可
![Demo演示效果](http://picpool-1255373220.cossh.myqcloud.com/Blog_Hexo_CodingNet/2017-11-01_cos2md-tool.png)
# 更多
因为暂时够用（虽然是一个一个图片上传），我可能不会再继续折腾这东西，不过如果有兴趣的各位可以帮忙再贡献贡献咯。
