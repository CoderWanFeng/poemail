# -*- coding: UTF-8 -*-
'''
@Author  ：程序员晚枫，B站/抖音/微博/小红书/公众号
@WeChat     ：CoderWanFeng
@Blog      ：www.python-office.com
@Date    ：2023/1/22 18:26 
@Description     ：
'''

DEFAULT_CONFIG_PATH = r'./'
DEFAULT_CONFIG_NAME = r'baidu-config.toml'

DEFAULT_CONFIG_PATH_NAME = DEFAULT_CONFIG_PATH + DEFAULT_CONFIG_NAME

FACE_URL = "https://aip.baidubce.com/rest/2.0/face/v1/merge?access_token="

SPLIT_LINE = '=' * 30

Mail_Type = {
    'qq': 'smtp.qq.com',
    '163': 'smtp.163.com',
}

Result_Type = {
    '200': 'success',
    '404': 'error',
    '500': 'warning'
}
