# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫，微信：CoderWanFeng
@读者群     ：http://www.python4office.cn/wechat-group/
@学习网站      ：https://www.python-office.com
@代码日期    ：2023/12/24 1:26 
@本段代码的视频说明     ：
'''
import os

import poemail

key = os.getenv('EMAIL_KEY')
msg_from = os.getenv('EMAIL_FROM')


poemail.receive.receive_email(key=key,
                              msg_from=msg_from,
                              output_path=r'E:\poemail\tests',
                              status="UNSEEN")

