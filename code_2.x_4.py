#__author__ = 'colleen'
# coding=utf-8
import re
import os

import requests


class Spider:
    def savePageInfo(self, _url, _position, _regX):

        url = _url
        position = _position
        html = requests.get(url).text

        regX = _regX

        pic_url = re.findall(regX,html,re.S)

        i = 0
        for each in pic_url:

            pic = requests.get(each)
            print url + each
            if not os.path.isdir(position):

                os.makedirs(position)

            fp = open( position+str(i)+'.jpg', 'wb' )
            fp.write(pic.content)
            # print position+each
            fp.close()
            i+=1



position_end = ''

url = 'http://tieba.baidu.com/p/3590998005' + position_end

position = '/Users/edison/Desktop/1/' + position_end

regX = '_blank\'><img src=(.*?) t'

spider = Spider()
spider.savePageInfo(url, position, regX)
