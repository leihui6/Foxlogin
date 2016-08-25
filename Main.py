# coding=utf-8
# encoding utf-8

import globalVal
import SimuLogin_
import LoginSucc
import subprocess

from tkinter.ttk import *
from tkinter import *
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk

import os
import time
import shelve
import socket
import threading

# 加载左边图像
def loadLeftImgWidget():
    canvas = Canvas(globalVal.root, width=27, height=300)
    image_file2 = Image.open("image/index_left.gif")
    globalVal.left_image = ImageTk.PhotoImage(image_file2)
    canvas.create_image(0, 0, image=globalVal.left_image, anchor=NW)
    canvas.pack(side=LEFT,fill=Y,expand=NO)

# 加载右边图像
def loadRightImgWidget():
    canvas = Canvas(globalVal.root, width=632, height=300, bg='blue')
    image_file2 = Image.open("image/index_right.gif")
    globalVal.right_image = ImageTk.PhotoImage(image_file2)
    canvas.create_image(0, 0, image=globalVal.right_image, anchor=NW)
    canvas.pack(side=RIGHT, fill=Y, expand=NO)

# 加载中间登录模块
def loadLoginWidget(self):

    globalVal.mid_widget = Frame(self,width='100')
    # 登录控件布局
    loginFrm = Frame(globalVal.mid_widget)
    gPADX = 3
    gPADY = 4
    # 用户名输入模块
    userNameFrame = Frame(loginFrm)
    Label(userNameFrame, text='用户名').pack(side=LEFT,padx=gPADX)
    self.usernameInput = Entry(userNameFrame)
    self.usernameInput.pack(side=LEFT)
    userNameFrame.pack(side=TOP,pady=gPADY)
    # END用户名输入模块

    # 用户密码输入模块
    userpwdFrame = Frame(loginFrm)
    Label(userpwdFrame, text='密　码').pack(side=LEFT,padx=gPADX)
    self.userpwdInput = Entry(userpwdFrame, show='*')
    self.userpwdInput.pack(side=LEFT)
    userpwdFrame.pack(side=TOP,pady=gPADY)
    # END用户密码输入模块

    # 验证码输入模块 包括输入框和显示Label
    Ocrframe = Frame(loginFrm)
    # 验证码输入框
    Label(Ocrframe, text='验证码').pack(side=LEFT,padx=gPADX)
    self.ocrCodeInput = Entry(Ocrframe, width='8')
    self.ocrCodeInput.bind('<Key-Return>', getuserinfo)
    self.ocrCodeInput.pack(side=LEFT)

    # 加载验证码
    def loadOcrCodeShow():
        # 开启线程 带cookie获取验证码 并保存
        # 等待线程结束
        # 检查是否保存即可
        thread_getOcrCode = threading.Thread(target=SimuLogin_.getOcrCode, name='getOcrCode')
        globalVal.getSecretCodeed = 0
        thread_getOcrCode.start()
        # 检查是否已经获取验证码
        while globalVal.getSecretCodeed == 0:
            thread_getOcrCode.join(1)

    # 结束loadOcrCodeShow() 函数
    loadOcrCodeShow()

    # 验证码成功加载
    if globalVal.getSecretCodeed == 1:
        image_file = Image.open('image/img.jpg')
        globalVal.ocrCode_image = ImageTk.PhotoImage(image_file)
        globalVal.image_label = Label(Ocrframe, image=globalVal.ocrCode_image, width='68', height='22')
        globalVal.image_label.bind('<Button-1>',updateOcrCodeShow)
        globalVal.image_label.pack(side=LEFT, padx='5.5')
    # 验证码加载失败 表示网络异常
    elif globalVal.getSecretCodeed == -1:
        # 打开验证码文件以显示出来
        image_file = Image.open('image/fail_img.jpg')
        globalVal.ocrCode_image = ImageTk.PhotoImage(image_file)
        globalVal.image_label = Label(Ocrframe, image=globalVal.ocrCode_image, width='68', height='22')
        globalVal.image_label.pack(side=LEFT, padx='5.5')
        m_title = "很悲伤的提示"
        m = "找不到网络呀..."
        messagebox.showerror(m_title, m)

    Ocrframe.pack(side=TOP,padx=gPADX,pady=gPADY)
    # END验证码输入和显示模块

    # 登录操作模块
    loginOperatorFrame = Frame(loginFrm)
    # 复选框
    def check_remmber_pwd():
        if globalVal.check_remmber_pwd:
            globalVal.check_remmber_pwd = False
            calSaveToShelve()
        else:
            globalVal.check_remmber_pwd = True
            saveToShelve()

    # 结束 check_remmber_pwd() 函数
    check_remmber_pwd_button = Checkbutton(loginOperatorFrame, text='记住密码',command=check_remmber_pwd)
    # 根据加载的布尔值来智能显示
    if globalVal.check_remmber_pwd:
        check_remmber_pwd_button.select()
        self.usernameInput.insert(0,globalVal.username)
        self.userpwdInput.insert(0, globalVal.password)
    else:
        pass
    check_remmber_pwd_button.pack(side=LEFT, padx=gPADX)
    # 登录按键
    self.loginbutton = Button(loginOperatorFrame, text='登录', width='20',relief='groove', command=lambda:getuserinfo(0))
    self.loginbutton.pack(side=LEFT, padx=gPADX)

    loginOperatorFrame.pack(side=TOP,padx=gPADX,pady=gPADY)
    # END登录按键模块

    loginFrm.pack(side=TOP,anchor=NW,pady=gPADY)
    pass

