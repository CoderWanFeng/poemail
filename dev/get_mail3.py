# -*- encoding: utf-8 -*-
# -*- encoding: gbk -*-
'''
基于Python 3.X，网上很多代码都残缺或者不能直接用，只能左抄抄右抄抄，自己改写了这份收取QQ邮箱的代码，可以收取邮件正文和附件。附件不会乱码。在邮件正文部分，解决的很粗暴，bs4直接去掉HTML属性了，同时变通解决换行问题，输出邮件内容为列表方便后期解析，以后有空再弄。测试暂时未发现bug，收取邮件后会改写为已读。
主要是可以以后改成一个基于邮箱的应答机器人。通过标题来判断问题处理方式，同时收取附件的功能可以用来传东西。
https://blog.csdn.net/weixin_43985754/article/details/134701455
'''
import os

import bs4
import email
from imapclient import IMAPClient
import sys


# import imaplib

# 猜测字符编码
def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        for item in content_type.split(';'):
            item = item.strip()
            if item.startswith('charset'):
                charset = item.split('=')[1]
                break
    return charset


def decode_str(s):
    value, charset = email.header.decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def getMail(host, username, password, port=993):
    try:
        c = IMAPClient(host, ssl=True)
        print('连接成功，SLL')
        c.login(username, password)  # 登录个人帐号
        print('登录成功，SLL')
    except:
        print('连接失败，检查服务器地址或者端口号')
        sys.exit()
    try:
        c.select_folder('INBOX', readonly=False)  # , readonly = True
        result = c.search('UNSEEN')
        if result == []:
            print('已读：%s' % c.search('SEEN'))
        #        msgdict = c.fetch(result, ['BODY.PEEK[]'] )
        msgdict = c.fetch(result, ['BODY[]'])  # 自动切换已读状态
        #        print(result)
        for message_id, message in msgdict.items():
            print('分解:%s' % message_id)
            msg = email.message_from_string(message[b'BODY[]'].decode())  # 生成Message类型,QQ邮箱返回是比特形式，要转换字符串，坑死了
            ## 由于'From', 'Subject' header有可能有中文，必须把它转化为中文
            subject = email.header.make_header(email.header.decode_header(msg['SUBJECT']))
            mail_from = email.header.make_header(email.header.decode_header(msg['From']))
            mail_to = email.utils.parseaddr(msg.get("to"))[1]  # 取to
            print('邮件标题：%s' % subject)
            print('mail_from:%s' % mail_from)
            print('mail_to:%s' % mail_to)

            # 循环信件中的每一个mime的数据块
            for par in msg.walk():
                if not par.is_multipart():  # 这里要判断是否是multipart，是的话，里面的数据是无用的，至于为什么可以了解mime相关知识。
                    name = par.get_param("name")  # 如果是附件，这里就会取出附件的文件名
                    if name:  # 有附件
                        # 下面的三行代码只是为了解码象=?gbk?Q?=CF=E0=C6=AC.rar?=这样的文件名
                        h = email.header.Header(name)
                        dh = email.header.decode_header(h)
                        fname = dh[0][0]
                        if dh[0][1]:
                            fname = decode_str(str(fname, dh[0][1]))  # 将附件名称可读化
                        print('附件名:%s' % fname)
                        data = par.get_payload(decode=True)  # 解码出附件数据，然后存储到文件中
                        try:
                            f = open(fname, 'wb')  # 注意一定要用wb来打开文件，因为附件一般都是二进制文件
                        except:
                            print('附件名有非法字符，自动换一个')
                            f = open('aaaa', 'wb')
                        f.write(data)
                        f.close()
                    else:
                        content_type = par.get_content_type()  # 获取数据类型
                        if content_type == 'text/plain' or content_type == 'text/html':
                            #                            print('# 纯文本或HTML内容:')
                            content = par.get_payload(decode=True)
                            # 要检测文本编码:
                            charset = guess_charset(par)
                            if charset:
                                content = content.decode(charset)
            #            with open('data.txt','w',encoding='utf-8') as f:
            #                f.write(content)
            html = content.replace('
                                   ','
                                   ')
            html_fj = html.split("
                                 ")
            邮件正文内容_list = []
            for i in html_fj:
                soup = bs4.BeautifulSoup(i, 'lxml')
            邮件正文内容 = soup.getText().strip()
            if len(邮件正文内容) != 0:
                邮件正文内容_list.append(邮件正文内容)
            print('%s号邮件正文内容: ' % (message_id))
            for i in 邮件正文内容_list:
                print(i)
            print('+' * 60)  # 用来区别各个部分的输出
            c.set_flags(message_id, '\Seen')
            # \Flagged标星，\Seen 标记已读，\Deleted 删除
            #            print('设置单个邮件为已读')
            # 设置所有未读取邮件为已读邮件
            #        if result!=[]:
            #            c.set_flags(msgdict, b'\\unseen', silent=False)
            #            print('设置邮件为已读')
            if result == []:
                print('无新的未读邮件')
                #    except Exception as bcnr:
                #        print('报错信息：%s' % bcnr)
    finally:
        c.logout()


if __name__ == '__main__':
    host = "imap.qq.com"  # "pop.mail_serv.com"
    username = os.getenv("EMAIL_FROM")
    password = os.getenv("EMAIL_PWD")
    port = 993
    getMail(host, username, password, port)