# __author__ = 'Administrator'
# coding=utf-8

import re
import urllib
import urllib2
import StringIO
import gzip
import os
import sys

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
}


# 解压gzip
def gzdecode(data):
	compressedstream = StringIO.StringIO(data)
	gziper = gzip.GzipFile(fileobj=compressedstream)
	data2 = gziper.read()  # 读取解压缩后数据
	return data2


# 获取html代码
def getHtml(url):
	request = urllib2.Request(url, headers=headers)
	try:
		response = urllib2.urlopen(request)
		html = response.read()
		return html
	except urllib2.URLError, e:
		print e.reason


# 目录是否存在，不存在则创建
def createDir(path):
	if not os.path.exists(path):
		os.makedirs(path)
	else:
		if os.path.isfile(path):
			os.mkdir(path)


# 提取描述url
def descUrl(html):
	reg = r"descUrl.*?location.protocol==='http:' \? '//(.*?)'.?:"
	desurlre = re.compile(reg, re.I)
	desurl = re.findall(desurlre, html)
	return desurl


# 提取所有图片
def getImglist(html):
	reg = r'src=\"(.*?)\"'
	imgre = re.compile(reg, re.I)
	imglist = re.findall(imgre, html)
	return imglist


# 提取主图
def getTitleImg(html, path):
	createDir(path)
	reg = r'auctionImages.*?\[(.*?)\]'
	imgre = re.compile(reg, re.I)
	titleImg = re.findall(imgre, html)
	titleImg = titleImg[0]
	imglist = titleImg.split(',')
	titleIndex = 1
	for imgurl in imglist:
		print "img ==== >  " + imgurl
		imgurl = imgurl.strip('"')
		imgurl = 'http:' + imgurl
		print imgurl
		splist = imgurl.split('.')
		filetype = splist[len(splist) - 1]
		try:
			urllib.urlretrieve(imgurl, path + "/title" + str(titleIndex) + '.' + filetype)
			titleIndex += 1
			print "==> ok!"
		except:
			print "==> err!!!!!!"


# 保存所有图片
def saveImgTo(imglist, path):
	createDir(path)
	imgIndex = 1
	for imgurl in imglist:
		splist = imgurl.split('.')
		filetype = splist[len(splist) - 1]
		print "saving " + imgurl
		try:
			urllib.urlretrieve(imgurl, path + "/" + str(imgIndex) + '.' + filetype)
			imgIndex += 1
			print "==> ok!"
		except:
			print "==> err!!!!!!"


# 从一个淘宝页面，得到详情图片
def getTaoBaoImg(url, savePath):
	html = getHtml(url)
	getTitleImg(html, savePath)
	desurl = descUrl(html)
	desurl = "http://" + desurl[0]
	print "desurl = " + desurl
	print "----------------------------------------------------------"
	# 得到淘贝详情html
	desHtml = getHtml(desurl)
	imglist = getImglist(desHtml)
	saveImgTo(imglist, savePath)


# -------------------------------------我是华丽的分界线 begin Other-----------------------------------------
# 提取其他详情图片列表
def getOtherImgurllist(html):
	reg = r'src="(.*?)"'
	desre = re.compile(reg, re.S)
	imgurllist = re.findall(desre, html)
	return imgurllist


# 从其他提取详情图片
def getOtherImg(url, savePath):
	html = getHtml(url)
	imglist = getOtherImgurllist(html)
	saveImgTo(imglist, savePath)


# 提取其他主图
def getOthertitleImg(html, savePath):
	print "todo:"


# -------------------------------------我是华丽的分界线 end Other-----------------------------------------

# 保存原地址
def saveUrl(url, savePath):
	output = open(savePath + "/url.htm", "w")
	output.write("""<html>
<head>
<meta http-equiv="Content-Language" content="zh-CN">
<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=gb2312">
<meta http-equiv="refresh" content="0.1;url=""" + url + """\">
<title></title>
</head>
<body>
</body>
</html>""")
	output.close()


savepath = "img"

input = open('url.txt', 'r')

urls = input.read()
urls = urls.split('\r\n')
print urls

if len(sys.argv) > 1 and sys.argv[1]:
	savepath = sys.argv[1]

print savepath

urlIndex = 1
for url in urls:
	if len(url) < 10:
		continue
	urlSavePath = savepath + '/' + str(urlIndex)
	createDir(urlSavePath)
	saveUrl(url, urlSavePath)
	print '*' * 50
	print url
	if url.find('taobao') != -1:
		getTaoBaoImg(url, urlSavePath)
	else:
		getOtherImg(url, urlSavePath)
	urlIndex += 1

print "success!"
