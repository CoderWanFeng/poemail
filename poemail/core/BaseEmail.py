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
