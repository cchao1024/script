# /usr/bin/env python
# coding=utf8

import hashlib
import time
import requests
import random
import json
import re

api = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
appid = '20190708000315910'  # 你的appid
secretKey = 'tymR5YEUYQVkKv9aE0qa'  # 你的密钥
def_from_lang = 'zh'
from_file_path = './string.xml'
out_put_file_name = 'string_%s.xml'
to_lang_map = {
    'en': 'en_GB'
}

# 调用百度翻译api 执行翻译
def trans_bd_api(q, to_lang, from_lang=def_from_lang):
    salt = random.randint(32768, 65536)

    md5 = hashlib.md5()
    sign = appid + q + str(salt) + secretKey
    sign = sign.encode('utf-8')
    # print("生成字符串1" + str(sign))
    md5.update(sign)
    sign = md5.hexdigest()
    # print("生成字符串1md5  " + str(sign))

    data = {
        'appid': appid,
        'q': q,
        'from': from_lang,
        'to': to_lang,
        'salt': str(salt),
        'sign': sign
    }
    proxies = {
        "http": "http://127.0.0.1:8888",
        "https": "http://127.0.0.1:8888"
    }

    # 发送请求
    response = requests.get(api, data, proxies=proxies)
    # response = requests.get(api, data)
    '''
    {
        "from": "en",
        "to": "zh",
        "trans_result": [{
            "src": "apple",
            "dst": "苹果"
        }]
    }
    '''

    try:
        json_obj = json.loads(str(response.text))
        result = json_obj['trans_result'][0]['dst']
        print('【' + q + '】      目标语言【' + to_lang + '】      响应的结果【' + result + '】')
        return result
    except:
        print(str(response.text) + '【' + q + '】      目标语言【' + to_lang + '】')
    return '█'


# 翻译完后追加写入到 目标文件
def trans_and_write(key, q):
    for lang in to_lang_map:
        result = trans_bd_api(q, lang)
        out_put_file = out_put_file_name % to_lang_map.get(lang)
        with open(out_put_file, 'a') as f:
            f.write('<string name="' + key + '">' + str(result) + '</string>\n')
            print('[' + out_put_file + ']   【' + key + '=' + result + '】')
            # 非vip 不允许高频率请求接口
        time.sleep(2)


def split_trans_content():
    # 正则 待翻译的文本
    # <string name="tab_name_1">说说</string>
    pattern = re.compile(r'^.*?name="(.*)">(.*)</string>')

    with open(from_file_path, 'r+', encoding='utf-8') as f:
        for line in f.readlines():
            if pattern.match(line.strip()):
                groups = pattern.match(line.strip()).groups()
                print('----------  翻译 [' + groups[1] + '] ----------')
                trans_and_write(groups[0], groups[1])


split_trans_content()
