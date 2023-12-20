import os
import unittest
from datetime import datetime

from poemail.api.base import send_text, send_file


class TestPoEmail(unittest.TestCase):
    def test_send_text(self):
        key = os.getenv('EMAIL_KEY')
        msg_from = os.getenv('EMAIL_FROM')
        msg_to = os.getenv('EMAIL_TO')
        send_text(key=key,
                  msg_from=msg_from,
                  msg_to=msg_to,
                  msg_subject='自动发邮件',
                  content='测试邮件发送' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    def test_send_file(self):
        key = os.getenv('EMAIL_KEY')
        msg_from = os.getenv('EMAIL_FROM')
        msg_to = os.getenv('EMAIL_TO')
        send_file(key=key,
                  msg_from=msg_from,
                  msg_to=msg_to,
                  msg_subject='自动发邮件',
                  content='测试邮件发送' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                  file_path=r'./test_files/程序员晚枫.doc')