# 加载中间复选框模块
def loadCheckButton(self):

    frm_check = Frame(globalVal.mid_widget)

    # 默认全部勾选
    globalVal.check_timetable = True
    globalVal.check_myscore = True
    globalVal.check_test = True

    # 公共距离
    com_width = '15'
    com_padx = '3'
    com_pady = '3.5'
    choiceList = ["大三第一学期", "大三第二学期",
                  "大四第一学期", "大四第二学期",
                  "大二第一学期", "大二第二学期",
                  "大一第一学期", "大一第二学期"]
    # 获取课表选择模块
    frm_T = Frame(frm_check)
        #复选框
    def check_timetable():
        if globalVal.check_timetable:
            globalVal.check_timetable = False
            globalVal.wantCount -= 1
        else:
            globalVal.check_timetable = True
            globalVal.wantCount += 1

    c0 = Checkbutton(frm_T,text='获取我的课表',command=check_timetable)
    c0.select()
    c0.pack(side=LEFT,padx=com_padx)
        #多选框
    globalVal.variable0 = StringVar(frm_T, '大三第一学期')
    self.w0 = Combobox(frm_T, textvariable=globalVal.variable0,
                       values=choiceList, width=com_width)
    self.w0['state'] = 'readonly'
    self.w0.pack(side=LEFT, padx=com_padx)

    frm_T.pack(side=TOP,pady=com_pady)

    # 获取成绩选择模块
    frm_M = Frame(frm_check)
        # 复选框
    def check_myscore():
        if globalVal.check_myscore:
            globalVal.wantCount -= 1
            globalVal.check_myscore = False
        else:
            globalVal.wantCount += 1
            globalVal.check_myscore = True
    c1 = Checkbutton(frm_M, text='获取我的成绩',command=check_myscore)
    c1.select()
    c1.pack(side=LEFT,padx=com_padx)

        # 多选框
    globalVal.variable1 = StringVar(frm_M, '大三第一学期')
    self.w1 = Combobox(frm_M, textvariable=globalVal.variable1,
                       values=choiceList, width=com_width)
    self.w1['state'] = 'readonly'
    self.w1.pack(side=LEFT, padx=com_padx)

    frm_M.pack(side=TOP,pady=com_pady)

    # 获取考试安排选择模块
    frm_B = Frame(frm_check)
        # 复选框
    def check_test():
        if globalVal.check_test:
            globalVal.wantCount -= 1
            globalVal.check_test = False
        else:
            globalVal.wantCount += 1
            globalVal.check_test = True
    c2 = Checkbutton(frm_B, text='获取考试安排',command=check_test)
    c2.select()
    c2.pack(side=LEFT,padx=com_padx)
        # 多选框
    globalVal.variable2 = StringVar(self, "大三第一学期")
    self.w2 = Combobox(frm_B, textvariable=globalVal.variable2,
                       values=choiceList, width=com_width)
    self.w2['state'] = 'readonly'
    self.w2.pack(side=LEFT, padx=com_padx)

    frm_B.pack(side=TOP,pady=com_pady)

    # 复选框模块加载完毕
    frm_check.pack(side=TOP,pady='2',anchor=NW)
    pass

