# coding=utf-8
'''this is from http://www.cnblogs.com/mfrbuaa/p/4383057.html,in the end ,there is a return name:None,but i dont know why'''
import urllib
import re
import os


def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


def getImg(html):
    reg = r'src="(http://imgsrc.baidu.com/forum/w%3D580.*?\.jpg)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)

    filepath = os.getcwd() + '\pythonimg'
    if os.path.exists(filepath) is False:
        os.mkdir(filepath)

    x = 0
    for imgurl in imglist:
        urllib.urlretrieve(imgurl, filepath + '\%s.jpg' % x)
        x += 1
    print u'图片完成下载，保存路径为' + filepath


html = getHtml("http://tieba.baidu.com/p/4090435619")

print getImg(html)
