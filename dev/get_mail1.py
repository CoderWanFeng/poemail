# https://geek-docs.com/python/python-ask-answer/688_python_receive_and_send_emails_in_python.html
# https://blog.51cto.com/u_16213436/7489927
# https://www.php.cn/faq/586358.html
import email
import imaplib
import os
from email.header import decode_header


def save_attachment(part):
    filename = part.get_filename()
    if filename:
        print('Downloading attachment:', filename)
        attach_data = part.get_payload(decode=True)
        with open(filename, 'wb') as f:
            f.write(attach_data)


# 连接到IMAP服务器
imap_server = imaplib.IMAP4_SSL("imap.qq.com")

qq_mail = os.getenv("EMAIL_FROM")
qq_key = os.getenv("EMAIL_KEY")

# 登录到邮箱
imap_server.login(qq_mail, qq_key)

# 选择邮箱文件夹
imap_server.select("INBOX")

# 搜索邮件
# status, message_ids = imap_server.search(None, "ALL")

# 解析邮件
# for message_id in message_ids[0].split():
#     status, email_data = imap_server.fetch(message_id, "(RFC822)")
#     # 在这里进行邮件的解析和处理
#     print(status, email_data)

# 接收所有未读邮件，参数'UNSEEN'控制
# status, data = imap_server.search(None, 'UNSEEN')
status, data = imap_server.search(None, 'ALL')
unread_msg_nums = data[0].split()

# 使用imap.fetch获取邮件内容，然后用email模块的message_from_bytes解析邮件，
# 遍历邮件中的每个部分，看是否有filename字段，如果有就表示这是一个附件，然后获取附件内容并写入文件。
for num in unread_msg_nums:
    # RFC822 代表接受邮件的全部内容，包括标题、正文和附件
    status, data = imap_server.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    subj = decode_header(msg["Subject"])[0][0]
    from_email = decode_header(msg["From"])[0][0]
    to_email = decode_header(msg["To"])[0][0]
    mail_type=msg.get_content_maintype()
    if mail_type == 'multipart':
        for part in msg.walk():
            content_type = part.get_content_type()
            if 'application' in content_type:
                save_attachment(part)
        # if part.get('Content-Disposition') is None:
        #     continue
        #
        # filename = part.get_filename()
        # if bool(filename):
        #     print('Downloading attachment:', filename)
        #     attach_data = part.get_payload(decode=True)
        #     # 注意：文件用双反斜杠链接
        #     file_path = r'./test_files' + '\\' + filename
        #     with open(file_path, 'wb') as f:
        #         f.write(part.get_payload(decode=True))  # 将附件解码并写入文件

        # 注意：文件用双反斜杠链接
        # file_path = r'./test_files
# 关闭连接
imap_server.close()
imap_server.logout()
