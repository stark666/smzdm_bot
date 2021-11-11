
import requests,os
from sys import argv

from pkg.provider.smzdm import sign
from internal.notify import dingtalk, serverchan

def smzdm_bot():
    sb = sign()
    sb.load_cookie_str(os.environ.get('COOKIES'))
    res = sb.check_in()

    check_in = '失败'
    if res['error_code'] == 0:
        check_in = '成功'    

    print(res)

    return f'「什么值得买」每日签到{check_in}!'


if __name__ == '__main__':
    dingtalk_notify = False
    serverchan_notify = False

    DINGTALK_ROBOT_SECRET = os.environ.get('DINGTALK_ROBOT_SECRET')
    DINGTALK_ROBOT_TOKEN = os.environ.get('DINGTALK_ROBOT_TOKEN')
    if (isinstance(DINGTALK_ROBOT_TOKEN,str) and len(DINGTALK_ROBOT_TOKEN)>0) and (isinstance(DINGTALK_ROBOT_SECRET,str) and len(DINGTALK_ROBOT_SECRET)>0):
        dingtalk_notify = True

    SERVERCHAN_SENDKEY = os.environ.get('SERVERCHAN_SENDKEY')
    if isinstance(SERVERCHAN_SENDKEY,str) and len(SERVERCHAN_SENDKEY)>0:
        serverchan_notify = True
   
    msg = smzdm_bot()
    if dingtalk_notify:
        print(f'检测到 "钉钉机器人" 准备推送: {msg}')
        dingtalk.push(msg = msg, token = DINGTALK_ROBOT_TOKEN, secret = DINGTALK_ROBOT_SECRET)

    if serverchan_notify:
        print(f'检测到 "SERVERCHAN" 准备推送: {msg}')
        serverchan.push(text = '什么值得买每日签到', desp = msg, secretKey = SERVERCHAN_SENDKEY)

    print('代码执行完毕')