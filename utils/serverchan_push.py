
import config
import requests

import time
import hmac
import hashlib
import base64
import urllib.parse
import json

def push_to_wechat(text,desp,secretKey):
    """
    通过serverchan将消息推送到微信
    :param secretKey: severchan secretKey
    :param text: 标题
    :param desp: 内容
    :return resp: json
    """
    url = f'http://sc.ftqq.com/{secretKey}.send'
    session = requests.Session()
    data = {'text':text,'desp':desp}
    resp = session.post(url,data = data.encode('utf-8'))
    return resp.json()

def get_dingtalk_sign(secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # print(timestamp)
    # print(sign)
    return '&timestamp=' + timestamp + '&sign=' + sign

def push_to_dingtalk(check, token, secret):
    headers = {
        'content-type': 'application/json',
    }

    sign = get_dingtalk_sign(secret=secret)
    url = 'https://oapi.dingtalk.com/robot/send?access_token=' + token + sign

    data = '{"msgtype": "text","text": {"content":"「什么值得买」 签到' + check + '!"}}'
    response = requests.post(url, headers=headers, data=data.encode('utf-8'))
    # print(url)
    # print(response)
    # print(response.content)
    return response


if __name__ == '__main__':
    #resp = push_to_wechat(text = 'test', desp='hi', secretKey= config.SERVERCHAN_SECRETKEY)
    resp = push_to_dingtalk(check = 0, token = config.TEST_DINGTALK_ROBOT_TOKEN, secret = config.TEST_DINGTALK_ROBOT_SECRET)
    print(resp)