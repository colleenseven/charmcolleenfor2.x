# __author__ = 'colleen'
# !/usr/bin/env python3
from bs4 import BeautifulSoup
import requests

# 抓取豆瓣排行榜电影
url = 'http://movie.douban.com/chart'
# page = urllib.request.urlopen(url).read().decode('utf-8')
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')


# 新片榜
NewRanking = soup.find('div', attrs={'class': 'indent'}).find_all('tr', attrs={'class': 'item'})
print('豆瓣新片榜---------------------------------------------------------------\n')
for item in NewRanking:
    name = item.find('img').attrs['alt']
    bintros = item.find('p').get_text()
    scores = item.find('span', attrs={'class': 'rating_nums'}).get_text()
    numcomments = item.find('span', attrs={'class': 'pl'}).get_text()
    print(name, bintros, scores, numcomments, '\n')


# 北美票房榜
NAranking = soup.find('div', id='ranking').find('ul', id='listCont1')
print('\n\n\n北美票房榜---------------------------------------------------------------')
print(NAranking.find('span', attrs={'class': 'box_chart_num color-gray'}).get_text(), '\n')

i = 1
money = NAranking.find_all('span')
for item in NAranking.find_all('a'):
    print('%2d' % i, item.get_text().strip(), money[i].get_text())
    i += 1
