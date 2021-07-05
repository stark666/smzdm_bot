
import config
import requests


def push_to_wechat(text, desp, appToken, uid):
    """
    通过wxpusher将消息推送到微信
    """
    url = f'http://wxpusher.zjiecode.com/api/send/message'
    session = requests.Session()
    data = {
        "appToken": appToken,
        "content": desp,
        "summary": text,
        "contentType": 1,
        "topicIds": [],
        "uids": [
            uid
        ],
    }
    headers = {
        'Content-Type': 'application/json'
    }
    resp = session.post(url, json=data, headers=headers)
    return resp.json()


if __name__ == '__main__':
    resp = push_to_wechat(text='test', desp='hi',
                          appToken='',
                          uid='')
    print(resp)
