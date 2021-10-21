"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests,os
from sys import argv

import config
from utils.serverchan_push import push_to_dingtalk, push_to_wechat

class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            # print(result)
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        if isinstance(cookies,str) and len(cookies) > 0:
            self.session.headers['Cookie'] = cookies.encode('utf-8')    

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content

if __name__ == '__main__':
    sb = SMZDM_Bot()

    # DINGTALK_ROBOT_SECRET = config.TEST_DINGTALK_ROBOT_SECRET
    # DINGTALK_ROBOT_TOKEN = config.TEST_DINGTALK_ROBOT_TOKEN
    # cookies = config.TEST_COOKIE

    cookies = os.environ.get('COOKIES')
    DINGTALK_ROBOT_SECRET = os.environ.get('DINGTALK_ROBOT_SECRET')
    DINGTALK_ROBOT_TOKEN = os.environ.get('DINGTALK_ROBOT_TOKEN')

    sb.load_cookie_str(cookies)
    res = sb.checkin()
    print(res)

    check_in = '失败'
    if res['error_code'] == 0:
        check_in = '成功'

    SERVERCHAN_SECRETKEY = os.environ.get('SERVERCHAN_SECRETKEY')
    print('sc_key: ', SERVERCHAN_SECRETKEY)
    if isinstance(SERVERCHAN_SECRETKEY,str) and len(SERVERCHAN_SECRETKEY)>0:
        print('检测到 SCKEY， 准备推送')
        push_to_wechat(text = '什么值得买每日签到',
                        desp = str(res),
                        secretKey = SERVERCHAN_SECRETKEY)

    if (isinstance(DINGTALK_ROBOT_TOKEN,str) and len(DINGTALK_ROBOT_TOKEN)>0) and (isinstance(DINGTALK_ROBOT_SECRET,str) and len(DINGTALK_ROBOT_SECRET)>0):
         print('检测到 "钉钉机器人" 准备推送')
         push_to_dingtalk(check = check_in, token = DINGTALK_ROBOT_TOKEN, secret = DINGTALK_ROBOT_SECRET)


    print('代码完毕')