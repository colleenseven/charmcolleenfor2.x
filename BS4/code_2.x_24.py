# __author__ = 'colleen'
# -*- coding: gbk -*-

import urllib
import urllib2
import time
import re
import os

from bs4 import BeautifulSoup


def req(url):
    # url='http://www.szu.edu.cn/2014/news/index_1.html'
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request(url, headers=header)
    data = urllib.urlopen(req).read()
    print data
    return data


def reqImg():
    # url='http://www.junmeng.com/tj/22376_4.html'
    url = r'http://www.junmeng.com/tj/22376.html'
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    patnLink = r'<a href=".*/tj/22376_\d*.html"><img src.+</a>'
    patnImg = r'<img src=.+>'
    savedir = r'C:\Users\hp\Desktop\results'
    if not os.path.exists(savedir):
        os.mkdir(savedir)

    for i in range(1, 20):
        if i == 1:
            tempurl = url
        else:
            tempurl = 'http://www.junmeng.com/tj/22376_%d.html' % i
        print tempurl
        # req=Request(tempurl,headers=header)
        data = urllib.urlopen(tempurl).read()
        # print data
        if i == 19:
            patnLink = r'<a href=.*><img src=.*</a>'
        imgLinks = re.findall(patnLink, data)
        # print results
        link = imgLinks[0]
        # print link
        imgLink = link[link.find('src=') + 5:link.find('.jpg') + 4]
        print imgLink
        fullLink = r'http://www.junmeng.com%s' % imgLink
        lct = time.strftime('%Y%m%d%H%M%S')
        urllib.urlretrieve(fullLink, '%s\%s%d.jpg' % (savedir, lct, i))
        # return data


def reqImg2():
    url = r'http://www.ik6.com/meinv/40569/index.html'
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    savedir = r'C:\Users\hp\Desktop\results'
    if not os.path.exists(savedir):
        os.mkdir(savedir)

    for i in range(1, 10):
        if i == 1:
            tempurl = url
        else:
            tempurl = 'http://www.ik6.com/meinv/40569/index_%d.html' % i
        print tempurl
        # req=Request(tempurl,headers=header)
        data = urllib.urlopen(tempurl).read()
        page = BeautifulSoup(data)
        imgsrc = page.find_all('center')[0].find_all('img')[0].get('lazysrc')
        print imgsrc
        lct = time.strftime('%Y%m%d%H%M%S')
        urllib.urlretrieve(imgsrc, '%s\%s%d.jpg' % (savedir, lct, i))


def reqImg3():
    url = r'http://www.ik6.com/meinv/40572/index.html'
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    savedir = r'C:\Users\hp\Desktop\results'
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    for i in range(1, 10):
        if i == 1:
            tempurl = url
        else:
            tempurl = 'http://www.ik6.com/meinv/40572/index_%d.html' % i
        print tempurl
        # req=Request(tempurl,headers=header)
        data = urllib.urlopen(tempurl).read()
        page = BeautifulSoup(data)
        imgsrc = page.find_all('center')[0].find_all('img')[0].get('lazysrc')
        print imgsrc
        lct = time.strftime('%Y%m%d%H%M%S')
        urllib.urlretrieve(imgsrc, '%s\%s%d.jpg' % (savedir, lct, i))


def reqImg4(url, themecount, imgcount):
    # url=r'http://www.ik6.com/meinv/40572/index.html'
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    savedir = r'C:\Users\hp\Desktop\result0128'
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    newUrl = (url[:url.rfind('.htm')] + '_%d.html')
    print newUrl
    for i in range(1, imgcount + 1):
        if i == 1:
            tempurl = url
        else:
            tempurl = newUrl % i
        print tempurl
        try:
            data = urllib.urlopen(tempurl).read()
            if not data:
                print 'no response,exit'
                return
            page = BeautifulSoup(data)
            centers = page.find_all('center')
            if len(centers) == 0:
                print 'response has no contents,exit'
                return
            else:
                imgsrc = centers[0].find_all('img')[0].get('lazysrc')
                print imgsrc
                # lct=time.strftime('%Y%m%d%H%M%S')
                # urllib.urlretrieve(imgsrc,'%s\%s%d.jpg'%(savedir,lct,i))
                urllib.urlretrieve(imgsrc, '%s\%d_%d.jpg' % (savedir, themecount, i))
        except Exception, e:
            return


req('http://blog.csdn.net/suwei19870312/article/details/8148427')
req('http://www.taobao.com')
reqImg()
reqImg2()
reqImg3()
for i in range(1000):
    count = 11170 + i
    url = r'http://www.ik6.com/meinv/%d/index.html' % count
    reqImg4(url, 8)
