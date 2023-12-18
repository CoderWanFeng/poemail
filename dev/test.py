import os
import smtplib
from email.mime.application import MIMEApplication

# 发件人邮箱地址
sendAddress = '程序员晚枫@qq.com'
# 发件人授权码
password = 'xxx'
# 连接服务器
server = smtplib.SMTP_SSL('smtp.qq.com', 465)
# 登录邮箱
loginResult = server.login(sendAddress, password)
print(loginResult)

msg_from = '程序员晚枫@qq.com'
msg_to = '程序员晚枫@qq.com'
msg_subject = '自动发邮件'
# 正文
content = """
尊敬的用户您好:
附件中为您申请的个人乘机凭证，请查收。手机查看可能出现乱码现象，请您在电脑上查看即可。
使用航旅纵横“验真服务-行程单验真”功能可以扫描凭证中的二维码检验信息。如有任何建议与意见，欢迎通过APP中的意见反馈与我们交流，谢谢您的使用。
"""
# 定义一个可以添加正文的邮件消息对象
# msg = MIMEText(content, 'plain', 'utf-8')

# # 发件人昵称和地址
# msg['From'] = msg_from
# # 收件人昵称和地址
# msg['To'] = msg_to
# # msg['To'] = '晚枫1号<程序员晚枫@qq.com>;xxx<xxx@qq.com>'
# # 抄送人昵称和地址
# # msg['Cc'] = 'xxx<xxx@qq.com>;xxx<xxx@qq.com>'
# # 邮件主题
# msg['Subject'] = msg_subject


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 定义一个可以添加正文和附件的邮件消息对象
msg = MIMEMultipart()
# 发件人昵称和地址
msg['From'] = msg_from
# 收件人昵称和地址
msg['To'] = msg_to
# msg['To'] = '晚枫1号<程序员晚枫@qq.com>;xxx<xxx@qq.com>'
# 抄送人昵称和地址
# msg['Cc'] = 'xxx<xxx@qq.com>;xxx<xxx@qq.com>'
# 邮件主题
msg['Subject'] = msg_subject
# 正文
content = """
尊敬的用户您好:
附件中为您申请的个人乘机凭证，请查收。手机查看可能出现乱码现象，请您在电脑上查看即可。
使用航旅纵横“验真服务-行程单验真”功能可以扫描凭证中的二维码检验信息。如有任何建议与意见，欢迎通过APP中的意见反馈与我们交流，谢谢您的使用。
"""
# 先通过MIMEText将正文规范化，构造成邮件的一部分，再添加到邮件消息对象中
msg.attach(MIMEText(content, 'plain', 'utf-8'))

# 附件（添加多个附件同理）
# # 以二进制形式将文件的数据读出，再使用MIMEText进行规范化
# # attachment = MIMEText(open('跑车.jpg', 'rb').read(), 'base64', 'utf-8')
# # 告知浏览器或邮件服务器这是字节流，浏览器处理字节流的默认方式为下载
# attachment['Content-Type'] = 'application/octet-stream'
# # 此部分主要是告知浏览器或邮件服务器这是一个附件，名字叫做xxxxx，
# # 这个文件名不要用中文，不同邮箱对中文的对待形式不同
# attachment['Content-Disposition'] = 'attachment;filename="car.jpg"'
# msg.attach(attachment)
# 添加Excel类型附件
file_name = r'D:\workplace\code\test\python\pdf_mark\添加了水印的文件.pdf'  # 文件名
file_path = os.path.join(file_name)  # 文件路径
xlsx = MIMEApplication(open(file_path, 'rb').read())  # 打开Excel,读取Excel文件
xlsx["Content-Type"] = 'application/octet-stream'  # 设置内容类型
xlsx.add_header('Content-Disposition', 'attachment', filename=file_name)  # 添加到header信息
msg.attach(xlsx)

server.sendmail(sendAddress, [msg_to], msg.as_string())
print('发送成功')
