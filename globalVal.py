# -*- coding: UTF-8 -*-
'''
    模块名称:GlobalVal
    功能:保存程序运行中所需要的变量/函数
    时间:2017-02-06
    作者:ptsph@foxmail.com
'''
from tkinter import *
# 验证码控件 避免局部变量被删除
global left_image
global mid_widget
global right_image
# 日志模块
global record_file
# 窗口控件 以便设置窗口参数
global root
# 验证码控件 设置为全局避免被函数[析构(c++)]
global image_label
global ocrCode_image
# 登录数据
global secretCode
global username
global password
# 用户的选择  选中是True 否则是False
global check_timetable
global check_myscore
global check_exam
global is_remember_pwd
# 默认选择框
global variable0
global variable1
global variable2
# 手动选择框
global check_timetable_val
global check_myscore_val
global check_exam_val
global foxlogin_version
global spider

# 将信息显示在窗口中的text控件
def showInText(showText):
    root.text['state'] = NORMAL
    root.text.insert(END, '>>'+showText+"\n")
    root.text.update()
    root.text['state'] = DISABLED
    root.text.see(END)
    pass

# 清除显示框中的数据
def clearShowInText():
    root.text['state'] = NORMAL
    root.text.delete('0.0', END)
    root.text.update()
    root.text['state'] = DISABLED
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


