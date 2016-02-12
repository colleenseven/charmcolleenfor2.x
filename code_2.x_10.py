# -*- coding: utf-8 -*-
'''this url is not found'''
import urllib
import urllib2

from bs4 import BeautifulSoup
import threadpool


class htmlpaser:
        def __init__(self):
                self.url = 'http://1.hzfans.sinaapp.com/process.php'

        # POST数据到接口
        def Post(self, postdata):
                # headers = {
                #         'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
                # }
                # data = urllib.urlencode(postdata)
                # req = urllib2.Request(self.url,data,headers)
                # resp = urllib2.urlopen(req,None,20)
                # html = resp.read()
                # return html
                data = urllib.urlencode(postdata)
                req = urllib2.Request(url, data)
                html = urllib2.urlopen(req).read()
                print html

        # 获取html内容
        def GetHtml(self, url):
                headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
                }
                req = urllib2.Request(url, None, headers)
                resp = urllib2.urlopen(req, None, 5)
                html = resp.read()
                # return html.decode('utf8')
                return html

        def GetHtml2(self, url):
                page = urllib.urlopen(url)
                html = page.read()
                page.close()
                return html

        def GetHtml3(self, url):
                req_header = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'gzip',
                        'Connection': 'close',
                        'Referer': None  # 注意假设依旧不能抓取的话，这里能够设置抓取站点的host
                        }
                req_timeout = 5
                req = urllib2.Request(url, None, req_header)
                resp = urllib2.urlopen(req, None, req_timeout)
                html = resp.read()
                return html

        def GetList(self, html):
                soup = BeautifulSoup(''.join(html))
                baseitem = soup.find('ul', {'class': 'list'})
                slist = baseitem.select('li a')
                return slist

        def DownImg(self, imgurl):
                path = r"d:/imgcache/" + self.gGetFileName(imgurl)
                data = urllib.urlretrieve(imgurl, path)
                return data

        def gGetFileName(self, url):
                if url == None: return None
                if url == "": return ""
                arr = url.split("/")
                return arr[len(arr) - 1]

        def mkdir(path):
                import os
                path = path.strip()
                path = path.rstrip("\\")
                # 推断路径是否存在
                # 存在     True
                # 不存在   False
                isExists = os.path.exists(path)
                # 推断结果
                if not isExists:
                        # 假设不存在则创建文件夹
                        # 创建文件夹操作函数
                        os.makedirs(path)
                        return True
                else:
                        # 假设文件夹存在则不创建，并提示文件夹已存在
                        return False

        # 返回两个值
        def ParseContent(self, html):
                soup = BeautifulSoup(''.join(html))
                baseitem = soup.find('div', {'class': 'showbox'})
                title = soup.find('div', {'class': 'msg'}).find('div', {'class': 'm_left'}).get_text()
                imglist = baseitem.find_all('img')
                for img in imglist:
                        imgurl = img.get('src')
                        self.DownImg(imgurl)
                content = baseitem.get_text().encode('utf8')
                position = content.find('热点推荐')
                return title, content[0:position]

        def ParseItem(self, item):
                url = item.get('href')
                if url == None:
                        return
                # print url+'\n'
                html = obj.GetHtml2(url)
                title, content = obj.ParseContent(html)
                # print title+'\n'
                return title


def print_result(request, result):
        print str(request.requestID) + ":" + result


obj = htmlpaser()

pool = threadpool.ThreadPool(10)
for i in range(1, 40):
        url = "http://op.52pk.com/shtml/op_wz/list_2594_%d.shtml" % (i)
        html = obj.GetHtml2(url)
        items = obj.GetList(html)
        print 'add job %d\r' % (i)
        requests = threadpool.makeRequests(obj.ParseItem, items, print_result)
        [pool.putRequest(req) for req in requests]
pool.wait()
