# -*- coding: UTF-8 -*-
'''
    模块名称:LoginSpider
    功能:爬虫逻辑控制
    时间:2017-02-06
    作者:ptsph@foxmail.com
'''
import requests
import random
import GlobalVal
import ProcessHtml
import SaveFile

class Spider:
    '''
        爬虫全部流程如下:
        - 建立session
        - 获取验证码
        - 从界面获取数据开始模拟登录
        - 个根据用户选择爬取课表/考试安排/成绩
    '''
    # 公共header
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # 验证码url
    valid_code_url = "http://ssfw.tjut.edu.cn/ssfw/jwcaptcha.do?"
    # 登录主页url
    home_url = "http://ssfw.tjut.edu.cn/ssfw/j_spring_ids_security_check"
    # 获取我的成绩的url
    socre_url = "http://ssfw.tjut.edu.cn/ssfw/zhcx/cjxx.do"
    # 获取我的考试安排的url
    exam_url = "http://ssfw.tjut.edu.cn/ssfw/xsks/kcxx.do"
    # 获取课程表的url
    timetable_url = 'http://ssfw.tjut.edu.cn/ssfw/pkgl/kcbxx/4/'

    # requests 会话对象
    __session = 0

    def __init__(self):
        self.__session = requests.Session()

    def get_valid_code(self):
        valid_code_url_tmp = self.valid_code_url + str(random.randint(0,100))
        try:
            picture = self.__session.get(valid_code_url_tmp,headers=self.header,timeout=12)
            open('image/img.jpg', 'wb').write(picture.content)
            return True
        # DNS failure, refused connection, etc
        except ConnectionError :
            GlobalVal.showInText('error:network disconnect.')
            return False
        # Timeout
        except TimeoutError:
            GlobalVal.showInText('error:time out(>12s).')
            return False
        # HTTPError
        except requests.HTTPError:
            GlobalVal.showInText('error:http requests.')
            return False
        # File write or read
        except IOError:
            GlobalVal.showInText('error:get.read or file.read')
            return False
        # Dont know what is happened.
        except :
            GlobalVal.showInText('error:network disconnect.')
            return False


    def login(self):
        login_params = {
            'j_username': GlobalVal.username,
            'j_password': GlobalVal.password,
            'validateCode': GlobalVal.secretCode
        }
        login_result = ''
        try:
            login_result = self.__session.post(self.home_url, data=login_params, headers=self.header,timeout=6)
        # DNS failure, refused connection, etc
        except ConnectionError :
            return False,'error:ConnectionError.'
        # Timeout
        except TimeoutError:
            return False, 'error:TimeoutError.'
        # HTTPError
        except requests.HTTPError:
            return False, 'error:HTTPError:%s.'%login_result.status_code
        except :
            return False,'error:network disconnect.'
        # Almost everything is ok.
        if 'success' in login_result.json():
            return True, login_result.json()
        else:
            return False, login_result.json()

    def get_my_score(self,score_params):
        score_params_post = {
            'currentSelectTabId': '01',
            'isFirst': '1',
            'optype': 'query',
            'qKch_ys': '',
            'qKclbdm_ys': '',
            'qKcm_ys': '',
            'qKcxzdm_ys': '',
            'qXndm_ys': score_params[0:9],
            'qXqdm_ys': score_params[-1:]
        }
        try:
            score_back = self.__session.post(self.socre_url, data=score_params_post, headers=self.header)
            return score_back.text.encode()
        except:
            return ''

    def get_my_exam(self,exam_params):
        exam_params_post = {
            'xnxqdm': exam_params
        }
        try:
            exam_back = self.__session.post(self.exam_url, data=exam_params_post, headers=self.header)
            return exam_back.text.encode()
        except:
            return ''

    def get_my_timetable(self,timetable_params):
        self.timetable_url += timetable_params
        try:
            timetable_back = self.__session.get(self.timetable_url, headers=self.header)
            return timetable_back.text.encode()
        except:
            return ''

def walk_with_score():
    proc = ProcessHtml.ProcessHtml()
    save_html = SaveFile.SaveHtml()
    score_html = GlobalVal.spider.get_my_score(GlobalVal.check_myscore_val)
    score_html_proced = proc.proc_score(score_html)
    save_html.save_as_score(score_html_proced)

def walk_with_timetable():
    proc = ProcessHtml.ProcessHtml()
    save_html = SaveFile.SaveHtml()
    timetable_html = GlobalVal.spider.get_my_timetable(GlobalVal.check_timetable_val)
    timetable_html_proced = proc.proc_timetable(timetable_html)
    save_html.save_as_timetable(timetable_html_proced)

def walk_with_exam():
    proc = ProcessHtml.ProcessHtml()
    save_html = SaveFile.SaveHtml()
    exam_html = GlobalVal.spider.get_my_exam(GlobalVal.check_exam_val)
    exam_html_proced = proc.proc_exam(exam_html)
    save_html.save_as_exam(exam_html_proced)


