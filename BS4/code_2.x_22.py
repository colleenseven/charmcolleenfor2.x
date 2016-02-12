# __author__ = 'colleen'
# !/usr/bin/env python3
from bs4 import BeautifulSoup
import requests

# ץȡ�������а��Ӱ
url = 'http://movie.douban.com/chart'
# page = urllib.request.urlopen(url).read().decode('utf-8')
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')


# ��Ƭ��
NewRanking = soup.find('div', attrs={'class': 'indent'}).find_all('tr', attrs={'class': 'item'})
print('������Ƭ��---------------------------------------------------------------\n')
for item in NewRanking:
    name = item.find('img').attrs['alt']
    bintros = item.find('p').get_text()
    scores = item.find('span', attrs={'class': 'rating_nums'}).get_text()
    numcomments = item.find('span', attrs={'class': 'pl'}).get_text()
    print(name, bintros, scores, numcomments, '\n')


# ����Ʊ����
NAranking = soup.find('div', id='ranking').find('ul', id='listCont1')
print('\n\n\n����Ʊ����---------------------------------------------------------------')
print(NAranking.find('span', attrs={'class': 'box_chart_num color-gray'}).get_text(), '\n')

i = 1
money = NAranking.find_all('span')
for item in NAranking.find_all('a'):
    print('%2d' % i, item.get_text().strip(), money[i].get_text())
    i += 1
