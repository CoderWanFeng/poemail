# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@微信     ：CoderWanFeng : https://mp.weixin.qq.com/s/Nt8E8vC-ZsoN1McTOYbY2g
@个人网站      ：www.python-office.com
@代码日期    ：2023/12/18 23:56 
@本段代码的视频说明     ：
'''
from poemail.core.base import BaseEmail


def send_text(key, msg_from, msg_to, msg_subject='', content='', host='smtp.qq.com', port=465):
    e_server = BaseEmail(key=key,
                         msg_from=msg_from,
                         msg_to=msg_to,
                         msg_subject=msg_subject)
    e_server.send_text(content)
