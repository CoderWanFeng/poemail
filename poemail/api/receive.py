# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫，微信：CoderWanFeng
@读者群     ：http://www.python4office.cn/wechat-group/
@学习网站      ：https://www.python-office.com
@代码日期    ：2023/12/23 21:43 
@本段代码的视频说明     ：
'''
from poemail.core.ReceiveEmail import ReceiveEmail
from poemail.lib.Const import Mail_Type


def receive_email(key, msg_from, msg_to, output_path=r'./', status="UNSEEN", msg_subject='', content='',
                  host=Mail_Type['qq'], port=465):
    receive_server = ReceiveEmail(key=key,
                                  msg_from=msg_from,
                                  msg_to=msg_to,
                                  msg_subject=msg_subject,
                                  host=host,
                                  port=port, base_output_path=output_path, status=status)
    receive_server.get_email()


if __name__ == '__main__':
    # receive_email('key', '', '', '标题', '内容', host=Mail_Type['qq'], port=465)
    print(666)
    ReceiveEmail()
