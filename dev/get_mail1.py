# https://geek-docs.com/python/python-ask-answer/688_python_receive_and_send_emails_in_python.html
# https://blog.51cto.com/u_16213436/7489927
import email
import imaplib
import os

# 连接到IMAP服务器
imap_server = imaplib.IMAP4_SSL("imap.qq.com", 993)

qq_mail = os.getenv("EMAIL_FROM")
qq_pwd = os.getenv("EMAIL_KEY")

# 登录到邮箱
imap_server.login(qq_mail, qq_pwd)

# 选择邮箱文件夹
imap_server.select("INBOX")

# 搜索邮件
status, message_ids = imap_server.search(None, "ALL")

# 解析邮件
for message_id in message_ids[0].split():
    status, email_data = imap_server.fetch(message_id, "(RFC822)")
    # 在这里进行邮件的解析和处理
    print(status, email_data)

    # 接收所有未读邮件，参数'UNSEEN'控制
    status, data = imap_server.search(None, 'UNSEEN')
    unread_msg_nums = data[0].split()

    # 使用imap.fetch获取邮件内容，然后用email模块的message_from_bytes解析邮件，
    # 遍历邮件中的每个部分，看是否有filename字段，如果有就表示这是一个附件，然后获取附件内容并写入文件。
    for num in unread_msg_nums:
        # RFC822 代表接受邮件的全部内容，包括标题、正文和附件
        status, data = imap_server.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if bool(filename):
                print('Downloading attachment:', filename)
                attach_data = part.get_payload(decode=True)
                # 注意：文件用双反斜杠链接
                file_path = r'./test_files' + '\\' + filename
                with open(file_path, 'wb') as f:
                    f.write(part.get_payload(decode=True))  # 将附件解码并写入文件

# 关闭连接
imap_server.close()
imap_server.logout()
