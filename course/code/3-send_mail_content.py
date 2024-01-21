# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫，微信：CoderWanFeng
@读者群     ：http://www.python4office.cn/wechat-group/
@学习网站      ：www.python-office.com
@代码日期    ：2023/12/24 1:26 
@本段代码的视频说明     ：
'''
import os

key = os.getenv('EMAIL_KEY')
msg_from = os.getenv('EMAIL_FROM')
msg_to = os.getenv('EMAIL_TO')
msg_subject = '我是邮件主题'
msg_cc = 'ai163361ia@163.com'
content = '我是邮件正文'

import poemail

poemail.send.send_email(key=key, msg_from=msg_from, msg_to=msg_to, msg_subject=msg_subject, content=content)



