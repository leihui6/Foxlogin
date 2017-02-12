# -*- coding: UTF-8 -*-
'''
    模块名称:GuiCtrl
    功能:GUI布局控制,登录逻辑控制
    时间:2017-02-06
    作者:ptsph@foxmail.com
'''
import GlobalVal
import subprocess
from tkinter.ttk import *
from tkinter import *
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import os
import shelve
import threading
import LoginSpider
from time import clock

# 加载左边图像
def loadLeftImgWidget():
    canvas = Canvas(GlobalVal.root, width=27, height=300)
    image_file2 = Image.open("image/index_left.gif")
    GlobalVal.left_image = ImageTk.PhotoImage(image_file2)
    canvas.create_image(0, 0, image=GlobalVal.left_image, anchor=NW)
    canvas.pack(side=LEFT,fill=Y,expand=NO)

# 加载右边图像
def loadRightImgWidget():
    canvas = Canvas(GlobalVal.root, width=632, height=300, bg='blue')
    image_file2 = Image.open("image/index_right.gif")
    GlobalVal.right_image = ImageTk.PhotoImage(image_file2)
    canvas.create_image(0, 0, image=GlobalVal.right_image, anchor=NW)
    canvas.pack(side=RIGHT, fill=Y, expand=NO)

# 加载中间登录模块
def loadLoginWidget(self):
    GlobalVal.mid_widget = Frame(self,width='100')
    # 登录控件布局
    loginFrm = Frame(GlobalVal.mid_widget)
    gPADX = 3
    gPADY = 4
    # 用户名输入模块
    userNameFrame = Frame(loginFrm)
    Label(userNameFrame, text='学　号').pack(side=LEFT,padx=gPADX)
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
    self.ocrCodeInput.bind('<Key-Return>', getUserInfo)
    self.ocrCodeInput.pack(side=LEFT)
    image_file = Image.open('image/init_img.jpg')
    GlobalVal.ocrCode_image = ImageTk.PhotoImage(image_file)
    GlobalVal.image_label = Label(Ocrframe, image=GlobalVal.ocrCode_image, width='68', height='22')
    GlobalVal.image_label.bind('<Button-1>', updateOcrCodeShow)
    GlobalVal.image_label.pack(side=LEFT, padx='5.5')
    Ocrframe.pack(side=TOP,padx=gPADX,pady=gPADY)
    # END验证码输入和显示模块

    # 登录操作模块
    loginOperatorFrame = Frame(loginFrm)

    # 设置复选框
    # 复选框
    def change_remember_state():
        if GlobalVal.is_remember_pwd == True:
            GlobalVal.is_remember_pwd = False
        else:
            GlobalVal.is_remember_pwd = True
    is_remember_pwd_button = Checkbutton(loginOperatorFrame, text='记住密码',command=lambda :change_remember_state())
    is_remember_pwd_button.select()
    is_remember_pwd_button.pack(side=LEFT, padx=gPADX)
    # END复选框模块

    # 登录按键
    self.loginbutton = Button(loginOperatorFrame, text='登录', width='20',relief='groove', command=lambda :getUserInfo(''))
    self.loginbutton.pack(side=LEFT, padx=gPADX)
    loginOperatorFrame.pack(side=TOP,padx=gPADX,pady=gPADY)
    # END登录按键模块

    loginFrm.pack(side=TOP,anchor=NW,pady=gPADY)
    return

