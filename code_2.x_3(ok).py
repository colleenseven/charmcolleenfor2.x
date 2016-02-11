# coding:utf-8
'''this url site is http://www.cnblogs.com/vpoet/p/4659595.html'''
import urllib
import urllib2
import re
import os

if __name__ == "__main__":
    rex = r'src="(http://imgsrc.baidu.com/forum/w%3D580.*?\.jpg)"';
    Response = urllib2.urlopen("http://tieba.baidu.com/p/4345307742");
    Html = Response.read()

    lists = re.findall(rex, Html);
    filepath = os.getcwd() + '\pythonimg'
    if os.path.exists(filepath) is False:
        os.mkdir(filepath)
    x = 0
    for picurl in lists:
        urllib.urlretrieve(picurl, filepath + '\%s.jpg' % x);
        x = x + 1;
        print picurl;

    print 'DownLoadPicOver'
    # 图片存储路径:C:\Users\Administrator\Desktop\pic
    # 测试爬取网址:http://tieba.baidu.com/p/3842835603?fr=frs
