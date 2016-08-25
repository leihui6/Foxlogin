# 获取考试安排

import urllib.request
import urllib.parse
import globalVal

def getMyTest():
    PostUrl = "http://ssfw.tjut.edu.cn/ssfw/xsks/kcxx.do"

    headers = {
        # 'Host':'ssfw.tjut.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        # 'Accept': '*/*',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://ssfw.tjut.edu.cn/ssfw/xsks/kcxx.do',
        # 'Content-Length': '55',
        # 'Connection': 'keep-alive',
    }

    postData = {
        'xnxqdm': globalVal.check_test_val
    }
    content = ''
    try:
        Data = urllib.parse.urlencode(postData).encode()
        request = urllib.request.Request(PostUrl, Data, headers)
        content = urllib.request.urlopen(request).read().decode('utf-8')
        globalVal.getCount += 1
    except HTTPError as e:
        globalVal.saveTolog('The server couldn\'t fulfill the request.')
        globalVal.saveTolog('Error code: %s'% e.code)
    except URLError as e:
        globalVal.saveTolog('We failed to reach a server.')
        globalVal.saveTolog('Reason: %s'% e.reason)
    except Exception as e:
        globalVal.saveTolog(e)
    return  content


