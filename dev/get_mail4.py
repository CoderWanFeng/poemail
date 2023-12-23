# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@微信     ：CoderWanFeng : https://mp.weixin.qq.com/s/Nt8E8vC-ZsoN1McTOYbY2g
@个人网站      ：www.python-office.com
@代码日期    ：2023/12/23 20:56 
@本段代码的视频说明     ：
'''

import email
import imaplib
import os
import re
import sys
import tempfile
import uuid
from email.header import Header
from email.utils import parseaddr
from traceback import format_exc


class EmailReceiveClient:
    # 出自：https://zhuanlan.zhihu.com/p/619408348

    def __init__(self, username, password, imap_server, imap_port, need_ssl=False):
        """
        构造函数
        :param username: 邮箱登录账号
        :param password: 邮箱登录密码
        :param imap_server: 邮箱服务器
        :param imap_port: 邮箱服务器端口
        :param need_ssl: 是否需要ssl加密
        """
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.need_ssl = need_ssl
        self.imap_port = imap_port
        self.imap_client = None

    def imap_login(self):
        """
        imap 登录邮箱, 登录后默认选择操作收件箱,
        备注参考: https://blog.csdn.net/jony_online/article/details/108638571
        :return: 登录结果, dict, eg: {"status_code": 200, "message": "imap login ok"}
        """
        try:
            imaplib.Commands['ID'] = 'AUTH'
            if self.need_ssl:
                server = imaplib.IMAP4_SSL(host=self.imap_server, port=self.imap_port)
            else:
                server = imaplib.IMAP4(host=self.imap_server, port=self.imap_port)
            server.login(self.username, self.password)
            args = ("name", "python_email_tool", "contact", "17602143142@163.com",
                    "version", "1.0.0", "vendor", "myclient")
            typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')
            print(server._untagged_response(typ, dat, 'ID'))
        except Exception as e:
            error_info = "imap login fail for the reason of: {0}, detail reason: {1}"
            return {"status_code": 400, "message": error_info.format(repr(e), format_exc())}
        self.imap_client = server
        self.select(section="INBOX")  # 默认解析收件箱信息
        return {"status_code": 200, "message": "imap login ok"}

    def show_folders(self):
        """
        返回邮箱所有文件夹
        :return: tuple, eg:
        ("ok", [b'() "/" "INBOX"', b'(\\Drafts) "/" "&g0l6P3ux-"',
        b'(\\Sent) "/" "&XfJT0ZAB-"', b'(\\Trash) "/" "&XfJSIJZk-"',
        b'(\\Junk) "/" "&V4NXPpCuTvY-"', b'() "/" "&dcVr0mWHTvZZOQ-"'])
        """
        return self.imap_client.list()

    def select(self, section):
        """
        选择解析信息的区域,不清楚可以调用show_folders查看已有区域
        :param section: str, eg: "INBOX"
        :return: tuple, eg: ('OK', [b'1'])
        """
        return self.imap_client.select(section)

    def search(self, charset, *criteria):
        """
        搜索邮件(参照RFC文档http://tools.ietf.org/html/rfc3501#page-49)
        """
        return self.imap_client.search(charset, *criteria)

    def get_unread(self):
        """
        返回所有未读的邮件列表(返回的是包含邮件序号的列表),注意邮箱系统可能默认只能接收最近30天的邮件,
        所以可能会看到这里为空的
        :returns tuple, eg: ('OK', [b'1 2'])
        """
        return self.search(None, "Unseen")  # Unseen 表示未读邮件,ALL 表示所有邮件

    def get_email_format(self, num):
        """
        以RFC822协议格式返回邮件详情的email对象
        :param num: str, digit, eg: "1"
        :return dict, eg: {"status_code": 200, "message": format_result}
        """
        # print(type(num), "aaa {0} bbb".format(num))
        data = self.imap_client.fetch(num, 'RFC822')
        status = data[0]
        content = data[1]
        if status == 'OK':
            return {"status_code": 200, "src": content[0][1],
                    "message": email.message_from_string(str(content[0][1], encoding="utf-8"))}
        else:
            return {"status_code": 500, "message": "fetch error, error info: {0}".format(content)}

    @staticmethod
    def get_sender_info(msg):
        """
        返回发送者的信息——元组（邮件称呼，邮件地址）
        :param msg: email对象
        :return: tuple, eg: ("eason", "17000000000@163.com")
        """
        print("msg from: ", msg["from"])
        name = email.utils.parseaddr(msg["from"])[0]
        decode_name = email.header.decode_header(name)[0]
        if decode_name[1] is not None:
            name = str(decode_name[0], decode_name[1])
        address = email.utils.parseaddr(msg["from"])[1]
        return name, address

    @staticmethod
    def get_receiver_info(msg):
        """
        返回接受者的信息——元组（邮件称呼，邮件地址）
        :param msg: email对象
        :return: tuple
        """
        name = email.utils.parseaddr(msg["to"])[0]
        decode_name = email.header.decode_header(name)[0]
        if decode_name[1] is not None:
            name = str(decode_name[0], decode_name[1])
        address = email.utils.parseaddr(msg["to"])[1]
        return name, address

    @staticmethod
    def get_cc_info(msg):
        """
        返回抄送人的邮箱信息
        :param msg: email对象
        :return: tuple
        """
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        if not msg['Cc']:
            return ""
        cc_list = msg['Cc'].split(',')
        cc_info = []
        for i in cc_list:
            match = re.search(pattern, i)

            if match:
                cc_info.append(match.group())
        return ",".join(cc_info)

    @staticmethod
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

    @staticmethod
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

    def save_eml(self, num):
        msg = self.get_email_format(num)
        if msg["status_code"] == 200:
            src = msg['src']
            message = msg['message']
        else:
            return {"status_code": 400, "message": msg["message"]}
        temp_path = tempfile.gettempdir()
        uuid_ret = uuid.uuid1()
        save_path = os.path.join(temp_path, str(uuid_ret) + '.eml')
        try:
            with open(save_path, 'wb') as f:
                f.write(src)
            print(f"主题为：{self.get_subject_content(message)} 的邮件保存成功，路径：{save_path}")
        except Exception as e:
            print(f'eml文件保存失败，原因：{str(e)}')

    def get_mail_info(self, num):
        """
        返回邮件的解析后信息部分
        返回列表包含（主题，纯文本正文部分，html的正文部分，发件人元组，收件人元组，附件列表）
        :param num: str, digit,表示检索区域的邮件编号
        :return: dict, eg:
        {"status_code": 200,
         "message": {"subject": "", "body": "", "html": "", "from": "", "to": "", "attachments": []}
        }
        """
        msg = self.get_email_format(num)
        if msg["status_code"] == 200:
            src = msg['src']
            msg = msg["message"]
        else:
            return {"status_code": 400, "message": msg["message"]}
        attachments = []
        body = None
        html = None
        # 用来存储邮件正文中的图片在本地的保存路径，便于发送邮件时使用
        pool = {}
        try:
            for part in msg.walk():
                charset = part.get_content_charset()
                if charset is None:
                    charset = part.get_charset()
                if not charset:
                    charset = "utf-8"
                attachment = self.parse_attachment(part)
                if attachment:
                    attachments.append(attachment)
                elif part.get_content_type() == "text/plain":
                    if body is None:
                        body = ""
                    try:
                        body += str(part.get_payload(decode=True), encoding=charset)
                    except UnicodeDecodeError:
                        try:
                            if charset == "utf-8":
                                body += str(part.get_payload(decode=True), encoding="gb2312")
                            elif charset == "gb2312":
                                body += str(part.get_payload(decode=True), encoding="utf-8")
                        except UnicodeDecodeError:
                            body += str(part.get_payload(decode=True))
                elif part.get_content_type() == "text/html":
                    if html is None:
                        html = ""
                    try:
                        html += str(part.get_payload(decode=True), encoding=charset)
                    except UnicodeDecodeError:
                        try:
                            if charset == "utf-8":
                                html += str(part.get_payload(decode=True), encoding="gb2312")
                            elif charset == "gb2312":
                                html += str(part.get_payload(decode=True), encoding="utf-8")
                        except UnicodeDecodeError:
                            html += str(part.get_payload(decode=True))
                elif part.get_content_type() == 'application/octet-stream':
                    temp_path = tempfile.gettempdir()
                    uuid_ret = uuid.uuid1()
                    save_path = os.path.join(temp_path, str(uuid_ret) + '.png')
                    with open(save_path, "wb") as f:
                        try:
                            if charset == "utf-8":
                                f.write(part.get_payload(decode=True))
                            elif charset == "gb2312":
                                f.write(part.get_payload(decode=True))
                        except UnicodeDecodeError:
                            f.write(part.get_payload(decode=True))

                    pool[part.get('Content-ID')[1:-1]] = save_path
                elif part.get_content_type().startswith("image"):
                    temp_path = tempfile.gettempdir()
                    uuid_ret = uuid.uuid1()
                    save_path = os.path.join(temp_path, str(uuid_ret) + '.png')
                    with open(save_path, "wb") as f:
                        try:
                            if charset == "utf-8":
                                f.write(part.get_payload(decode=True))
                            elif charset == "gb2312":
                                f.write(part.get_payload(decode=True))
                        except UnicodeDecodeError:
                            f.write(part.get_payload(decode=True))
                    pool[part.get('Content-ID')[1:-1]] = save_path
        except Exception as e:
            self.mark_unseen(num=str(num))
            error_info = "receive email failed, exception: {0}, detail: {1}".format(repr(e), format_exc())
            return {"status_code": 400, "message": error_info}
        return {"status_code": 200,
                "message": {
                    'subject': self.get_subject_content(msg),
                    'body': body,
                    'html': html,
                    'from': self.get_sender_info(msg),
                    'to': self.get_receiver_info(msg),
                    'cc': self.get_cc_info(msg),
                    'attachments': attachments,
                    'path': pool,
                }
                }

    def mark_unseen(self, num):
        """
        将指定邮件标记为未读
        :param num: 指定区域邮件的编号
        :return: None
        """
        self.imap_client.store(num, '-FLAGS', r'\Seen')

    def mark_seen(self, num):
        """
        将指定邮件标记为已读
        :param num: 指定区域邮件的编号
        :return: None
        """
        self.imap_client.store(num, '+FLAGS', r'\Seen')


if __name__ == '__main__':
    # 是否将邮件保存为 eml 格式文件
    is_save = False
    # 是否将未读邮件保存为已读邮件
    is_change2seen = False

    # 基本配置信息
    username = ""
    password = ""
    imap_server = ""
    need_ssl = False
    imap_port = 993 if need_ssl else 143  # 如果ssl连接则默认为993,否则默认为143
    client = EmailReceiveClient(
        username=username, password=password,
        imap_server=imap_server, imap_port=imap_port, need_ssl=need_ssl
    )
    login_ret = client.imap_login()
    print('邮箱登录成功', login_ret)
    unread_ret = client.get_unread()  # ('OK', [b'223 225 226 227'])

    unread_num_list = str(unread_ret[1][0], encoding="utf-8").split(' ')
    # 处理未读邮件
    if unread_num_list == ['']:
        print("未读邮件为空，程序结束")
        sys.exit(0)
    for unread_num in unread_num_list:

        if is_save:
            client.save_eml(unread_num)
        if is_change2seen:
            client.mark_seen(unread_num)
        mail_info = client.get_mail_info(unread_num)
        print(mail_info)
