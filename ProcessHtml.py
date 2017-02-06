# -*- coding: UTF-8 -*-
'''
    模块名称:ProcessHtml
    功能:处理获取到的页面,使得页面更加简洁
    时间:2017-02-06
    作者:ptsph@foxmail.com
'''
from bs4 import BeautifulSoup

class ProcessHtml:
    '''
        处理基本规则
        - 有效css本地化
        - js全部删除
        - title修改为From Foxlogin
        - 简洁化各个界面,意味着删除页面无用小部件
    '''
    def __init__(self):
        pass

    # 处理课程表的html
    def proc_timetable(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser', from_encoding='utf-8')
        # 修改网页抬头
        html_title = soup.title
        html_title.string = "From Foxlogin"
        # css转为本地化
        cssList = soup.find_all("link")
        for css in cssList:
            getVal = css.get('href')
            if getVal:
                css['href'] = "../../" + getVal[getVal.find('css'):]
        # 去掉全部js
        jsList = soup.find_all("script")
        for js in jsList:
            js.decompose()
        # 去掉自主选择框
        div_choice = soup.find("div", {'class': 'NoPrint mainQuery'})
        if div_choice:
            div_choice.decompose()
        # 去掉打印字样
        span_print = soup.find("span", {'class': 'spanFloatRight'})
        if span_print:
            span_print.decompose()
        return str(soup)

    # 处理我的成绩html
    def proc_score(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser', from_encoding='utf-8')
        # 修改网页抬头
        html_title = soup.title
        html_title.string = "From Foxlogin"
        # 改变div
        divList = soup.find_all("div")
        for div in divList:
            if div.has_attr('title'):
                div['style'] = 'display:inline'
        # 修改css
        cssList = soup.find_all("link", {'rel': 'stylesheet'})
        for css in cssList:
            # 在decompose后会发生空访问现象
            if css.name:
                getVal = css.get('href')
                if "lovey" in getVal or "css/custom" in getVal:
                    css['href'] = "../../" + getVal[getVal.find('css'):]
                else:
                    css.decompose()
        # 删除所有js
        jsList = soup.find_all("script")
        for js in jsList:
            js.decompose()
        # 修改宽度
        th_className = soup.find("th", text='课程名称')
        if th_className:
            th_className['width'] = '25%'
        # 修改不必要的输入框
        tableList = soup.find_all("table", {'height': '35px'})
        for table in tableList:
            table.decompose()
        # 完善图片链接
        img = soup.find("img", {'class': 'tip-icon'})
        if img:
            img['src'] = '../../image/init_img.jpg'
        # 去掉修改顶部ul
        ul = soup.find("ul", {'class': 'ui_nav_breadcrumb_style02 ul_fixed'})
        if ul:
            ul.decompose()
        return str(soup)

    def proc_exam(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser', from_encoding='utf-8')
        # 修改网页抬头
        html_title = soup.title
        html_title.string = "From Foxlogin"
        # 删除全部css
        cssList = soup.find_all("link")
        for css in cssList:
            css.decompose()
        # 删除全部js路径
        jsList = soup.find_all("script")
        for js in jsList:
            js.decompose()
        # 删除顶部搜索框
        search_bar = soup.find("div", {'id': 'mainQuery'})
        if search_bar:
            search_bar.decompose()
        # 修改顶部ul
        ul = soup.find("ul", {'class': 'ui_nav_breadcrumb_style02 ul_fixed'})
        if ul:
            ul.decompose()
        # 删除顶部通知
        inform = soup.find("div", {'id': 'tsDiv'})
        if inform:
            inform.decompose()

        return str(soup)