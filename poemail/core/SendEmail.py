# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫，微信：CoderWanFeng
@读者群     ：http://www.python4office.cn/wechat-group/
@学习网站      ：https://www.python-office.com
@代码日期    ：2023/12/23 21:10 
@本段代码的视频说明     ：
'''
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from poemail.core.BaseEmail import BaseEmail
from poemail.lib.Const import Result_Type


class SendEmail(BaseEmail):

    def __init__(self, key, msg_from, msg_to, msg_subject='', host='smtp.qq.com', port=465, msg_cc=None):
        super().__init__(key, msg_from, msg_to, msg_subject, host, port)
        # 定义一个可以添加正文和附件的邮件消息对象
        self.msg = MIMEMultipart()
        # 发件人昵称和地址
        self.msg['From'] = self.msg_from
        # 收件人昵称和地址
        self.msg['To'] = self.msg_to
        # 抄送人昵称和地址
        if msg_cc:
            self.msg['Cc'] = msg_cc
        # 邮件主题
        self.msg['Subject'] = self.msg_subject

    def send_text(self, content):

        # 将文本内容添加到邮件消息对象中
        self.msg.attach(MIMEText(content, 'plain', 'utf-8'))
        # 使用服务器发送邮件
        # 判断 抄送人 是否为空，不为空则添加到抄送人列表中
        if self.msg['Cc']:
            cc_list = self.msg['Cc'].split(';')  # 将抄送人字符串拆分为列表
            msg_to = self.msg_to.split(';')
            self.server.sendmail(self.msg_from, [*msg_to, *cc_list], self.msg.as_string())
            print(f'【{self.msg_from}】给抄送人【{cc_list}】等{len(cc_list)}人发送邮件成功!')
        else:
            msg_to = self.msg_to.split(';')
            self.server.sendmail(self.msg_from, [*msg_to], self.msg.as_string())

    def send_file(self, content, files):

        # 将文本内容添加到邮件消息对象中
        self.msg.attach(MIMEText(content, 'plain', 'utf-8'))
        for file_path in files:
            file_info = Path(file_path)
            file_attach = MIMEApplication(open(str(file_info.absolute()), 'rb').read())
            file_attach["Content-Type"] = 'application/octet-stream'  # 设置内容类型
            file_attach.add_header('Content-Disposition', 'attachment', filename=str(file_info.name))  # 添加到header信息
            self.msg.attach(file_attach)
        if self.msg['Cc']:
            cc_list = self.msg['Cc'].split(';')  # 将抄送人字符串拆分为列表
            msg_to = self.msg_to.split(';')
            self.server.sendmail(self.msg_from, [*msg_to, *cc_list], self.msg.as_string())
            print(f'【{self.msg_from}】给抄送人【{cc_list}】等{len(cc_list)}人发送邮件成功!')
        else:
            msg_to = self.msg_to.split(';')
            self.server.sendmail(self.msg_from, [*msg_to], self.msg.as_string())

    def send_mail(self, content, attach_files=[]):
        print(f'【{self.msg_from}】给【{self.msg_to}】发送邮件...')
        try:
            # 根据文件参数是否为空，选择对应的方法
            if len(attach_files) > 0:
                self.send_file(content, attach_files)
            else:
                self.send_text(content)
            print(f'【{self.msg_from}】给【{self.msg_to}】发送邮件成功!')
            return Result_Type["200"]
        except Exception as error:
            print(error)
            return None
