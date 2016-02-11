# -*-coding:utf-8-*-
'''this url is http://www.cnblogs.com/mtTeam/p/4895089.html'''
import re
import os

import requests


class Spider:
    def savePageInfo(self, _url, _position, _regX):
        url = _url
        position = _position
        html = requests.get(url).text

        regX = _regX

        pic_url = re.findall(regX, html, re.S)

        i = 0
        for each in pic_url:

            pic = requests.get(each)
            print  each
            if not os.path.isdir(position):
                os.makedirs(position)

            fp = open(position + "/" + str(i) + '.jpg', 'wb')
            fp.write(pic.content)
            print position + " " + each
            fp.close()
            i += 1


# position_end = ''

url = 'http://www.umei.cc/'  # + position_end

position = os.getcwd() + '\pythonimg'  # + position_end

regX = r'src="(http://s.umei.cc/small.*?\.jpg)"'

spider = Spider()
spider.savePageInfo(url, position, regX)
