# coding=utf-8
import LoginSucc
import globalVal

import urllib.request
from http import cookiejar
import urllib.parse
import socket
import time
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

# 模拟登录函数  在验证码已知的情况下
def virLogin():
    # 表头数据
    headers = {
        # 'Host':'ssfw.tjut.edu.cn',
        # 使用火狐浏览器访问
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'User_Agent':'Mozilla / 5.0(Windows NT 10.0; WOW64; rv:45.0) Gecko / 20100101 Firefox / 45.0',
        # 'Accept': '*/*',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check',
        # 'Content-Length': '55',
        # 'Connection': 'keep-alive',
    }

    PostUrl = "http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check"

    # 提交表单的数据
    postData = {
        'j_username': globalVal.username,
        'j_password': globalVal.password,
        'validateCode': globalVal.secretCode
    }

    # 将发送的数据编码
    Data = urllib.parse.urlencode(postData).encode()

    try:
        request = urllib.request.Request(PostUrl, Data, headers)
        globalVal.showInText("进入教务系统...")
        response = globalVal.opener.open(request)

        # 获取反馈
        result = response.read().decode('utf-8')

        # 数据检查
        # print(result)

        if "userNameOrPasswordError" in result:
            return 0
        elif "validateCodeError" in result:
            return 1
        else:
            return 2

    except HTTPError as e:
        globalVal.saveTolog('The server couldn\'t fulfill the request.')
        globalVal.saveTolog('Error code: %s'% e.code)
        return 3
    except URLError as e:
        globalVal.saveTolog('We failed to reach a server.')
        globalVal.saveTolog('Reason: %s'% e.reason)
        return 3
    except:
        globalVal.saveTolog("What's the problem ???")
        return 3

# 获取验证码
def getOcrCode(CaptchaUrl="http://ssfw.tjut.edu.cn/ssfw/jwcaptcha.do"):

    socket.setdefaulttimeout(1)
    cookie_support = urllib.request.HTTPCookieProcessor(cookiejar.CookieJar())
    globalVal.opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(globalVal.opener)

    ORCCount = 0
    limitCount = 33
    # 获取验证码
    # 获取验证码的同时可以检测网络状态
    # 最多尝试33次获取验证码 否则网络连接失败 并给予线程标记
    while True:
        try:
            globalVal.saveTolog("正在尝试获取验证码(%d)..."% ORCCount)
            picture = globalVal.opener.open(CaptchaUrl).read()
            local = open('image/img.jpg', 'wb')
            local.write(picture)
            local.close()
            globalVal.getSecretCodeed = 1
            break
        except:
            cookie_support = urllib.request.HTTPCookieProcessor(cookiejar.CookieJar())
            globalVal.opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
            urllib.request.install_opener(globalVal.opener)
            ORCCount += 1
            # 获取次数大于33次就退出
            if ORCCount >= limitCount:
                globalVal.saveTolog("获取验证码失败! 请检查网络连接")
                globalVal.getSecretCodeed = -1
                break

    # 修改 到这里并不能说明获取到了验证码
    # 用于线程的标识   表示已经获取到了验证码
    # globalVal.getSecretCodeed = True
    pass

def getBackGround () :
    socket.setdefaulttimeout(5)
    globalVal.today = time.strftime("%Y-%m-%d", time.localtime())
    bing_url = 'http://www.daoiqi.com/pod/bing.php'
    html = urllib.request.urlopen(bing_url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    url = soup.find('img').get('src')
    # 尝试下载每日图片
    urllib.request.urlretrieve(url, 'bing_background(%s).jpg'%globalVal.today)
    globalVal.saveTolog("获取必应每日图片完成")
