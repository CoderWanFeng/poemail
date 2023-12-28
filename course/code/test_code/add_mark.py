# -*- coding: UTF-8 -*-
'''
@作者  ：B站/抖音/微博/小红书/公众号，都叫：程序员晚枫
@微信     ：CoderWanFeng : https://mp.weixin.qq.com/s/Nt8E8vC-ZsoN1McTOYbY2g
@个人网站      ：www.python-office.com
@代码日期    ：2023/12/24 2:08 
@本段代码的视频说明     ：
'''

# pip install python-office
import office

office.image.add_watermark(file=r'D:/download/cover.png',
                           mark='B站：程序员晚枫',
                           output_path='../../imgs/cover')
