
import config
import requests


def push_to_wechat(text,desp,secretKey):
    """
    通过serverchan将消息推送到微信
    :param secretKey: severchan secretKey
    :param text: 标题
    :param desp: 内容
    :return resp: json
    """
    url = f'http://sctapi.ftqq.com/{secretKey}.send'
    session = requests.Session()
    data = {'text':text,'desp':desp}
    resp = session.post(url,data = data)
    return resp.json()


if __name__ == '__main__':
    resp = push_to_wechat(text = 'test', desp='hi', secretKey= config.SERVERCHAN_SECRETKEY)
    print(resp)