# 加载中间显示模块
def loadShowWidget(self):
    self.text = Text(globalVal.mid_widget,width='35',height='3')
    self.text.focus_set()
    self.text.pack(side=LEFT)
    globalVal.showInText('Foxlogin提示框')
    globalVal.mid_widget.pack(side=LEFT,expand=NO)
    pass

def lookLog():
    globalVal.logFile.flush()
    def sub_lookLog():
        subprocess.call('notepad data/log.log')
    t_lookLog = threading.Thread(target=sub_lookLog, name='sub_lookLog')
    t_lookLog.start()

def lookResult():
    globalVal.username = globalVal.root.usernameInput.get()
    if not os.path.exists(globalVal.username):
        m_title = "查看结果"
        m = '找不到 \' %s \' 的获取结果'% globalVal.username
        messagebox.showwarning(m_title, m)
    else:
        def sub_lookResult():
            subprocess.call('explorer %s' % globalVal.username)
        t_lookResult = threading.Thread(target=sub_lookResult, name='sub_lookResult')
        t_lookResult.start()

# 加载菜单模块
def loadMenuWidget():
    menubar = Menu(globalVal.root)

    Look = Menu(menubar, tearoff=0)
    Look.add_command(label="查看结果", command=lookResult)
    Look.add_command(label="查看日志(deBug)", command=lookLog)
    # 查看
    menubar.add_cascade(label="查看", menu=Look)
    About = Menu(menubar, tearoff=0)
    About.add_command(label="关于Foxlogin",command=showAbout)
    About.add_separator()
    About.add_command(label="退出",command=proQuit)
    # 关于
    menubar.add_cascade(label="关于", menu=About)

    globalVal.root.config(menu=menubar)

# 设置窗口属性
def setProcperty(root):
    root.geometry('%dx%d+200+100' % (910, 320))
    root.title("Foxlogin(V1.0.0.8.2016)")
    root.iconbitmap('image/code_icon.ico')
    root.resizable(False, False)

# 显示菜单弹窗
def showAbout ():
    m_title = "关于\'Foxlogin\'"
    m = 'Foxlogin \nV1.0.0.8.2016(天津理工大学专属)\n\n@鲸鱼和Plus 保留所有权\n\n本软件仅限于个人使用' \
        '\n\n我们不允许任何人以任何形式将此软件用于商业用途\n\n感谢学校服务器提供的支持,Foxlogin于2016年9月停止维护\nfind_by_u@163.com'
    messagebox.showinfo(m_title, m)

# 退出操作
def proQuit():
    globalVal.shelveFile.close()
    globalVal.logFile.close()
    globalVal.root.quit()

# 显示操作成功弹出
def showDoneInfo(doneShowStr):
    m_title = "来自Foxlogin的提醒"
    if globalVal.getCount == globalVal.wantCount:
        globalVal.saveTolog("<数据获取完整>")
        m = doneShowStr+'\n你选择获取的数据存储在\"%s/\"文件夹下\n\n查看->查看结果\n\n使用浏览器打开即可' % globalVal.username
        messagebox.showinfo(m_title, m)
    else:
        globalVal.saveTolog("<数据获取不完整>")
        m = doneShowStr + '\n<数据获取不完整>\n你选择获取的数据存储在\"%s/\"文件夹下\n\n查看->查看结果\n\n使用浏览器打开即可' % globalVal.username
        messagebox.showwarning(m_title, m)

