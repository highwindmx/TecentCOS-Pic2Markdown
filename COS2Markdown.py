#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import os
from datetime import date
import Tkinter as tk # Tkinter is for python2, tkinter is for python3
import tkFileDialog as tfd
from qcloud_cos import CosClient # 记得预装一个下库文件
from qcloud_cos import UploadFileRequest

class Application(tk.Tk): 
    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        self.grid()       
        button_width = 16 #设置按钮宽度
        entry_small_width = 20
        entry_big_width = 60
        
# 0     #选择本地文件 
        buttonSelect = tk.Button(self, text=u'选择图片文件', command=self.filePathSelect, width=button_width)
        buttonSelect.grid(row=0, column=0, sticky='w')
        #显示本地文件名称
        self.entryLocalNameVar = tk.StringVar()
        self.entryLocalName = tk.Entry(self, textvariable=self.entryLocalNameVar, width=entry_small_width)
        self.entryLocalName.grid(row=0, column=1, sticky='w')
        #显示本地文件路径
        self.entryLocalPathVar = tk.StringVar()
        self.entryLocalPath = tk.Entry(self, textvariable=self.entryLocalPathVar, width=entry_big_width-entry_small_width)
        self.entryLocalPath.grid(row=0, column=2, sticky='e')
        
# 1     #文件重命名
        buttonRemoteRename = tk.Button(self, text=u'点击重命名', command=self.on_button_rename, width=button_width) # 按键后才会执行
        buttonRemoteRename.grid(row=1, column=0, sticky='w')
        #重写文件名
        self.entryRemoteRenameVar = tk.StringVar()
        self.entryRemoteRename = tk.Entry(self, textvariable=self.entryRemoteRenameVar, width=entry_small_width)        
        self.entryRemoteRename.bind("<Return>", self.on_return_rename) # 回车后才会执行
        self.entryRemoteRename.grid(row=1, column=1, sticky='e')        
        #生成新文件名
        self.Rename2Var =tk.StringVar()
        self.labelRemoteRenameVar =tk.StringVar()
        self.labelRemoteRename = tk.Label(self, textvariable=self.labelRemoteRenameVar)
        self.labelRemoteRename.grid(row=1, column=2, sticky='w') 
        
# 2     #上传前信息
        # 设置用户属性, 包括appid, secret_id和secret_key config bucket
        # 这些属性可以在cos控制台获取(https://console.qcloud.com/cos)  # ？？ 可以做成字典
        self.appid = 125...                                        # 把125...替换为用户的appid
        self.secret_id = u'...'                                    # 把...替换为用户的secret_id
        self.secret_key = u'...'                                   # 把...替换为用户的secret_key
        self.region = "shanghai"                                   # 把...替换为用户的region，目前可以为 shanghai/guangzhou
        self.bucket = u'...'                                       # 把...替换为用户的bucket
        self.remote_folder =  u'...'                               # 把...替换为用户的远程路径（如果新建了文件夹）
        self.replace_flag = 1                                      # 0表示可以覆盖？
        
        self.labelUploadInfoVar =tk.StringVar()
        self.labelUploadInfo = tk.Label(self, textvariable=self.labelUploadInfoVar)
        self.labelUploadInfo.grid(row=2, column=0, columnspan=3)
        self.labelUploadInfoVar.set(u'COS信息概览：[bucket：' + self.bucket + u']   [远程文件夹：' + self.remote_folder + ']')
                
# 3     #上传文件按钮
        buttonUpload = tk.Button(self, text=u'点击上传至腾讯云', command=self.upload_file_2_COS, width=button_width+entry_big_width)
        buttonUpload.grid(row=3, column=0, columnspan=3)
        
# 4     #上传状态
        self.labelUploadStatueVar =tk.StringVar()
        self.labelUploadStatue = tk.Label(self, textvariable=self.labelUploadStatueVar)
        self.labelUploadStatue.grid(row=4, column=0, columnspan=3)
        self.labelUploadStatueVar.set(u'如果点击上传无反应，试试重命名后再上传(默认不覆盖已有文件)')           
        
