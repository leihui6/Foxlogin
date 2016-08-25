#   SearchMyInfo.py
#   查找我的个人信息
#


import urllib.request
import urllib.parse
import globalVal

def getMyInfo(url):
    try:
        html=urllib.request.urlopen(url).read().decode('utf-8')
    except Exception as e:
        globalVal.saveTolog(e)
    return html