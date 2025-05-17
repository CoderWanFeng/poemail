import os

import poemail

key = os.getenv('EMAIL_KEY')
msg_from = os.getenv('EMAIL_FROM')


poemail.receive.receive_email(key=key,
                              msg_from=msg_from,
                              output_path=r'E:\poemail\tests',
                              status="UNSEEN")

