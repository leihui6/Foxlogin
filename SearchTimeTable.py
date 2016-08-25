# coding=utf-8
#   SearchTimeTable.py
#   查找课程表
#   2016年8月6日

#   sYear:开始学年
#   eYear:结束学年
#   term:学期 如1
#   http://ssfw.tjut.edu.cn/ssfw/pkgl/kcbxx/4/ 中的4 代表学生的课表 2是老师的课表


import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError

import globalVal

def getTimeTable():
    html = ''
    try:
        url = "http://ssfw.tjut.edu.cn/ssfw/pkgl/kcbxx/4/"
        searchUrl = (url+ globalVal.check_timetable_val)
        html=urllib.request.urlopen(searchUrl).read().decode('utf-8')
        globalVal.getCount += 1
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    except Exception as e:
        globalVal.saveTolog(e)
    return html