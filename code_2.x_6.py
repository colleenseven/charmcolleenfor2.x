#__author__ = 'colleen'
import urllib
from selenium import webdriver
import os
import BeautifulSoup

base_dir = os.path.join(os.getcwd(), "nationalgeographic")
if not os.path.exists(base_dir):
    os.mkdir(base_dir)

base_url = 'http://photography.nationalgeographic.com/photography/photo-of-the-day'

driver = webdriver.Firefox()
driver.get(base_url)

previois_link = driver.find_element_by_partial_link_text('Previous')

while previois_link:
    print 'current url is: ', driver.current_url
    content = urllib.urlopen(driver.current_url).read()
    soup = BS(content)
    urls = soup.findAll('img', width = '990')
    for url in urls:
        url = url["src"]
        filename = base_dir + '\\' + url.split('/')[-1]
        urllib.urlretrieve(url, filename)
        print 'download', filename, 'to', base_dir
    previois_link = driver.find_element_by_partial_link_text('Previous')
    previois_link.click()
    driver.refresh()
    print 'after refresh', driver.current_url