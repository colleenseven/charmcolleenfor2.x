# /usr/bin/env python
# -*- coding:utf-8 -*-
import re

from bs4 import BeautifulSoup  # HTML

doc = ['<html><head><title>Page title</title></head>',
       '<body><p id="firstpara" align="center">This is paragraph <b>one</b>.',
       '<p id="secondpara" align="blah">This is paragraph <b>two</b>.', '</html>']
# BeautifulSoup 接受一个字符串参数
soup = BeautifulSoup(''.join(doc), "html.parser")
print type(soup)
print type(soup.html)
print type(soup.title.string)

# BeautifulSoup文档树有三种基本对象
print
# BeautifulSoup对象
html = soup.html
print type(html)
print html

print
# BeautifulSoup.Tag
title = soup.title
print type(title)
print title

print
# BeautifulSoup.NavigableString
contents = soup.contents
print type(contents)
print contents

print
# 使用contents方法查看文档树层级结构
print len(soup.contents[0].contents)
print soup.contents[0].contents[0]
print soup.contents[0].contents[1]
print len(soup.contents[0].contents[0])
print soup.contents[0].contents[0].contents[0]
print soup.contents[0].contents[0].contents[0].contents[0]


# 获取树的子代元素，类似深度遍历
print
head = html.next
print type(head)
print head

print
title = head.next
print type(title)
print title

print
title_content = title.next
print type(title_content)
print title_content

print
body = title_content.next
print type(body)
print body


# 使用replacewith方法替换对象
print
print head
print head.parent
head.replaceWith('head was replace')
print head.parent  # 输出空，因为原数据保留并被剪除
print head  # 没有改变正常输出
print soup.head  # 输出空，head对象已不存在
print soup  # 文档对象已经被修改

print
# 使用find,findAll方法进行搜索
print soup.findAll('p')
print
print soup.findAll('p', id='firstpara')
print
# 传一个属性或多个属性对
print soup.findAll('p', {'align': 'blah'})
# 使用正则表达式
print soup.findAll(id=re.compile("para$"))


# 读取和修改属性
print
p1 = soup.p
print p1
print p1['id']
p1['id'] = 'changeid'
print p1  # 已被修改
print soup  #文档对象已经被修改
