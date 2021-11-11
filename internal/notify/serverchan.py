
import requests

def push(text,desp,secretKey):
    """
    通过 serverchan 将消息推送到微信
    :param secretKey: severchan secretKey
    :param text: 标题
    :param desp: 内容
    :return resp: json
    """
    url = f'https://sctapi.ftqq.com/{secretKey}.send'
    session = requests.Session()
    data = {'text':text,'desp':desp}
    resp = session.post(url, data = data)
    return resp.json()