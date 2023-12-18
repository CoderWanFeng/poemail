import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class BaseEmail:
    def __init__(self, key, msg_from, msg_to, msg_subject='', host='smtp.qq.com', port=465):
        self.key = key
        self.msg_from = msg_from
        self.msg_to = msg_to
        self.msg_subject = msg_subject
        self.host = host
        self.port = port
        self.login_mail()

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
        # msg['To'] = '晚枫1号<程序员晚枫@qq.com>;xxx<xxx@qq.com>'
        # 抄送人昵称和地址
        # msg['Cc'] = 'xxx<xxx@qq.com>;xxx<xxx@qq.com>'
        # 邮件主题
        msg['Subject'] = self.msg_subject
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        self.server.sendmail(self.msg_from, [self.msg_to], msg.as_string())