# 加载中间复选框模块
def loadCheckButton(self):
    frm_check = Frame(GlobalVal.mid_widget)

    # 默认全部勾选
    GlobalVal.check_timetable = True
    GlobalVal.check_myscore = True
    GlobalVal.check_exam = True

    # 公共距离
    com_width = '15'
    com_padx = '3'
    com_pady = '3.5'
    choiceList = ["大四第一学期", "大四第二学期",
                  "大三第一学期", "大三第二学期",
                  "大二第一学期", "大二第二学期",
                  "大一第一学期", "大一第二学期"]
    # 获取课表选择模块
    frm_T = Frame(frm_check)
    # 1)复选框
    def check_timetable():
        if GlobalVal.check_timetable:
            GlobalVal.check_timetable = False
        else:
            GlobalVal.check_timetable = True
    c0 = Checkbutton(frm_T,text='获取我的课表',command=check_timetable)
    c0.select()
    c0.pack(side=LEFT,padx=com_padx)
    # 2)多选框
    GlobalVal.variable0 = StringVar(frm_T, '大三第一学期')
    self.w0 = Combobox(frm_T, textvariable=GlobalVal.variable0,values=choiceList, width=com_width)
    self.w0['state'] = 'readonly'
    self.w0.pack(side=LEFT, padx=com_padx)
    frm_T.pack(side=TOP,pady=com_pady)
    # END获取课表模块

    # 获取成绩选择模块
    frm_M = Frame(frm_check)
    # 复选框
    def check_myscore():
        if GlobalVal.check_myscore:
            GlobalVal.check_myscore = False
        else:
            GlobalVal.check_myscore = True
    c1 = Checkbutton(frm_M, text='获取我的成绩',command=check_myscore)
    c1.select()
    c1.pack(side=LEFT,padx=com_padx)
    # 多选框
    GlobalVal.variable1 = StringVar(frm_M, '大三第一学期')
    self.w1 = Combobox(frm_M, textvariable=GlobalVal.variable1,values=choiceList, width=com_width)
    self.w1['state'] = 'readonly'
    self.w1.pack(side=LEFT, padx=com_padx)
    frm_M.pack(side=TOP,pady=com_pady)
    # END成绩选择模块

    # 获取考试安排选择模块
    frm_B = Frame(frm_check)
    # 复选框
    def check_exam():
        if GlobalVal.check_exam:
            GlobalVal.check_exam = False
        else:
            GlobalVal.check_exam = True
    c2 = Checkbutton(frm_B, text='获取考试安排',command=check_exam)
    c2.select()
    c2.pack(side=LEFT,padx=com_padx)
    # 多选框
    GlobalVal.variable2 = StringVar(self, "大三第一学期")
    self.w2 = Combobox(frm_B, textvariable=GlobalVal.variable2,values=choiceList, width=com_width)
    self.w2['state'] = 'readonly'
    self.w2.pack(side=LEFT, padx=com_padx)
    frm_B.pack(side=TOP,pady=com_pady)
    # END考试安排选择模块

    # 复选框模块加载完毕
    frm_check.pack(side=TOP,pady='2',anchor=NW)
    return

# 加载中间显示模块
def loadShowWidget(self):
    self.text = Text(GlobalVal.mid_widget,width='35',height='3',bg='black',fg='#7FFF00 ')
    self.text.focus_set()
    self.text.pack(side=LEFT)
    GlobalVal.showInText('Welcome to %s'%GlobalVal.foxlogin_version)
    GlobalVal.mid_widget.pack(side=LEFT,expand=NO)
    return

# 加载用户登录信息
def loadLoginInfo (self):
    # 填充学号密码
    self.usernameInput.insert(0, GlobalVal.username)
    self.userpwdInput.insert(0, GlobalVal.password)
    # 更新验证码
    updateOcrCodeShow('')

# 查看结果
def lookResult():
    GlobalVal.username = GlobalVal.root.usernameInput.get()
    if not os.path.exists(GlobalVal.username):
        m_title = "查看结果"
        m = '找不到 \' %s \' 的获取结果'% GlobalVal.username
        messagebox.showwarning(m_title, m)
    else:
        def sub_lookResult():
            subprocess.call('explorer %s' % GlobalVal.username)
        t_lookResult = threading.Thread(target=sub_lookResult, name='sub_lookResult')
        t_lookResult.start()

