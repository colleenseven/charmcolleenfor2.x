# __author__ = 'colleen'
# coding=utf-8
# Creeper
import os
import urllib2
import datetime
import warnings
import traceback
import ConfigParser

import bs4

import MySQLdb

try:
    basedir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    import sys

    basedir = os.path.dirname(os.path.abspath(sys.argv[0]))

SETTINGS_FILE = os.path.join(basedir, 'settings.ini')
GLOBAL_CONFIG = {
    'server': {
        'debug': False,
    },
    'db': {
        'host': '127.0.0.1',
        'port': '3306',
        'user': 'root',
        'password': '',
        'dbname': 'test',
        'table': 'group'
    }
}


def __config(item):
    GLOBAL_CONFIG[sec][item[0]] = item[1]


try:
    parser = ConfigParser.ConfigParser()
    parser.readfp(open(SETTINGS_FILE))
    for sec in parser.sections():
        map(__config, parser.items(sec))
except:
    print 'settings.ini needed'
    raise

N = 0


class Handle(object):
    def __init__(self, *args, **kwargs):
        super(Handle, self).__init__()
        self.db = {}
        self.conn = None
        self.cursor = None
        self._cursor(**kwargs)

    def _cursor(self, **kwargs):
        self.db.update(**kwargs)
        host = kwargs.get('host', '127.0.0.1')
        port = int(kwargs.get('port', 3306))
        user = kwargs.get('user', 'root')
        pwd = kwargs.get('password', '')
        dbname = kwargs.get('dbname', 'test')
        charset = kwargs.get('charset', 'utf8')
        _conn = MySQLdb.connect(user=user, passwd=pwd,
                                host=host, port=port, charset=charset)
        try:
            _conn.select_db(dbname)
        except:
            sql = """CREATE DATABASE IF NOT EXISTS `%s` DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
                  """ % dbname
            _conn.cursor().execute(sql)
            _conn.select_db(dbname)
        self.conn = _conn
        self.cursor = _conn.cursor()

    def format_pk(self, pk, index):
        d = {1: 2, 2: 4, 3: 6, 4: 9, 5: 12}
        try:
            pk = int(float(pk))
        except:
            raise ValueError, 'the primary key must be integer or string interger'
        return int(str(pk)[:d[index]])
        while (pk * 1.0 / 10).is_integer():
            pk = pk * 1.0 / 10
        return pk < 10 and int(pk) * 10 or int(pk)

    def do_execute(self, pk, name, type, parent='NULL'):
        global N
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')
        if N % 100 == 0 and N != 0:
            print 'Total: %s ---%s' % (N, now)
            # time.sleep(5)
        if not parent or parent == '':
            parent = 'NULL'
        sql = """INSERT INTO `%s` (`id`, `name`, `type`, `parent`) VALUES(%s, '%s', '%s', %s);
              """ % (self.db['table'], pk, name, type, parent)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print '+',
            N += 1
        except MySQLdb.Warning, w:
            print "\nWarning:%s" % str(w)
            print '#',
        except MySQLdb.Error, e:
            if not 'Duplicate entry' in str(e):
                print "\nError:%s" % str(e)
                self.debug(pk, name)
                self.debug(pk, parent)
            else:
                print '=',
                self.debug(pk, name)
        except:
            traceback.print_exc()
            print '?',

    def do_executemany(self, items, params=None):
        sql = """INSERT INTO `%s` (`id`, `name`, `type`, `parent`) VALUES """ % self.db['table']
        sql += "(%s, %s, %s, %s)";
        try:
            self.cursor.executemany(sql, items)
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Error:%s" % str(e)
        except:
            traceback.print_exc()


