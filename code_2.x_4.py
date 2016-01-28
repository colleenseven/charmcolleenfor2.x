#__author__ = 'colleen'
# coding=utf-8
# ����
import re
# ���罻��
import requests
# ����ϵͳ����
import os

# ����һ����
class Spider:
    #����һ������
    def savePageInfo(self, _url, _position, _regX):

        # Ҫ������ַ
        url = _url
        # ���ص�ַ
        position = _position
        # ��ȡ��ҳԴ����
        html = requests.get(url).text

        # ����
        regX = _regX

        pic_url = re.findall(regX,html,re.S)

        i = 0
        for each in pic_url:

            pic = requests.get( each )
            print  url + each
            # ����ļ��в����ڣ��򴴽�һ���ļ���
            if not os.path.isdir(position):

                os.makedirs(position)

            fp = open( position+str(i)+'.jpg', 'wb' )
            fp.write(pic.content)
            # print position+each
            fp.close()
            i+=1


#����������������������������������������ҳ��ȡͼƬ������������������������������������������������

position_end = ''

# Ҫ������ַ
url = 'http://tieba.baidu.com/p/3590998005' + position_end

# ���ص�ַ
position = '/Users/edison/Desktop/1/' + position_end

# ����
regX = '_blank\'><img src=(.*?) t'

#���� url, ����λ��, ��ȡ������
spider = Spider()
spider.savePageInfo(url, position, regX)
