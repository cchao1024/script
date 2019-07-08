# /usr/bin/env python
# coding=utf8

import urllib
import requests
import hashlib
import random

appid = ''  # 你的appid
secretKey = ''  # 你的密钥

httpClient = None
myurl = '/api/trans/vip/translate'
q = 'apple'
fromLang = 'en'
toLang = 'zh'
salt = random.randint(32768, 65536)

sign = appid + q + str(salt) + secretKey
sign = hashlib.md5(sign).hexdigest()
myurl = myurl + '?appid=' + appid + '&q=' + urllib.quote(
    q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
data = {
    'appid': appid,
    'q': 'hello',
    'from': 'auto',
    'en': 'en',
    'salt': str(salt),
    'sign': sign
}
proxies = {
    "http": "http://127.0.0.1:8888",
    "https": "http://127.0.0.1:8888"
}
# httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
# httpClient.request('GET', myurl)
response = requests.get('http://api.fanyi.baidu.com/api/trans/vip/translate', data,
                        proxies=proxies)

# response是HTTPResponse对象
response = httpClient.getresponse()
print
response.read()
