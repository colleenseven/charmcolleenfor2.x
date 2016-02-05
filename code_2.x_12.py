# __author__ = 'Administrator'
# coding:utf-8
import urllib
import urllib2
import re


# 将正则表达式编译成Pattern对象
rex = r'src="(http://imgsrc.baidu.com/forum/w%3D580.*?\.jpg)"';
pages = ('1', '2');

for page in pages:
	pageurl = "http://tieba.baidu.com/p/3710495592?pn=" + page;
	Response = urllib2.urlopen(pageurl);
	Html = Response.read();
	lists = re.findall(rex, Html);
	lensofpage = len(lists);
	print lensofpage;

	picname = 'pic' + page;
	print picname;
	x = 1;
	for picurl in lists:
		urllib.urlretrieve(picurl, 'C:\Users\Administrator\Desktop\%s\%s.jpg' % (picname, x));
		print page + picurl;
		x = x + 1;

print 'DownLoadPicOver'
# 图片存储路径:C:\Users\Administrator\Desktop\pic1
# C:\Users\Administrator\Desktop\pic2
# 测试爬取网址:http://tieba.baidu.com/p/3710495592?pn=1
#         http://tieba.baidu.com/p/3710495592?pn=2
