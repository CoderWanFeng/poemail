# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫，微信：CoderWanFeng
@读者群     ：http://www.python4office.cn/wechat-group/
@学习网站      ：www.python-office.com
@代码日期    ：2023/12/18 23:56 
@本段代码的视频说明     ：
'''

from poemail.core.SendEmail import SendEmail
from poemail.lib.Const import Mail_Type


def send_text(key, msg_from, msg_to, msg_subject='', content='', host='smtp.qq.com', port=465):
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


def send_email(key, msg_from, msg_to, msg_cc=None, attach_files=[], msg_subject='', content='', host=Mail_Type['qq'],
               port=465):
    """
    发送邮件函数

    参数:
    key (str): 邮箱账户密钥
    msg_from (str): 发件人邮箱地址
    msg_to (str): 收件人邮箱地址
    file_path (str, 可选): 邮件附件路径，默认为None
    msg_subject (str, 可选): 邮件主题，默认为空字符串
    content (str, 可选): 邮件内容，默认为空字符串
    host (str, 可选): 邮箱服务器地址，默认为'qq'
    port (int, 可选): 邮箱服务器端口号，默认为465

    返回:
    无

    """
    e_server = SendEmail(key=key,
                         msg_from=msg_from,
                         msg_to=msg_to,
                         msg_cc=msg_cc,
                         msg_subject=msg_subject,
                         host=host,
                         port=port)
    res = e_server.send_mail(content, attach_files)
