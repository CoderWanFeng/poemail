# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫，微信：CoderWanFeng
@读者群     ：http://www.python4office.cn/wechat-group/
@学习网站      ：www.python-office.com
@代码日期    ：2023/12/23 21:10 
@本段代码的视频说明     ：
'''
import email
import imaplib
import os
import uuid
from email.header import decode_header
from pathlib import Path

from pofile import fix_unsaved_char, mkdir

from poemail.core.BaseEmail import BaseEmail


class ReceiveEmail(BaseEmail):
    def __init__(self, key, msg_from, msg_to, msg_subject='', host='smtp.qq.com', port=465, base_output_path=r'./',
                 status="UNSEEN"):
        super().__init__(key, msg_from, msg_to, msg_subject, host, port)
        self.base_output_path = base_output_path
        self.status = status

    def get_subject_content(self, msg):
        """
        返回邮件的主题(参数msg是email对象，可调用get_email_format获得)
        :param msg: email对象
        :return: str
        """
        decode_content = email.header.decode_header(msg['subject'])[0]
        if decode_content[1] is not None:
            return str(decode_content[0], decode_content[1])
        return decode_content[0]

    def parse_attachment(self, message_part, output_dir):
        """
        解析邮件附件

        Args:
            message_part: 邮件消息部分
            output_dir: 输出目录

        Returns:
            attachment: 邮件附件信息字典，如果没有附件则返回None
        """

        content_disposition = message_part.get("Content-Disposition", None)
        if content_disposition:
            dispositions = content_disposition.strip().split(";")
            if bool(content_disposition and dispositions[0].lower() == "attachment"):
                # 是含有附件的邮件
                if 'message/rfc822' == message_part.get_content_type():
                    # 是符合message/rfc822标准的附件
                    payload = message_part.get_payload()
                    attachment = {
                        "content_type": message_part.get_content_type(),
                    }
                    # print("payload: ", payload)
                    for mail in payload:
                        mail2 = email.message_from_bytes(mail.as_bytes())
                        subject = self.get_subject_content(mail2)
                        # for char in self.invalid_character:
                        #     subject = subject.replace(char, '')
                        # filename = subject + ".eml"
                        subject = fix_unsaved_char(subject)
                        mail_content = mail.as_bytes()
                        attachment["size"] = len(mail_content)
                        attachment["name"] = subject + "_" + str(uuid.uuid1()) + ".eml"

                        save_path = os.path.join(output_dir, attachment["name"])
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
                    # for char in self.invalid_character:
                    #     name = name.replace(char, '')
                    name = fix_unsaved_char(name)
                    attachment["name"] = os.path.splitext(name)[0] + "_" + str(uuid.uuid1()) \
                                         + os.path.splitext(name)[1]
                    save_path = os.path.join(output_dir, name)
                    try:
                        with open(save_path, 'wb') as f:
                            f.write(file_data)
                            attachment['save_path'] = save_path
                            print(f'附件文件保存成功，路径为；{save_path}')
                    except Exception as e:
                        print(f'附件文件保存失败，原因：{str(e)}')
                return attachment
        return None

    def get_email(self):
        # 连接到IMAP服务器
        imap_server = imaplib.IMAP4_SSL(self.host)

        # 登录到邮箱
        imap_server.login(self.msg_from, self.key)

        # 选择邮箱文件夹
        imap_server.select("INBOX")

        # 接收所有未读邮件，参数'UNSEEN'控制
        # status, data = imap_server.search(None, 'UNSEEN')
        status, data = imap_server.search(None, self.status)
        unread_msg_nums = data[0].split()

        # 使用imap.fetch获取邮件内容，然后用email模块的message_from_bytes解析邮件，
        # 遍历邮件中的每个部分，看是否有filename字段，如果有就表示这是一个附件，然后获取附件内容并写入文件。
        file_path_index = 0
        for num in unread_msg_nums:
            file_path_index += 1
            # RFC822 代表接受邮件的全部内容，包括标题、正文和附件
            status, data = imap_server.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            t = decode_header(msg["From"])
            from_email = decode_header(msg["From"])[-1][0]
            from_email = fix_unsaved_char(str(from_email))
            mail_type = msg.get_content_maintype()
            if mail_type == 'multipart':
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if 'application' in content_type:
                        save_dir = Path(self.base_output_path) / (str(file_path_index) + from_email)
                        mkdir(str(save_dir))
                        self.parse_attachment(part, str(save_dir))  # 保存附件
        # 关闭连接
        imap_server.close()
        imap_server.logout()
