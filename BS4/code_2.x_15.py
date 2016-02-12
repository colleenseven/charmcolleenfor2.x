# __author__ = 'colleen'
# -*-coding=utf-8-*-
# author:zhangle

import urllib2
import urllib
import thread
import threading

import chardet
from bs4 import BeautifulSoup as BS

myLock = threading.RLock()


class GetUrls(object):
    pageCount = 1
    search_url = 'http://www.baidu.com/s?wd=key'
    req_header = {'User-Agent': 'Mozilla/5.0(Windows;U;Windows NT 6.1;en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}

    def __init__(self, inputInfo):
        self.inputInfo = inputInfo
        GetUrls.search_url = GetUrls.search_url.replace('key', self.inputInfo)

    # detect the coding of the html page
    def __detectCode(self, url):
        htmlInfo = urllib.urlopen(url).info()
        coding = htmlInfo.getparam('charset')
        if coding is None:
            htmlInfo = urllib.urlopen(url).read()
            coding = chardet.detect(htmlInfo)['encoding']
            if coding is None:
                coding = 'utf-8'
        coding = coding.lower()
        return coding

    # get the html title
    def __getTitle(self, url):
        coding = self.__detectCode(url)
        try:
            titleReq = urllib2.Request(url, None, GetUrls.req_header)
            titleRes = urllib2.urlopen(titleReq)
            html = titleRes.read()
            titleSoup = BS(html, 'html.parser', decode(coding, 'ignore'))
            title = titleSoup.title.string
            return title
        except urllib2.HTTPError:
            return None
        except urllib2.URLError:
            return None

    # get the information inside the html page
    def __getInfo(self, redUrl):
        # myLock.acquire()
        with open('info.txt', mode='a') as a_file:
            title = self.__getTitle(redUrl)
            if title:
                # print title.encode('gbk','ignore')
                a_file.write(title.encode('gbk', 'ignore') + '\n')
                a_file.write(redUrl + '\n\n')
                # myLock.release()

    def __searchUrls(self, url):
        if GetUrls.pageCount > 20:
            return
        else:
            req = urllib2.Request(url, None, GetUrls.req_header)
            res = urllib2.urlopen(req)
            html = res.read()
            soup = BS(html, 'html.parser', decode('utf-8', 'ignore'))

            # get the 100 urls from page 10 to page 20
            if GetUrls.pageCount > 10:
                htmlList = soup.find_all('h3')
                for hh in htmlList:
                    # get url in the html page
                    urlInPage = hh.a.get('href')

                    # get url after redirecting
                    try:
                        req = urllib2.Request(urlInPage, None, GetUrls.req_header)
                        redUrl = urllib2.urlopen(req).geturl()
                    except urllib2.HTTPError:
                        redUrl = urlInPage
                    thread.start_new_thread(self.__getInfo, (redUrl,))

            GetUrls.pageCount += 1
            pNode = soup.find_all('span', text=GetUrls.pageCount)
            nextUrl = 'http://www.baidu.com' + pNode[0].parent.get('href')

            self.__searchUrls(nextUrl)

    def UrlParse(self):
        self.__searchUrls(GetUrls.search_url)


if __name__ == '__main__':
    getUrlInfo = GetUrls('�ھ��')
    getUrlInfo.UrlParse()
