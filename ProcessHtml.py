# coding=utf-8
# ProcessHtml.py
# 处理获取到的html文件


from bs4 import BeautifulSoup
import globalVal

# 处理个人信息
def modify_myInfo(htmlHead,html):
    strHtml  = str(html)
    strHtml = strHtml.replace("\"/ssfw/","\"" + htmlHead + "/ssfw/")
    return strHtml

# 处理课程表的html
def modify_timeTable(html):
    strHtml  = str(html)
    soup = BeautifulSoup(strHtml, 'html.parser')



    # 修改网页的背景图片
    bg = soup.body
    bg['background'] = "../../background/bing_bg(%s).jpg"%globalVal.today

    # 改变中间内容的透明度
    divBody = soup.find_all("div", {'class': 'tableGroup otherInfo'})
    for div in divBody:
        div['style'] = 'opacity: 0.8'

    # 修改网页抬头
    html_title = soup.title
    html_title.string = "Foxlogin"

    # 处理css
    cssList = soup.find_all("link")
    for css in cssList:
        getVal = css.get('href')
        if getVal:
            css['href'] = "../../" +getVal[getVal.find('css'):]
    # 处理js
    jsList = soup.find_all("script")
    for js in jsList:
        if js.get('src'):
            js['src'] = 'by_lileihui'
    # 处理div选择框
    div_choice = soup.find("div",{'class':'NoPrint mainQuery'})
    div_choice['style'] = 'display:none'
    # 处理打印字样
    span_print = soup.find("span",{'class':'spanFloatRight'})
    span_print['style'] = 'display:none'
    return str(soup)

# 处理成绩的html
def modify_myScore(html):
    strHtml  = str(html)
    soup = BeautifulSoup(strHtml, 'html.parser')

    # 修改网页的背景图片
    bg = soup.body
    bg['background'] = "../../background/bing_bg(%s).jpg"%globalVal.today

    # 修改网页抬头
    html_title = soup.title
    html_title.string = "Foxlogin"

    # 改变中间内容的透明度
    divBody = soup.find_all("div",{'class':'div_body'})
    for div in divBody:
        div['style'] = 'opacity: 0.8'

    # 改变div
    divList = soup.find_all("div")
    for div in divList:
        if div.get('title'):
            div['style'] = 'display:by_lileihui'

    # 修改css
    cssList = soup.find_all("link")
    for css in cssList:
        getVal = css.get('href')
        if "lovey" in getVal or "css/custom" in getVal:
            css['href'] =  "../../" + getVal[getVal.find('css'):]
        else:
            css ['href'] = "lielihui"

    # 修改js
    jsList = soup.find_all("script")
    for js in jsList:
        if js.get('src'):
            js['src'] = 'lileihui'

    # 修改宽度
    th_className = soup.find("th",text='课程名称')
    if th_className:
        th_className['width'] = '25%'

    # 修改不必要的输入框
    tableList = soup.find_all("table",{'height':'35px'})
    for table in tableList:
          table['style'] = 'display:none'

    # 完善图片链接
    img = soup.find("img",{'class':'tip-icon'})
    if img:
        img['src'] = '../../image/fail_img.jpg'

    # 修改顶部ul
    ul = soup.find("ul",{'class':'ui_nav_breadcrumb_style02 ul_fixed'})
    if ul:
        ul['style'] = 'display:none'

    return str(soup)

# 处理考试安排的html
def modify_myTest(html):
    strHtml = str(html)
    soup = BeautifulSoup(strHtml, 'html.parser')

    # 修改网页的背景图片
    bg = soup.body
    bg['background'] = "../../background/bing_bg(%s).jpg"%globalVal.today

    # 改变中间内容的透明度
    divBody = soup.find_all("div", {'class': 'div_body'})
    for div in divBody:
        div['style'] = 'opacity: 0.8'


    # 修改网页抬头
    html_title = soup.title
    html_title.string = "Foxlogin"

    # 修改css路径
    cssList = soup.find_all("link")
    for css in cssList:
        getVal = css.get('href')
        if "lovey" in getVal or "css/custom" in getVal:
            css['href'] = "../../" +getVal[getVal.find('css'):]
        else:
            css['href'] = "by_lileihui"

    # 修改js路径
    jsList = soup.find_all("script")
    for js in jsList:
        if js.get('src'):
            js['src'] = 'by_lileihui'

    # 修改table
    tableList = soup.find_all("table",{'height':'35px'})
    for table in tableList:
        table['style'] = 'display:none'

    # 修改顶部ul
    ul = soup.find("ul", {'class': 'ui_nav_breadcrumb_style02 ul_fixed'})
    if ul:
        ul['style'] = 'display:none'

    # 篡改js本地代码
    strSoup = str(soup)
    strSoup = strSoup.replace(".ui_table", '.ui_table{这坨代码贼傻}')
    strSoup = strSoup.replace('.div_body','.div_body{idontlike固定界面}')

    return strSoup