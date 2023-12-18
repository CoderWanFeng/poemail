import os
import unittest

from poemail.api.base import send_text


class TestPoEmail(unittest.TestCase):
    def test_send_text(self):
        key = os.getenv('EMAIL_KEY')
        send_text(key=key,
                  msg_from='程序员晚枫@qq.com',
                  msg_to='程序员晚枫@qq.com',
                  msg_subject='自动发邮件',
                  content='测试邮件发送' + str(os.getpid()))