# 加载菜单模块
def loadMenuWidget():
    menubar = Menu(GlobalVal.root)
    Look = Menu(menubar, tearoff=0)
    Look.add_command(label="查看结果", command=lookResult)

    # 查看
    menubar.add_cascade(label="查看", menu=Look)
    About = Menu(menubar, tearoff=0)
    About.add_command(label="关于Foxlogin",command=showAbout)
    About.add_separator()
    About.add_command(label="退出",command=proQuit)

    # 关于
    menubar.add_cascade(label="关于", menu=About)
    GlobalVal.root.config(menu=menubar)
    return

# 设置窗口属性
def setProcperty(root):
    root.geometry('%dx%d+200+100' % (910, 320))
    root.title(GlobalVal.foxlogin_version)
    root.iconbitmap('image/code_icon.ico')
    root.resizable(False, False)
    return

# 显示菜单弹窗
def showAbout ():
    m_title = "about\'Foxlogin\'"
    m = 'Only for 天津理工大学\n\nVersion:%s\n\nSource Code From:github.com/CallMePlus\n\nAll rights reserved'%GlobalVal.foxlogin_version
    messagebox.showinfo(m_title, m)
    return

# 退出操作
def proQuit():
    GlobalVal.record_file.close()
    GlobalVal.root.quit()
    return

# 开始登录 登录触发
def getUserInfo(event):
    GlobalVal.clearShowInText()

    # 获取登录的所有信息 复选框数据已经在全局变量中保存
    GlobalVal.username = GlobalVal.root.usernameInput.get()
    GlobalVal.password = GlobalVal.root.userpwdInput.get()
    GlobalVal.secretCode = GlobalVal.root.ocrCodeInput.get()

    # 检测学号,密码,验证码合法性
    if errorCheck() != True:
        return

    # 获取多选框的内容
    GlobalVal.check_timetable_val = GlobalVal.easyRead2Year(GlobalVal.root.w0.get())
    GlobalVal.check_myscore_val= GlobalVal.easyRead2Year(GlobalVal.root.w1.get())
    GlobalVal.check_exam_val= GlobalVal.easyRead2Year(GlobalVal.root.w2.get())

    GlobalVal.showInText("Connect......")
    login_result = GlobalVal.spider.login()
    if login_result[0] == False:
        GlobalVal.showInText("error %s"%login_result[1])
        return
    # 正式登录
    GlobalVal.showInText("Connected.")
    updateToShelve()
    launch()

# 错误检查 并给予提示
def errorCheck():
    # 用户名需要在 5-15 位 并且为 数字
    if (not (5 < len(GlobalVal.username) < 15 ) ) or (not GlobalVal.username.isdigit()):
        GlobalVal.showInText("请输入规范的用户名")
        return False

    # 密码需要大于6位
    if len(GlobalVal.password) < 6:
        GlobalVal.showInText("请输入规范的密码")
        return False

    # 验证码需要等于4位
    if len(GlobalVal.secretCode) != 4:
        GlobalVal.showInText("请输入正确的验证码")
        return False

    return True

# 更新验证码
def updateOcrCodeShow(event):
    GlobalVal.spider = LoginSpider.Spider()
    get_result = GlobalVal.spider.get_valid_code()
    if get_result == False:
        return
    image_file = Image.open('image/img.jpg')
    GlobalVal.ocrCode_image = ImageTk.PhotoImage(image_file)
    GlobalVal.image_label['image'] = GlobalVal.ocrCode_image
    GlobalVal.image_label.pack(side=LEFT, padx='5.5')
    return

# 更新本地数据
def updateToShelve():
    GlobalVal.username = GlobalVal.root.usernameInput.get()
    GlobalVal.password = GlobalVal.root.userpwdInput.get()

    # 所有状态复位
    for item in GlobalVal.record_file.items():
        item[1]['is_remember_pwd'] = False

    # 需要更新数据
    if GlobalVal.is_remember_pwd == True:
        # 本地已经存在用户数据
        if GlobalVal.username in GlobalVal.record_file.keys():
            GlobalVal.record_file[GlobalVal.username]['is_remember_pwd'] = True
            GlobalVal.record_file[GlobalVal.username]['user_password'] = GlobalVal.password
        # 本地存在用户数据需要创建用户数据
        else:
            need_update_info = {}
            need_update_info['user_password'] = GlobalVal.password
            need_update_info['is_remember_pwd'] = True
            GlobalVal.record_file[GlobalVal.username] = need_update_info
            print('保存本地数据,新建用户信息')

    # 写回到硬盘
    GlobalVal.record_file.sync()
    return

