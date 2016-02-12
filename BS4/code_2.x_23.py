# __author__ = 'colleen'
# -*- coding: utf-8 -*-
# func passport jw.qdu.edu.cn
import urllib
# python3后urllib.request代替urllib2
import urllib.request
import json
from bs4 import BeautifulSoup


class taofen:
    def getHtml(self, pageurl):
        # 获取网站html代码
        req = urllib.request.Request(pageurl, headers={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        })
        _respose = urllib.request.urlopen(req, timeout=2)
        try:
            html = _respose.read().decode('UTF-8').replace('&nbsp', '')
        except Exception as e:
            pass
        return html

    def getKind(self, html):
        soup = BeautifulSoup(html, "html.parser")
        liList = soup.find_all('li')
        res = []
        for li in liList:
            if li.img and li.find(class_="change_price"):
                img = li.img.attrs['original']
                name = li.img.attrs['alt']
                price = li.find(class_="change_price").string
                resNode = {'img': img, 'name': name, 'price': price}
                res.append(resNode)
        return res


if __name__ == "__main__":
    taofen = taofen()
    html = taofen.getHtml("http://www.taofen8.com/promcat-4/cat-300/subcat-0/page-1/order-3/sp-2")

    res = taofen.getKind(html)
    # ensure_ascii=False将utf-8编码的中文正确显示
    res = json.dumps(res, ensure_ascii=False)
    print(res)
