#__author__ = 'colleen'
#!/usr/bin/env python
#coding=utf-8
import urllib
import urllib2
import re
import pymongo
def getHtml(url):
    page=urllib2.urlopen(url)
    html=page.read()
    page.close()
    return html

def getContent(html):
    reg=r'<li class="poster">.+?src="(.+?\.jpg)".+?</li>.+?class="title".+?
       class="">(.+?)</a>.+?class="rating".+?class="subject-rate">(.+?)</span>.+?<a onclick=".+?">(.+?)</a>'
    contentre=re.compile(reg,re.DOTALL)
    contentlist=contentre.findall(html)
    return contentlist

def getConnection(): #拿到数据库连接
    conn=pymongo.Connection('localhost',27017)
    return conn

def saveToDB(contentlist): #存储至mongodb数据库中
    conn=getConnection()
    db=conn.db
    t_movie=db.t_movie
    for content in contentlist:
        value=dict(poster=content[0],title=content[1],rating=content[2],ticket_btn=content[3])
        t_movie.save(value)

def display(contentlist):
    for content in contentlist:
        #values=dict(poster=content[0],title=content[1],rating=content[2],ticket_btn=content[3])
        print 'poster','\t',content[0]
        print 'title','\t',content[1]
        print 'rating','\t',content[2]
        print 'ticket_btn','\t',content[3]
        print'..............................................................................'

if __name__=="__main__":
    url="http://movie.douban.com/"
    html=getHtml(url)
    #print html
    contentlist=getContent(html)
    print len(contentlist)
    #print contentlist
    display(contentlist)
    saveToDB(contentlist)
    print "finished"