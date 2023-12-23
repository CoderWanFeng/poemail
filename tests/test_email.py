import os
import unittest
from datetime import datetime

from poemail.api.receive import receive_email
from poemail.api.send import *

key = os.getenv('EMAIL_KEY')
msg_from = os.getenv('EMAIL_FROM')
msg_to = os.getenv('EMAIL_TO')


class TestPoEmail(unittest.TestCase):
    def test_send_text(self):
        send_email(key=key,
                   msg_from=msg_from,
                   msg_to=msg_to,
                   msg_subject='自动发邮件' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                   content='测试邮件发送' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def test_send_file(self):
        send_email(key=key,
                   msg_from=msg_from,
                   msg_to=msg_to,
                   msg_subject='自动发邮件',
                   content='测试邮件发送' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                   file_path=r'./test_files/程序员晚枫.doc')

    def test_receive_mail(self):
        receive_email(key=key,
                      msg_from=msg_from,
                      msg_to=msg_to,
                      output_path=r'./test_files/get_email', status="ALL")
