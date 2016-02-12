# __author__ = 'colleen'
# coding=utf-8
'''this url is http://www.cnblogs.com/sxcmos/p/5163537.html,there are some problem about csv file'''
import urllib2
import os

from bs4 import BeautifulSoup

url = 'http://wooyun.org/corps/page/'
total_page = 44
count = 1

filepath = os.getcwd() + "\wooyun"
if not os.path.exists(filepath):
    os.mkdir(filepath)
file = open(filepath + '\wooyunCS1.xlsx', 'w')

for num in range(1, total_page + 1):
    real_url = url + str(num)
    response = urllib2.urlopen(real_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    for i in range(0, len(soup('td', width='370'))):
        if i % 2 == 0:
            name = soup('td', width='370')[i].get_text()
            link = soup('td', width='370')[i + 1].get_text()
            print name, ':', link
            file.write(str(count) + ',' + name.encode('utf-8') + ',' + link.encode('utf-8') + '\n')
            count += 1

file.close()
print "OVER"

# 总结：
# 存储CSV时候的格式： 用 + ',' + 格式，就会把每个参数分开成每一列存储
# 所需要的内容交替出现时，可用取位置的方法，偶数行和奇数行来分别取
# 在此例中使用str(num)，比使用re.sub()简便