# 开始进入登录流程
def launch():
    '''
    print("学　号:", GlobalVal.username)
    print("密　码:", GlobalVal.password)
    print("验证码:", GlobalVal.secretCode)
    print("记住密码", GlobalVal.is_remember_pwd)
    print("我的课表:", GlobalVal.check_timetable_val, '状态:', GlobalVal.check_timetable)
    print("我的成绩:", GlobalVal.check_myscore_val, '状态:', GlobalVal.check_myscore)
    print("考试安排:", GlobalVal.check_exam_val, '状态:', GlobalVal.check_exam)
	'''
    start_time = clock()

    thread_timetable = ''
    if GlobalVal.check_timetable:
        GlobalVal.showInText('Download timetable....')
        thread_timetable = threading.Thread(target=LoginSpider.walk_with_timetable,name='get_timetable')
        thread_timetable.start()

    thread_exam=''
    if GlobalVal.check_exam_val:
        GlobalVal.showInText('Download exam ....')
        thread_exam = threading.Thread(target=LoginSpider.walk_with_exam,name='get_exam')
        thread_exam.start()

    thread_score=''
    if GlobalVal.check_myscore:
        GlobalVal.showInText('Download score....')
        thread_score = threading.Thread(target=LoginSpider.walk_with_score, name='get_score')
        thread_score.start()

    if GlobalVal.check_timetable:
        thread_timetable.join()
    if GlobalVal.check_exam_val:
        thread_exam.join()
    if GlobalVal.check_myscore:
        thread_score.join()

    # 结束操作
    GlobalVal.showInText('Done.')
    end_time = clock()
    GlobalVal.showInText('Speed time:%s s'% str(end_time-start_time)[:5])
    GlobalVal.showInText('查看->查看结果')
    updateOcrCodeShow('')
    return

#  提前加载  检查目录是否存在
def preLoad():
    GlobalVal.foxlogin_version = 'Foxlogin 2.0.2.2017'
    # 检查data目录是否存在 创建本地记录文件
    record_file_opened = False
    if not os.path.exists('data'):
        os.mkdir('data')
        # 并且创建一个本地记录文件
        GlobalVal.record_file= shelve.open("data/user_info.dat",writeback=True)
        record_file_opened = True
        GlobalVal.is_remember_pwd = False
        user_info = {'is_remember_pwd':False,'user_password':''}
        GlobalVal.record_file[''] = user_info
    if record_file_opened == False:
        GlobalVal.record_file = shelve.open("data/user_info.dat",writeback=True)

    # 检查image中关键文件是否存在
    if \
            not os.path.exists('image/code_icon.ico') \
            or \
            (not os.path.exists('image/init_img.jpg'))\
            or \
            (not os.path.exists('image/index_left.gif')) \
            or \
            (not os.path.exists('image/index_right.gif')):
        messagebox.showerror ('很严重的提示', '缺失关键文件,请从源获取完整文件')
        GlobalVal.record_file.close()
        GlobalVal.root.quit()
        exit()

    # 根据本地记录文件填充密码 默认记住密码
    GlobalVal.is_remember_pwd = True
    for item in GlobalVal.record_file.items():
        if item[1]['is_remember_pwd'] == True:
            GlobalVal.username = item[0]
            GlobalVal.password = item[1]['user_password']
            GlobalVal.is_remember_pwd = True
            return
    GlobalVal.username = ''
    GlobalVal.password = ''
    return

def loadMiddleWidget():
    loadLoginWidget(GlobalVal.root)
    loadCheckButton(GlobalVal.root)
    loadShowWidget(GlobalVal.root)
    loadLoginInfo(GlobalVal.root)