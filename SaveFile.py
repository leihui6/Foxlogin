# coding=utf-8
# SaveFile.py
# 保存文件
import os
import globalVal
import urllib.request

import urllib.parse

def saveHtml(htmlFile,fileName):
    # 保存的原则是'学好/学期/html文件'
    # print  (fileName)
    # 将 复选框内容转为学期(汉字)
    word = globalVal.year2easyRead(fileName[3:14])

    # 获取文件夹路径 '学好/学期'
    folderName = './' + globalVal.username + '/'+word

    # 将文件名中的学期转为汉字
    fileName = fileName[:3] + word + fileName[14:]

    globalVal.saveTolog(fileName + "已保存在\""+folderName+"/\"下")

    # 检查是否存在文件夹
    if os.path.exists(folderName):
        file = open(folderName + "/"+ fileName, 'wb+')

        file.write(htmlFile.encode('utf-8'))

        file.close()
    else:
        os.makedirs(folderName)

        file = open(folderName + "/" + fileName, 'wb+')

        file.write(htmlFile.encode('utf-8'))

        file.close()

# 获取html中的img链接
def savePhoto(folderName,username):
    if os.path.exists(folderName):
        imgUrl = "http://ssfw.tjut.edu.cn/ssfw/photo.widgets?handler=photo1Handler&value=&bh=%s" % username
        urllib.request.urlretrieve(imgUrl, folderName + "/photo.jpg")

    else:
        os.mkdir(folderName)
        imgUrl = "http://ssfw.tjut.edu.cn/ssfw/photo.widgets?handler=photo1Handler&value=&bh=%s" % username
        urllib.request.urlretrieve(imgUrl, folderName + "/photo.jpg")
