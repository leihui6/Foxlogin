# -*- coding: UTF-8 -*-
'''
    模块名称:Main
    功能:程序运行入口
    时间:2017-02-06
    作者:ptsph@foxmail.com
'''
import GuiCtrl
import GlobalVal
from tkinter import *


# 执行代码
if __name__ == "__main__":
    GlobalVal.root = Tk()
    # 文件预校检
    GuiCtrl.preLoad()
    # GUI属性设置
    GuiCtrl.setProcperty(GlobalVal.root)
    # 加载菜单栏
    GuiCtrl.loadMenuWidget()
    # 左边视图
    GuiCtrl.loadLeftImgWidget()
    # 中间视图
    GuiCtrl.loadMiddleWidget()
    # 右边视图
    GuiCtrl.loadRightImgWidget()
    GlobalVal.root.mainloop()