# 5     #复制MD格式链接
        buttonCopyMd = tk.Button(self, text=u'点击拷贝MD格式', command=self.OnButtonCopyMdClick, width=button_width)
        buttonCopyMd.grid(row=5, column=0, sticky='w')
        self.entryMdUrlVar = tk.StringVar()
        self.entryMdUrl = tk.Entry(self, textvariable=self.entryMdUrlVar, width=entry_big_width)
        self.entryMdUrl.grid(row=5, column=1, columnspan=2, sticky='w')

# 6     #复制HTML格式链接   
        buttonCopyHTML = tk.Button(self, text=u'点击拷贝HTML格式', command=self.OnButtonCopyHtmlClick, width=button_width)
        buttonCopyHTML.grid(row=6, column=0, sticky='w')
        self.entryHtmlUrlVar = tk.StringVar()
        self.entryHtmlUrl = tk.Entry(self, textvariable=self.entryHtmlUrlVar, width=entry_big_width)
        self.entryHtmlUrl.grid(row=6, column=1, columnspan=2, sticky='w')
        
        #程序格式处理
        self.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)
        self.update()
        self.geometry(self.geometry())
    
    def remote_rename(self):
        local_pic_name = self.entryLocalNameVar.get()
        now = date.today()
        remote_pic_name_prefix = str(now) + u'_'
        remote_pic_new_name = self.entryRemoteRenameVar.get()
        remote_file_name = remote_pic_name_prefix  + remote_pic_new_name
        self.Rename2Var.set(remote_file_name)
        self.labelRemoteRenameVar.set(u'将更名为：' + remote_file_name)
        
    def on_button_rename(self):
        self.remote_rename()
        # print 'button clicked'        
        
    def on_return_rename(self, event):
        self.remote_rename()
        # print 'return pressed'
   
    def filePathSelect(self):
        # 定义参数
        defaultFileOpenPath = u'...'  # 设置默认打开的文件路径
        localFilePath = tfd.askopenfilename(initialdir=defaultFileOpenPath)
        localFileName = os.path.basename(localFilePath)
        # 返回显示值
        self.entryLocalPathVar.set(localFilePath) 
        self.entryLocalNameVar.set(localFileName)           
        self.entryRemoteRenameVar.set(localFileName)
        self.on_button_rename()
        # print 'file selected'
        
    def OnButtonCopyMdClick(self):
        self.clipboard_clear()
        self.clipboard_append(self.entryMdUrlVar.get())
        
    def OnButtonCopyHtmlClick(self): 
        self.clipboard_clear()
        self.clipboard_append(self.entryHtmlUrlVar.get())
           
    def upload_file_2_COS(self):      
        cos_client = CosClient(self.appid, self.secret_id, self.secret_key, self.region)

        try:
            local_pic_path = self.entryLocalPathVar.get()
            local_pic_name = os.path.basename(local_pic_path)
            if local_pic_name != '':  # ？？ 判断本地图片是否存在，不过应该有其他更好的判断方法吧                           
                # 设置远程图片路径
                remote_pic_path = self.remote_folder + self.Rename2Var.get()
                # print remote_pic_path #debug用
                
                # 上传文件
                request = UploadFileRequest(self.bucket, remote_pic_path, local_pic_path)
                request.set_insert_only(self.replace_flag)
                upload_file_ret = cos_client.upload_file(request)
                # 得到Url
                upload_url = upload_file_ret['data']['source_url']
                md_url = '![...]' + '(' + upload_url + ')'
                html_url = '<img src="' + upload_url + '" alt="..." style="width: 85%;"/>'
                # debug用
                # print u'*****************0**********************'
                # print upload_file_ret
                # print upload_file_ret['message']
                # print upload_url
                # print md_url
                # print html_url
                # print u'*****************1**********************'
                
                #窗口返回赋值
                self.labelUploadStatueVar.set(upload_file_ret['message']) #返回是否上传成功的提示
                self.entryMdUrlVar.set(md_url)
                self.entryHtmlUrlVar.set(html_url)
            else:
                print 'local Picture Name Incorrect!'
        except:
            pass
            
if __name__ == '__main__':
    app = Application(None)
    app.title('腾讯云图库上传生成Markdown链接格式')
    app.mainloop()
