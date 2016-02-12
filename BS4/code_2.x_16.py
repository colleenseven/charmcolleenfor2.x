# __author__ = 'colleen'
import urllib


def get_content(url):
    """
    获取网页源码
    """
    html = urllib.urlopen(url)
    content = html.read()
    html.close()
    return content


def get_name(name, file):
    """
    抓取图片文件名
    """
    self.picName = name.decode('utf-8')
    if "*" in self.picName:
        self.picName = self.picName.replace("*", "")
    elif "/" in self.picName:
        self.picName = self.picName.replace("/", "")
    print self.picName


def get_file(info):
    """
    获取img文件
    """
    soup = BeautifulSoup(info, "html.parser")
    all_files = soup.find_all('a', title="免费下载")
    titles = soup.find_all('h1')
    for title in titles:
        name = str(title)[4:-5]

    for file in all_files:
        get_name(name, file)


def pic_category(str_images):
    """
    下载图片
    """
    soup = BeautifulSoup(info, "html.parser")
    all_image = soup.find_all('div', class_="large-Imgs")
    images = str_images
    pat = re.compile(images)
    image_code = re.findall(pat, str(all_image))
    for i in image_code:
        if str(i)[-3:] == 'gif':
            image = urllib.urlretrieve('http://www.cssmoban.com' + str(i),
                                       'E:\\googleDownLoad\\\cssmuban\\' + str(self.picName).decode('utf-8') + '.gif')
        else:
            image = urllib.urlretrieve('http://www.cssmoban.com' + str(i),
                                       'E:\\googleDownLoad\\\cssmuban\\' + str(self.picName).decode('utf-8') + '.jpg')


def pic_download(info):
    """
    下载图片
    """
    pic_category(r'src="(.+?\.gif)"')
    pic_category(r'src="(.+?\.jpg)"')


self.num = 1
for i in range(6000):
    url = 'http://www.cssmoban.com/cssthemes/' + str(self.num) + '.shtml'
    info = get_content(url)
    get_file(info)
    pic_download(info)
    self.num = self.num + 1
