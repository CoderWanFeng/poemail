# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫，微信：CoderWanFeng
@读者群     ：http://www.python4office.cn/wechat-group/
@学习网站      ：https://www.python-office.com
@代码日期    ：2023/12/18 23:24 
@本段代码的视频说明     ：
'''
import time
from datetime import datetime
from pathlib import Path

from poemail.core.BaseEmail import BaseEmail

# e = BaseEmail(key='xxx',
#               msg_from='程序员晚枫@qq.com',
#               msg_to='程序员晚枫@qq.com',
#               msg_subject='自动发邮件')
# e.send_text('测试' + str(time.time()))


print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
