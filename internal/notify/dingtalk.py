
import requests

import time
import hmac
import hashlib
import base64
import urllib.parse

def get_sign(secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # print(timestamp)
    # print(sign)
    return '&timestamp=' + timestamp + '&sign=' + sign

def push(msg, token, secret):
    headers = {
        'content-type': 'application/json',
    }

    sign = get_sign(secret=secret)
    url = f'https://oapi.dingtalk.com/robot/send?access_token={token}{sign}'

    data = '{"msgtype": "text","text": {"content":"' + msg + '"}}'
    response = requests.post(url, headers=headers, data=data.encode('utf-8'))
    # print(url)
    # print(response)
    # print(response.content)
    return response