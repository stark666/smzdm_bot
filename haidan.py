# -*- coding: utf-8 -*-

import os
import re
import urllib3

def sign() :
    global ERROR
    r = HTTP.request('GET', SIGNURL, headers=HEADERS)
    if (r.status != 200) :
        print('!! 签到失败，错误的状态： ' + str(r.status))
        ERROR = 1
    # 获取最新魔力值
    print('-> 尝试更新魔力值')
    r = HTTP.request('GET', BASEURL, headers=HEADERS)
    if (r.status != 200) :
        print('!! 错误的状态： ' + str(r.status))
        ERROR = 1
    data = r.data.decode('utf-8')
    pattern = re.compile('<span\s*id=[\'|"]magic_num[\'|"]>([0-9,\.]+)\([\s\S]+\)</span>')
    mn = re.search(pattern, data)
    if mn:
        mn = float(mn.group(1).replace(',', ''))
        d = mn - MAGIC_NUM
        print('-> 签到成功，获得魔力值：' + str(d))
    else:
        print('!! 获取最新魔力值失败')
        ERROR = 3

def get_status() :
    global ERROR
    global MAGIC_NUM

    print('-> 正在获取用户状态...')
    r = HTTP.request('GET', BASEURL, headers=HEADERS)
    if (r.status != 200) :
        print('!! 错误的状态： ' + str(r.status))
        ERROR = 1
    data = r.data.decode('utf-8')

    # 用户名
    pattern = re.compile('<a\s*href=[\'|"]userdetails\.php\?id=\d+[\'|"]\s*class=[\'|"].+[\'|"]\s*>\s*<b>\s*(.+)</b>\s*</a>')
    username = re.search(pattern, data)
    if username:
        if PRIVACY == '2':
            print('-> 当前用户：[保护]')
        elif PRIVACY == '3':
            print('-> 当前用户：' + username.group(1))
        else:
            if PRIVACY != '1':
                print('!! 错误的隐私登录设置')
            print('-> 当前用户：*' + username.group(1)[1:len(username.group(1)) - 1]  + '*')
    else:
        print('-> 登录身份过期或程序失效')
        ERROR = 2

    # 魔力值
    pattern = re.compile('<span\s*id=[\'|"]magic_num[\'|"]>([0-9,\.]+)\([\s\S]+\)</span>')
    mn = re.search(pattern, data)
    if mn:
        MAGIC_NUM = float(mn.group(1).replace(',', ''))
        print('-> 当前魔力值：' + str(MAGIC_NUM))
    else:
        print('-> 登录身份过期或程序失效')
        ERROR = 2

    # 打卡状态
    pattern = re.compile('<input\s*type=[\'|"]submit[\'|"]\s*id=[\'|"]modalBtn[\'|"]\s*class=[\'|"]dt_button[\'|"]\s*value=[\'|"]已经打卡[\'|"][\s]*/[\s]*>')
    signed = re.search(pattern, data)
    if not signed:
        sign()  #签到
    else:
        print('-> 今日已签到')

def main() :
    print("=================================================")
    print("||                 HaiDan Sign                 ||")
    print("||                Author: Jokin                ||")
    print("||               Version: v0.0.5               ||")
    print("=================================================")

    global HEADERS
    global MAGIC_NUM

    global ERROR
    ERROR = 0

    global BASEURL
    BASEURL = 'https://www.haidan.video/index.php'

    global SIGNURL
    SIGNURL = 'https://www.haidan.video/signin.php'

    global HTTP
    HTTP = urllib3.PoolManager()

    global PRIVACY
    PRIVACY =  os.getenv('HAIDAN_PRIVACY') if os.getenv('HAIDAN_PRIVACY') else '1'

    _uid = os.getenv('HAIDAN_UID') if os.getenv('HAIDAN_UID') else False
    _pass = os.getenv('HAIDAN_PASS') if os.getenv('HAIDAN_PASS') else False
    _login = os.getenv('HAIDAN_LOGIN') if os.getenv('HAIDAN_LOGIN') else 'bm9wZQ%3D%3D'
    _multi =  os.getenv('HAIDAN_MULTI') if os.getenv('HAIDAN_MULTI') else False

    if _multi == False:
        if not _uid or not _pass or not _login:
            print('!! 缺少设置： 环境变量/Secrets')
            exit(4)
        else:
            _multi = _uid + '@' + _pass
    else:
        print('-> 多账户支持已经启用')

    # MULTI 解析
    sp = _multi.split(',')
    for i in range(0, len(sp)):
        print('-> 当前进度： ' + str(i + 1) + '/' + str(len(sp)))
        # 格式化
        account = sp[i].strip().split('@')
        if len(account) != 2 :
            print('!! 多账户设置格式错误')
            exit(5)
        # 数据分离
        _uid = account[0]
        _pass = account[1]
        # 初始化
        MAGIC_NUM = 0
        HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'cookie': 'c_secure_login=' + _login + '; c_secure_uid=' + _uid + '; c_secure_pass=' + _pass,
        }

        get_status()

    print('-> 已经完成本次任务')
    if (ERROR != 0):
        print('!! 本次任务出现错误，请及时查看日志')
    else:
        print('-> 任务圆满完成')
    exit(ERROR)

if __name__ == '__main__':
    main()
