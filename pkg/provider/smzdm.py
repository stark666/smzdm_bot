"""
「什么值得买」自动签到
GitHub Actions 定时执行
"""

import requests

"""
请求头
"""
DEFAULT_HEADERS = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'zhiyou.smzdm.com',
        'Referer': 'https://www.smzdm.com/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        }

class sign(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            # print(result)
            return True
        except Exception as e:
            print(f'Error: {e}')            
            return False

    def load_cookie_str(self, cookies):
        if isinstance(cookies,str) and len(cookies) > 0:
            self.session.headers['Cookie'] = cookies.encode('utf-8')    

    def check_in(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content