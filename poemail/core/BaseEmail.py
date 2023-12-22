import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


class BaseEmail:
    def __init__(self, key, msg_from, msg_to, msg_subject='', host='smtp.qq.com', port=465):
        self.key = key  # 设置密钥
        self.msg_from = msg_from  # 设置发件人
        self.msg_to = msg_to  # 设置收件人
        self.msg_subject = msg_subject  # 设置邮件主题
        self.host = host  # 设置邮件服务器主机名
        self.port = port  # 设置邮件服务器端口号
        self.login_mail()  # 登录邮箱

    def login_mail(self):
        # 连接服务器
        self.server = smtplib.SMTP_SSL(self.host, self.port)
        # 登录邮箱
        loginResult = self.server.login(self.msg_from, self.key)
        return loginResult

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

    def send_file(self, content, file_path):
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
        file_info = Path(file_path)
        file_attach = MIMEApplication(open(str(file_info.absolute()), 'rb').read())
        file_attach["Content-Type"] = 'application/octet-stream'  # 设置内容类型
        file_attach.add_header('Content-Disposition', 'attachment', filename=str(file_info.name))  # 添加到header信息
        msg.attach(file_attach)
        self.server.sendmail(self.msg_from, [self.msg_to], msg.as_string())

    def send_mail(self, content, file_path=None):
        # 根据文件参数是否为空，选择对应的方法
        if file_path:
            self.send_file(content, file_path)
        else:
            self.send_text(content)