# 开始登录 登录触发
def getuserinfo(event):
    globalVal.clearShowInText()
    # 获取登录的所有信息 复选框数据已经在全局变量中保存
    globalVal.username =globalVal.root.usernameInput.get()
    globalVal.password =globalVal.root.userpwdInput.get()
    globalVal.secretCode = globalVal.root.ocrCodeInput.get()

    # 检测学号不能为空  而且要是20开头
    if '20' not in globalVal.username:
        globalVal.showInText("学号不能为空")
        return

    # 获取多选框的内容
    globalVal.check_timetable_val = globalVal.easyRead2Year(globalVal.root.w0.get())
    globalVal.check_myscore_val= globalVal.easyRead2Year(globalVal.root.w1.get())
    globalVal.check_test_val= globalVal.easyRead2Year(globalVal.root.w2.get())

    # 写入日志输出校检
    globalVal.saveTolog("用户名:%s" % globalVal.username)
    globalVal.saveTolog("记住密码:%s" % globalVal.check_remmber_pwd)
    globalVal.saveTolog("我的课表:%s, 状态:%s" % (globalVal.check_timetable_val, globalVal.check_timetable))
    globalVal.saveTolog("我的成绩:%s, 状态:%s" % (globalVal.check_myscore_val, globalVal.check_myscore))
    globalVal.saveTolog("考试安排:%s, 状态:%s" % (globalVal.check_test_val, globalVal.check_test))

    # 输出到控制台检查数据
    '''
    print("用户名:", globalVal.username)
    print("密　码:", globalVal.password)
    print("验证码:", globalVal.secretCode)
    print("记住密码",globalVal.check_remmber_pwd)
    print("我的课表:",globalVal.check_timetable_val ,'状态:',globalVal.check_timetable)
    print("我的成绩:",globalVal.check_myscore_val,'状态:',globalVal.check_myscore)
    print("考试安排:",globalVal.check_test_val,'状态:',globalVal.check_test)
    '''
    # 错误检查
    if errorCheck(True):
        globalVal.showInText("正在尝试进入系统...")

        if globalVal.check_timetable:
            globalVal.showInText("准备获取课表...")
            pass
        if globalVal.check_myscore:
            globalVal.showInText("准备获取成绩...")
            pass
        if globalVal.check_test:
            globalVal.showInText("准备获取成绩...")
            pass
        # 开始登录
        updateToShelve()
        launch()
    else:
        pass

# 错误检查 并给予提示
def errorCheck(checkOcr):

    # 用户名需要在 5-15 位
    if (not (5 < len(globalVal.username) < 15 ) ) or (not globalVal.username.isdigit()):
        globalVal.showInText("请输入规范的用户名")
        return False

    # 密码需要大于6位
    if len(globalVal.password) < 6:
        globalVal.showInText("请输入规范的密码")
        return False

    if checkOcr:
        # 验证码需要等于4位
        if len(globalVal.secretCode) != 4:
            globalVal.showInText("请输入正确的验证码")
            return False

    globalVal.check_timetable_val = globalVal.easyRead2Year(globalVal.root.w0.get())
    globalVal.check_myscore_val = globalVal.easyRead2Year(globalVal.root.w1.get())
    globalVal.check_test_val = globalVal.easyRead2Year(globalVal.root.w2.get())

    # 检查获取的年份
    intusername = int(globalVal.username[0:4])
    if int(globalVal.check_timetable_val[0:4]) < intusername:
        globalVal.showInText("获取我的课表(0):请选择正确的时间段")
        return False
    if int(globalVal.check_myscore_val[0:4]) <  intusername:
        globalVal.showInText("获取我的成绩(1):请选择正确的时间段")
        return False
    if int(globalVal.check_test_val[0:4]) < intusername:
        globalVal.showInText("获取考试安排(2):请选择正确的时间段")
        return False

    return True


# 更新验证码
def updateOcrCodeShow(event):
    globalVal.showInText("正在更新验证码...")
    # 开启线程 带cookie获取验证码 并保存
    # 等待线程结束
    # 检查是否保存即可
    thread_getOcrCode = threading.Thread(target=SimuLogin_.getOcrCode, name='getOcrCode')
    thread_getOcrCode.start()
    globalVal.getSecretCodeed = 0
    # 检查是否已经获取验证码
    while globalVal.getSecretCodeed == 0:
        thread_getOcrCode.join(1)

    # 检查更新验证码状态
    if globalVal.getSecretCodeed == 1:
        # 打开验证码文件以显示出来
        image_file = Image.open('image/img.jpg')
        globalVal.ocrCode_image = ImageTk.PhotoImage(image_file)
        globalVal.image_label['image'] = globalVal.ocrCode_image
        globalVal.image_label.pack(side=LEFT, padx='5.5')
    elif globalVal.getSecretCodeed == -1:
        # 打开验证码文件以显示出来
        image_file = Image.open('image/fail_img.jpg')
        globalVal.ocrCode_image = ImageTk.PhotoImage(image_file)
        globalVal.image_label['image'] = globalVal.ocrCode_image
        globalVal.image_label.pack(side=LEFT, padx='5.5')
        globalVal.showInText("更新验证码失败!")
        m_title = "很悲伤的提示"
        m = "找不到网络呀..."
        messagebox.showerror(m_title, m)
    globalVal.showInText("验证码更新完毕")

