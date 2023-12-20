# https://geek-docs.com/python/python-ask-answer/688_python_receive_and_send_emails_in_python.html
import imaplib
import os

# 连接到IMAP服务器
imap_server = imaplib.IMAP4_SSL("imap.qq.com")

# 登录到邮箱
imap_server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PWD"))

# 选择邮箱文件夹
imap_server.select("INBOX")

# 搜索邮件
status, message_ids = imap_server.search(None, "ALL")

# 解析邮件
for message_id in message_ids[0].split():
    status, email_data = imap_server.fetch(message_id, "(RFC822)")
    # 在这里进行邮件的解析和处理
    print(status, email_data)

# 关闭连接
imap_server.close()
imap_server.logout()
