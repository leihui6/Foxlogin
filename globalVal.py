# coding=utf-8
import time
from tkinter import *
# 验证码控件 避免局部变量被删除
global left_image
global mid_widget
global right_image

# 日志模块
global shelveFile
global logFile
# 登录的反馈信息
global loginflag

# 实际获取到的数据量
global getCount
# 期望获取到的数据量
global wantCount

# cmd 中开启了子进程 数据共享使用
global tasklist

# 窗口控件 以便设置窗口参数
global root

# 验证码控件 设置为全局避免被函数[析构(c++)]
global image_label
global ocrCode_image

# 登录数据
global secretCode
global username
global password
global opener

# 是否获取到了验证码
global getSecretCodeed

# 用户的选择  选中是True 否则是False
global check_timetable
global check_myscore
global check_test
global check_remmber_pwd
# 默认选择框
global variable0
global variable1
global variable2
# 手动选择框
global check_timetable_val
global check_myscore_val
global check_test_val

global today

# 将信息显示在窗口中的text控件
def showInText(showText):
    root.text['state'] = NORMAL
    root.text.insert(END, '>'+showText+"\n")
    root.text.update()
    root.text['state'] = DISABLED
    root.text.see(END)
    pass

def clearShowInText():
    root.text['state'] = NORMAL
    root.text.delete('0.0', END)
    root.text.update()
    root.text['state'] = DISABLED
    pass

def saveTolog(text):
    operateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logFile.write(operateTime+" # "+str(text)+'\n')
    logFile.flush()
    pass

def year2easyRead(termYear):
    termYear = termYear.split('-')
    return '大'+year2Word(int(termYear[1])- int(username[0:4]))+ ' 第'+year2Word(int(termYear[2]))+'学期'


def easyRead2Year(termYear):
    start = int(username[0:4]) + year2Word(termYear[1]) - 1
    end = start + 1
    term = year2Word(termYear[3])
    return str(start) + '-' + str(end) +'-'+str(term)

def year2Word(year):
    if year == 1:
        return '一'
    elif year == 2:
        return '二'
    elif year == 3:
        return '三'
    elif year == 4:
        return '四'

    if year == '一':
        return 1
    elif year == '二':
        return 2
    elif year == '三':
        return 3
    elif year == '四':
        return 4