# 保留用户信息
def saveToShelve():
    globalVal.username = globalVal.root.usernameInput.get()
    globalVal.password = globalVal.root.userpwdInput.get()

    if errorCheck(False):
        globalVal.shelveFile = shelve.open('data/data.dat', writeback=True)
        # 检查是否已经存在在本地文件中

        # 已经存在在本地文件中
        if globalVal.username in globalVal.shelveFile.keys():
            globalVal.shelveFile[globalVal.username]['ifRemmberPwd'] = True

        # 不存在在本地文件中
        else:
            operateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            netinfo = socket.gethostbyname_ex(socket.gethostname())

            person = {}
            person['username'] = globalVal.username
            person['password'] = globalVal.password
            person['time'] = operateTime
            person['netinfo'] = netinfo
            person['ifRemmberPwd'] = True
            globalVal.shelveFile[globalVal.username] = person
        # end if
        globalVal.shelveFile.close()
        # globalVal.showInText('已记住啦！下次登录时无需输入账号密码')
    else:
        # globalVal.showInText('无法记住异常数据')
        pass
# 取消保留
def calSaveToShelve():
    globalVal.shelveFile = shelve.open('data/data.dat',writeback=True)
    for item in globalVal.shelveFile.items():
        globalVal.shelveFile[item[0]]['ifRemmberPwd'] = False
        # print(item)
    globalVal.shelveFile.close()

# 更新本地数据
def updateToShelve():
    globalVal.shelveFile = shelve.open('data/data.dat', writeback=True)
    globalVal.username = globalVal.root.usernameInput.get()
    globalVal.password = globalVal.root.userpwdInput.get()
    operateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    netinfo = socket.gethostbyname_ex(socket.gethostname())

    if globalVal.username in globalVal.shelveFile.keys():
        globalVal.shelveFile[globalVal.username]['ifRemmberPwd'] = globalVal.check_remmber_pwd
        globalVal.shelveFile[globalVal.username]['password'] = globalVal.password
        globalVal.shelveFile[globalVal.username]['time'] = operateTime
        globalVal.shelveFile[globalVal.username]['netinfo'] = netinfo
    else:
        # 先取消全部记住密码
        for item in globalVal.shelveFile.items():
            globalVal.shelveFile[item[0]]['ifRemmberPwd'] = False

        # 记住特殊密码
        person = {}
        person['username'] = globalVal.username
        person['password'] = globalVal.password
        person['time'] = operateTime
        person['netinfo'] = netinfo
        person['ifRemmberPwd'] = True
        globalVal.shelveFile[globalVal.username] = person

    globalVal.shelveFile.close()

