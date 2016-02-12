# __author__ = 'colleen'
# -*- coding: utf-8 -*-
import urllib
import threading

from bs4 import BeautifulSoup

import urllib.request

mylock = threading.RLock()


class Crawler:
    unVisitUrl = set()
    visitedUrl = []

    def getHtml(self, url):

        html = ''
        req = urllib.request.Request(url, headers={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        })
        try:
            respose = urllib.request.urlopen(req, timeout=10)
            html = respose.read().decode('UTF-8').replace('&nbsp', '')
        except Exception as e:
            pass

        return html;

    def getUrlFromHtml(self, html, sitePath):

        if (html):
            soup = BeautifulSoup(html, 'html.parser')
            aList = soup.find_all('a')
            for a in aList:
                try:
                    if sitePath in a['href'] and a['href'].startswith('http://'):
                        self.addUnVisitUrl(a['href'])
                        self.addVisitedUrl(a['href'])
                except KeyError:
                    pass

    # 解析网页内容
    def analysis(self, url, sitePath):

        self.initUnVisitUrl(url)

        while (len(self.unVisitUrl) > 0):
            visitingUrl = self.getUnVisitUrl()
            print(visitingUrl)
            if (visitingUrl):
                html = self.getHtml(visitingUrl)
                if (html):
                    # 获取网页中所有内部链接，存储
                    self.getUrlFromHtml(html, sitePath)

    # 初始化根链接
    def initUnVisitUrl(self, url):
        self.unVisitUrl.add(url)

    def addUnVisitUrl(self, url):
        if url not in self.unVisitUrl and url not in self.visitedUrl:
            self.unVisitUrl.add(url)

    def getUnVisitUrl(self):

        url = None
        unVisitUrlTmp = list(self.unVisitUrl)
        if unVisitUrlTmp[0]:
            url = unVisitUrlTmp[0]
            self.unVisitUrl.remove(url)

        return url

    def addVisitedUrl(self, url):
        self.visitedUrl.append(url)
