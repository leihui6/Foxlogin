# -*- coding: UTF-8 -*-
'''
    模块名称:SaveFile
    功能:保存html页面,保存逻辑控制
    时间:2017-02-06
    作者:ptsph@foxmail.com
'''
import os
import GlobalVal

class SaveHtml:
    '''
        保存原则:
        相对路径为"学号/学期/文件名.html"
        - 初始化获取学号
        - 根据需要获取学期
        - 文件名在函数内部赋予

    '''
    save_path =''

    def __init__(self):
        self.save_path = './' + GlobalVal.username
        if os.path.exists(self.save_path) == False:
            os.makedirs(self.save_path)

    def save_as_score(self,html):
        last_dirnmae = GlobalVal.year2easyRead(GlobalVal.check_myscore_val)
        if os.path.exists(self.save_path +'\\'+last_dirnmae) == False:
            os.makedirs(self.save_path +'\\'+last_dirnmae)
        fileName='我在%s的成绩.html'%last_dirnmae
        open(self.save_path +'\\'+last_dirnmae+'\\' + fileName,'wb+').write(html.encode())

    def save_as_timetable(self,html):
        last_dirnmae = GlobalVal.year2easyRead(GlobalVal.check_timetable_val)
        if os.path.exists(self.save_path +'\\'+last_dirnmae) == False:
            os.makedirs(self.save_path +'\\'+last_dirnmae)
        fileName='我在%s的课表.html'%last_dirnmae
        open(self.save_path +'\\'+last_dirnmae+'\\' + fileName,'wb+').write(html.encode())

    def save_as_exam(self,html):
        last_dirnmae = GlobalVal.year2easyRead(GlobalVal.check_exam_val)
        if os.path.exists(self.save_path +'\\'+last_dirnmae) == False:
            os.makedirs(self.save_path +'\\'+last_dirnmae)
        fileName='我在%s的考试安排.html'%last_dirnmae
        open(self.save_path +'\\'+last_dirnmae+'\\' + fileName,'wb+').write(html.encode())