# 开始进入登录流程
def launch():

    globalVal.saveTolog('------开始登录------')
    lauch_time0 = time.time()

    # 开始模拟登录
    virLogin_flag = SimuLogin_.virLogin()

    # 0是用户密码错误
    if virLogin_flag == 0:
        thread_updateOrcCode = threading.Thread(target=updateOcrCodeShow,args=('', ), name='updateOrcCode')
        thread_updateOrcCode.start()
        m = '用户名和密码不匹配'
        messagebox.showwarning('提示', m)
        globalVal.saveTolog('------登录账号密码不匹配------')
        pass
    # 1是验证码错误
    elif virLogin_flag == 1:
        thread_updateOrcCode = threading.Thread(target=updateOcrCodeShow,args=('', ), name='updateOrcCode')
        thread_updateOrcCode.start()
        m = '验证码错误'
        messagebox.showwarning('提示', m)
        globalVal.saveTolog('------登录验证码错误------')
        pass
    # 登录成功
    if virLogin_flag == 2:

        # 登录成功后的获取信息操作
        LoginSucc.loginSucc()

        globalVal.showInText("%s的数据获取完毕" % globalVal.username)

        # 开启线程获取验证码
        thread_updateOrcCode = threading.Thread(target=updateOcrCodeShow,args=('', ), name='updateOrcCode')
        thread_updateOrcCode.start()

        # 完成直接打开文件夹
        lookResult()

        # 提示获取成功
        doneShowStr = "全程耗时:%s 秒" % (str(time.time() - lauch_time0)[:5])
        showDoneInfo(doneShowStr)

        # 获取文件数置为0
        globalVal.getCount = 0
        globalVal.saveTolog('------登录完成------')
        pass
    # 异常
    if virLogin_flag == 3:
        thread_updateOrcCode = threading.Thread(target=updateOcrCodeShow,args=('', ), name='updateOrcCode')
        thread_updateOrcCode.start()
        m = '异常\n若多次尝试异常请将\'data/log.log\'文件反馈给我们\n(O ^ ~ ^ O)\n于2016-08-25停止维护 '
        messagebox.showerror ('提示', m)
        globalVal.saveTolog('------登录异常------')
        pass
    return

#  提前加载  检查目录是否存在
def preLoad():
    globalVal.getCount = 0
    globalVal.wantCount = 3

    # 检查是否有360
    import os
    globalVal.tasklist = '没有'

    def sub_tasklist():
        globalVal.tasklist = str(os.popen('tasklist /fi "imagename eq 360Tray.exe \nexit" ').readlines())
    t_tasklist = threading.Thread(target=sub_tasklist, name='t_sub_tasklist')
    t_tasklist.start()
    t_tasklist.join(1)

    if not ("没有" in globalVal.tasklist):
        m = '未知错误'
        messagebox.showerror('未知错误', m)
        globalVal.root.quit()
        exit()

    # 检查data目录是否存在
    if not os.path.exists('data'):
        os.mkdir('data')
    # 打开并创建文件
    globalVal.shelveFile = shelve.open("data/data.dat")
    globalVal.logFile = open('data/log.log', mode='a+')

    # 检查image中关键文件是否存在
    if \
            not os.path.exists('image/code_icon.ico') \
            or \
            (not os.path.exists('image/fail_img.jpg'))\
            or \
            (not os.path.exists('image/index_left.gif')) \
            or \
            (not os.path.exists('image/index_right.gif')):
        globalVal.saveTolog('缺失关键文件,请从源获取完整文件')
        m = '缺失关键文件,请从源获取完整文件'
        messagebox.showerror ('很严重的提示', m)
        globalVal.root.quit()
        exit()

    # 检查css目录 和 文件数目
    if not os.path.exists('css') or len(os.listdir('css')) != 27:
        globalVal.saveTolog('缺失css文件,请从源获取完整文件,以达到最佳显示效果')
        m = '缺失css文件,请从源获取完整文件,以达到最佳显示效果'
        messagebox.showwarning('温馨提示', m)

    # 检查是否需要记住密码
    globalVal.check_remmber_pwd = False
    for item in globalVal.shelveFile.items():
        if globalVal.shelveFile[item[0]]['ifRemmberPwd']:
            # print(item)
            globalVal.username = globalVal.shelveFile[item[0]]['username']
            globalVal.password = globalVal.shelveFile[item[0]]['password']
            globalVal.check_remmber_pwd = True
    globalVal.shelveFile.close()
    pass

    thread_getBackGround = threading.Thread(target=SimuLogin_.getBackGround, name='getBackGround')
    thread_getBackGround.start()


# 执行代码
if __name__ == "__main__":


    globalVal.root = Tk()
    preLoad()
    setProcperty(globalVal.root)
    loadMenuWidget()
    loadLeftImgWidget()
    loadLoginWidget(globalVal.root)
    loadCheckButton(globalVal.root)
    loadShowWidget(globalVal.root)
    loadRightImgWidget()
    globalVal.root.mainloop()
