# coding=utf-8
#   SearchMyScore.py
#   获取成绩信息(已经登录的情况下)
#
#   2016年8月6日

import urllib.request
import urllib.parse
import globalVal
from urllib.error import URLError, HTTPError

def getMyScore():
    PostUrl = "http://ssfw.tjut.edu.cn/ssfw/zhcx/cjxx.do"

    headers ={
        #'Host':'ssfw.tjut.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        #'Accept': '*/*',
        #'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #'X-Requested-With': 'XMLHttpRequest',
        'Referer':'http://ssfw.tjut.edu.cn/ssfw/zhcx/cjxx.do',
        #'Content-Length': '55',
        #'Connection': 'keep-alive',
    }
    postData ={
        'currentSelectTabId':'01',
        'isFirst':'1',
        'optype':'query',
        'qKch_ys':'',
        'qKclbdm_ys':'',
        'qKcm_ys':'',
        'qKcxzdm_ys':'',
        'qXndm_ys' : globalVal.check_myscore_val[0:9],
        'qXqdm_ys' : globalVal.check_myscore_val[-1:]
    }
    content = ''
    try:
        Data = urllib.parse.urlencode(postData).encode()
        request = urllib.request.Request(PostUrl,Data,headers)
        content = urllib.request.urlopen(request).read().decode('utf-8')
        globalVal.getCount += 1
    except HTTPError as e:
        globalVal.saveTolog('The server couldn\'t fulfill the request.')
        globalVal.saveTolog('Error code:%s '% e.code)
    except URLError as e:
        globalVal.saveTolog('We failed to reach a server.')
        globalVal.saveTolog('Reason: %s'% e.reason)
    except Exception as e:
        globalVal.saveTolog(e)
    return content