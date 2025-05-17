import os
from datetime import datetime

import poemail

key = os.getenv('EMAIL_KEY')
msg_from = os.getenv('EMAIL_FROM')
msg_to = os.getenv('EMAIL_TO')
msg_cc = os.getenv('EMAIL_CC')

poemail.send.send_email(key=key,
                        msg_from=msg_from,
                        msg_to=msg_to,
                        msg_cc=msg_cc,
                        msg_subject='带附件的邮件' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                        content='测试邮件发送' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                        attach_files=[r'./test_files/4-send_mail_content_file/程序员晚枫.doc',
                                      r'./test_files/4-send_mail_content_file/0816.jpg'])