class Creeper(Handle):
    def __init__(self, *args, **kwargs):
        Handle.__init__(self, *args, **kwargs)
        self.init_db()
        self.root_url = ''
        self._type = {1: 'province', 2: 'city', 3: 'county', 4: 'town', 5: 'village'}

    def init_db(self):
        __sql = """CREATE TABLE IF NOT EXISTS `%s` (
          `id` bigint(20) NOT NULL,
          `name` varchar(30) NOT NULL,
          `type` varchar(30) NOT NULL,
          `parent` bigint(20) DEFAULT NULL,

          PRIMARY KEY (`id`),
          KEY `Group_12345` (`name`),
          KEY `Group_67890` (`parent`),
          FOREIGN KEY(parent) REFERENCES `%s` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """ % (self.db['table'], self.db['table'])

        try:
            self.cursor.execute(__sql)
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS `debug` (
                  `id` int(11) NOT NULL AUTO_INCREMENT,
                  `badid` bigint(20) NOT NULL,
                  `others` varchar(256) DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;""")
            self.conn.commit()
        except MySQLdb.Warning, w:
            if not 'already exists' in str(w):
                print "Warning:%s" % str(w)
        except MySQLdb.Error, e:
            print "Error:%s" % str(e)
            traceback.print_exc()
        except:
            traceback.print_exc()
            pass

    def debug(self, *args):
        try:
            _sql = """INSERT INTO `debug` (`badid`, `others`) VALUES(%s, '%s');
                   """ % (args[0], args[1])
            self.cursor.execute(_sql)
            self.conn.commit()
        except:
            traceback.print_exc()
        finally:
            return

    def __get_url(self, tup, index):
        id = tup[0]
        parent = tup[-1]
        __url = []
        for i in range(0, index, 2):
            __url.append(str(id)[i: i + 2])
        __url.append(str(id))
        return self.root_url + '/'.join(__url) + '.html'

    def format_tag(self, x_tag, url, index, limit=None):
        if limit and index > limit: return
        parent = str(url.split('/2013/')[1].split('/')[-1])[:-5]
        __type = self._type[index]
        __parent = not parent and 'NULL' or parent
        if isinstance(x_tag, bs4.element.Tag) and x_tag.has_attr('href'):
            print '.',
            href = x_tag['href']
            child_url = '/'.join(url.split('/')[:-1])
            full_url = '/'.join([child_url, href])
            __pk = self.format_pk(href.split('.html')[0].split('/')[-1], index)
            __name = x_tag.text
            i = (__pk, __name, __type, __parent)
            self.do_execute(*i)
            self.get_info(full_url, index + 1, limit)
        else:
            print '*',
            __pk = self.format_pk(x_tag[0].text, index)
            __name = x_tag[1].text
            self.do_execute(__pk, __name, __type, __parent)

    def get_info(self, url, index, limit=None):
        # 解析页面,获取目标区域的数据
        # 获取单元数据,格式化为可供插入数据库的元组
        try:
            __html = urllib2.urlopen(url).read()
            __soup = bs4.BeautifulSoup(__html, from_encoding='gbk')
            __tr = __soup('tr', class_='%str' % self._type[index])
        except:
            try:
                self.debug(0, url)
            except:
                traceback.print_exc()
            finally:
                return
        __lst = []
        for tr in __tr:
            # 每个tr中的多个td代表多个省
            if index == 1:
                for td in tr('td'):
                    __lst.extend(td('a'))
                continue

            # 每个tr中的多个td代表一个节点,取最后一个td中的a标签
            if tr('td')[-1]('a'):
                __lst.extend(tr('td')[-1]('a'))
            else:
                # 没有子节点的元素,单纯的通过td中的数据创建
                self.format_tag([tr('td')[0], tr('td')[-1]], url, index, limit)

        for a in __lst:
            self.format_tag(a, url, index, limit)

    def do_get_childs(self, index):
        # 1. 查询获取当前层级节点数目
        _sql = """SELECT COUNT( * ) FROM  `%s` WHERE `type`='%s';
               """ % (self.db['table'], self._type[index])
        self.cursor.execute(_sql)
        total = self.cursor.fetchone()[0]

        # 2. 遍历父节点,获取子节点数据
        for i in range(0, total, 30):
            _sql = """SELECT `id`, `parent` FROM `%s` WHERE `type` = '%s' LIMIT %s, %s;
                   """ % (self.db['table'], self._type[index], i, i + 30)
            self.cursor.execute(_sql)
            id_and_parent = list(set(self.cursor.fetchall()))
            for tup in id_and_parent:
                url = self.__get_url(tup, index)
                self.get_info(url, index + 1)


warnings.filterwarnings('error', category=MySQLdb.Warning)
del warnings

if __name__ == '__main__':
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/"
    db_config = GLOBAL_CONFIG['db']
    g = Creeper(**db_config)
    g.root_url = url
    g.init_db()
    lst = g.get_info(url, index=1, limit=5)
    # g.do_get_childs(3)
