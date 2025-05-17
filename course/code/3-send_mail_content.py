import os

key = os.getenv('EMAIL_KEY')
msg_from = os.getenv('EMAIL_FROM')
msg_to = os.getenv('EMAIL_TO')
msg_subject = '我是邮件主题'
msg_cc = 'ai163361ia@163.com'
content = '我是邮件正文'

import poemail

poemail.send.send_email(key=key, msg_from=msg_from, msg_to=msg_to, msg_subject=msg_subject, content=content)



