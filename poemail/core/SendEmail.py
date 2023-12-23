# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@微信     ：CoderWanFeng : https://mp.weixin.qq.com/s/Nt8E8vC-ZsoN1McTOYbY2g
@个人网站      ：www.python-office.com
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

    def send_text(self, content):
        # 定义一个可以添加正文的邮件消息对象
        msg = MIMEMultipart()
        # 定义一个可以添加正文和附件的邮件消息对象
        msg = MIMEMultipart()
        # 发件人昵称和地址
        msg['From'] = self.msg_from
        # 收件人昵称和地址
        msg['To'] = self.msg_to
        # 抄送人昵称和地址
        # msg['Cc'] = 'xxx<xxx@qq.com>;xxx<xxx@qq.com>'
        # 邮件主题
        msg['Subject'] = self.msg_subject
        # 将文本内容添加到邮件消息对象中
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        # 使用服务器发送邮件
        self.server.sendmail(self.msg_from, [self.msg_to], msg.as_string())

    def send_file(self, content, files):
        # 定义一个可以添加正文和附件的邮件消息对象
        msg = MIMEMultipart()
        # 发件人昵称和地址
        msg['From'] = self.msg_from
        # 收件人昵称和地址
        msg['To'] = self.msg_to
        # 抄送人昵称和地址
        # msg['Cc'] = 'xxx<xxx@qq.com>;xxx<xxx@qq.com>'
        # 邮件主题
        msg['Subject'] = self.msg_subject
        # 将文本内容添加到邮件消息对象中
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        for file_path in files:
            file_info = Path(file_path)
            file_attach = MIMEApplication(open(str(file_info.absolute()), 'rb').read())
            file_attach["Content-Type"] = 'application/octet-stream'  # 设置内容类型
            file_attach.add_header('Content-Disposition', 'attachment', filename=str(file_info.name))  # 添加到header信息
            msg.attach(file_attach)
        self.server.sendmail(self.msg_from, [self.msg_to], msg.as_string())

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
