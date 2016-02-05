#coding=utf-8

'''this is from http://www.cnblogs.com/mfrbuaa/p/4383057.html'''

import re
import os
import urllib

'''this is the first one'''

url="http://tieba.baidu.com/p/4178073660"
imgcontent=urllib.urlopen(url).read()
reg = r'src="(http://imgsrc.baidu.com/forum/w%3D580.*?\.jpg)"'
imgre = re.compile(reg)
urllist = imgre.findall(imgcontent)
if not urllist:
	print 'not found...'
else:

	filepath=os.getcwd()+'\pythonimg'
	if os.path.exists(filepath) is False:
		os.mkdir(filepath)
	x=1
	print u'爬虫准备就绪...'
	for imgurl in urllist:
		temp= filepath + '\%s.jpg' % x
		print u'正在下载第%s张图片' % x
		print imgurl
		urllib.urlretrieve(imgurl,temp)
		x+=1
	print u'图片完成下载，保存路径为'+filepath