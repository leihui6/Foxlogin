Foxlogin
===
_Foxlogin_ 是一个能快速获取你的任意学期的考试安排/考试成绩/课表的程序;</br>
目前(2016/08/30),我们决定停止对其进行维护;</br>
欢迎对我们公开的代码进行你需要的修改;</br>

### 平台:
* Python 3.5.2

### 所需要的第三方模块:
* Pillow
* BeautifulSoup4

### 使用
* \>\> python Main.py

### 功能分布
* Main.py: 负责窗体程序的创建 , 程序入口;
* globalVal.py : 负责全局变量,函数;
* LoginSucc.py : 负责登录成功后的驱动程序;
* ProcessHtml.py: 负责对获取到的html进行处理;
* SaveFile.py: 负责对数据的保存;
* SearchMyInfo.py : 负责获取我的个人信息;
* SearchMyScore.py : 负责获取我的成绩;
* SearchMyTest.py : 负责获取我的考试安排;
* SearchTimeTable.py : 负责获取的课表;
* SimuLogin\_.py : 负责模拟登录

### 文件分布
>* 以下文件夹中的内容请不要擅自改动,即使程序会对其包含的文件进行必要的检测;
>* ./image : 储存程序启动与运行需要的图像资料.
>* ./css : 储存将获取的HTML界面完美显示的必要文件.
>* 以下文件夹会在程序启动时自动创建:
>* ./background :存储Bing首页壁纸,,用于HTML页面的背景;
>* ./data : 存储程序运行日志;

### 遗憾
* 如果能重来,我想我会使用Requests库爬取页面.
* 程序框架还有待改进.

如果你有任何问题,请毫不犹豫的与我联系:
<find_by_u@163.com>
