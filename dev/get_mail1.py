# https://geek-docs.com/python/python-ask-answer/688_python_receive_and_send_emails_in_python.html
# https://blog.51cto.com/u_16213436/7489927
# https://www.php.cn/faq/586358.html
import email
import imaplib
import os
import tempfile
import uuid
from email.header import decode_header

from dev.get_mail4 import EmailReceiveClient


def get_subject_content(msg):
    """
    返回邮件的主题(参数msg是email对象，可调用get_email_format获得)
    :param msg: email对象
    :return: str
    """
    decode_content = email.header.decode_header(msg['subject'])[0]
    if decode_content[1] is not None:
        return str(decode_content[0], decode_content[1])
    return decode_content[0]


def parse_attachment(message_part):
    """
    判断是否有附件，并解析（解析email对象的part）
    返回列表（内容类型，大小，文件名，数据流）
    :param message_part: email对象的part
    :return: dict, keys: content_type, size, name, data
    """
    content_disposition = message_part.get("Content-Disposition", None)
    if content_disposition:
        dispositions = content_disposition.strip().split(";")
        print("dispositions: ", dispositions)
        invalid_character = r'<>:"/\|?* '
        if bool(content_disposition and dispositions[0].lower() == "attachment"):
            if 'message/rfc822' == message_part.get_content_type():
                payload = message_part.get_payload()
                attachment = {
                    "content_type": message_part.get_content_type(),
                }
                # print("payload: ", payload)
                for mail in payload:
                    mail2 = email.message_from_bytes(mail.as_bytes())
                    subject = EmailReceiveClient.get_subject_content(mail2)
                    for char in invalid_character:
                        subject = subject.replace(char, '')
                    # filename = subject + ".eml"
                    mail_content = mail.as_bytes()
                    attachment["size"] = len(mail_content)
                    attachment["name"] = subject + "_" + str(uuid.uuid1()) + ".eml"
                    temp_path = tempfile.gettempdir()
                    uuid_ret = uuid.uuid1()
                    save_path = os.path.join(temp_path, str(uuid_ret) + '.eml')
                    try:
                        with open(save_path, 'wb') as f:
                            f.write(mail_content)
                            attachment['save_path'] = save_path
                            print(f'附件邮件保存成功，路径为：{save_path}')
                    except Exception as e:
                        print(f'eml文件保存失败，原因：{str(e)}')
                    # attachment["data"] = mail_content
            else:
                file_data = message_part.get_payload(decode=True)
                attachment = {"content_type": message_part.get_content_type(),
                              "size": len(file_data)
                              }
                # print("attachment: ", attachment)
                decode_name = email.header.decode_header(message_part.get_filename())[0]
                name = decode_name[0]
                if decode_name[1] is not None:
                    name = str(decode_name[0], decode_name[1])
                for char in invalid_character:
                    name = name.replace(char, '')
                attachment["name"] = os.path.splitext(name)[0] + "_" + str(uuid.uuid1()) \
                                     + os.path.splitext(name)[1]
                # attachment["data"] = file_data
                temp_path = tempfile.gettempdir()
                uuid_ret = uuid.uuid1()
                save_path = os.path.join(temp_path, str(uuid_ret) + os.path.splitext(name)[1])
                try:
                    with open(save_path, 'wb') as f:
                        f.write(file_data)
                        attachment['save_path'] = save_path
                        print(f'附件文件保存成功，路径为；{save_path}')
                except Exception as e:
                    print(f'附件文件保存失败，原因：{str(e)}')
            return attachment
    return None


def save_attachment(part):
    part.ge
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
    mail_type = msg.get_content_maintype()
    if mail_type == 'multipart':
        for part in msg.walk():
            content_type = part.get_content_type()
            if 'application' in content_type:
                parse_attachment(part)
# 关闭连接
imap_server.close()
imap_server.logout()
