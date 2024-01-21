# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫，微信：CoderWanFeng
@读者群     ：http://www.python4office.cn/wechat-group/
@学习网站      ：www.python-office.com
@代码日期    ：2023/12/18 23:56 
@本段代码的视频说明     ：
'''
from pocode.api.lifecycle import deprecated

from poemail.core.BaseEmail import BaseEmail
from poemail.core.SendEmail import SendEmail
from poemail.lib.Const import Mail_Type


@deprecated(version='0.0.2', demo="http://www.python4office.cn/log/2023/12/poemail/1219-email003/")
def send_text(key, msg_from, msg_to, msg_subject='', content='', host=Mail_Type['163'], port=465):
    """
    发送文本邮件

    参数:
    key (str): 邮箱验证密钥
    msg_from (str): 发件人邮箱地址
    msg_to (str): 收件人邮箱地址
    msg_subject (str, 可选): 邮件主题，默认为空字符串
    content (str, 可选): 邮件内容，默认为空字符串
    host (str, 可选): 邮件服务器地址，默认为'smtp.qq.com'
    port (int, 可选): 邮件服务器端口号，默认为465
    """
    e_server = SendEmail(key=key,
                         msg_from=msg_from,
                         msg_to=msg_to,
                         msg_subject=msg_subject)
    e_server.send_text(content)



