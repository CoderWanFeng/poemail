# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫，微信：CoderWanFeng
@读者群     ：http://www.python4office.cn/wechat-group/
@学习网站      ：www.python-office.com
@代码日期    ：2023/12/23 20:56
@本段代码的视频说明     ：
'''

# 以下是一个基本的Python示例，使用poplib和email库来登录邮箱并下载所有未读邮件的附件。这个示例假设你已经启用了POP3服务并获取了相应的授权密码。

import email
import os
import poplib
from email.header import decode_header
from email.utils import parseaddr

# 邮箱设置
email_addr = 'your_email@example.com'
password = 'your_password_or_authorization_code'
pop3_server = 'pop.example.com'  # 替换为你的POP3服务器地址

# 连接POP3服务器
pop_conn = poplib.POP3_SSL(pop3_server)
pop_conn.user(email_addr)
pop_conn.pass_(password)

# 获取邮件数量和大小
num_messages = len(pop_conn.list()[1])
for i in range(num_messages):
    # 获取邮件信息
    raw_email = b'\n'.join(pop_conn.retr(i + 1)[1])
    email_msg = email.message_from_bytes(raw_email)

    # 检查邮件是否未读
    if 'X-Status' in email_msg and 'UNSEEN' in email_msg['X-Status']:
        # 解析邮件标题和发件人
        subject, encoding = decode_header(email_msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding)
        from_name, from_email = parseaddr(email_msg['From'])

        # 解析并下载附件
        for part in email_msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if not filename:
                ext = mimetypes.guess_extension(part.get_content_type())
                if not ext:
                    ext = '.bin'
                filename = f'part-{i}{ext}'

            file_data = part.get_payload(decode=True)
            with open(os.path.join('attachments', from_name, filename), 'wb') as f:
                f.write(file_data)

# 关闭POP3连接
pop_conn.quit()
"""

这个脚本会将未读邮件的附件按照发件人的名字分类存储在
`attachments`
目录下。请注意，这个示例可能需要根据你的邮箱服务提供商进行一些调整，例如处理不同的邮件状态标识（未读 / 已读）或者不同的附件编码方式。

另外，如果你的邮箱使用的是IMAP协议而不是POP3，你可能需要使用imaplib库代替poplib，并相应地调整代码。

"""
