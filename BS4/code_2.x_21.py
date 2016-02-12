# __author__ = 'colleen'
# !/usr/bin/python
"""
parser
    for parsing html file from leiphone.com and 36kr.com
author
    xiaoyang
contact
    hityixiaoyang@gmail.com
version

describe
    parse a html file from leiphone.com
log
   1.2012-11-22 create
   2.2012-11-23 add FileCollect and ParseTask class
   3.2012-11-23 add MutiThreads support
"""

import sys
import os
import Queue
import threading
import re

from bs4 import BeautifulSoup


# for mutithread,you shouldn't change these vars directly
OUT_CNT_LOCK = threading.Lock()
PRINT_LOCK = threading.Lock()
OUT_FILE_PREFIX = "out"
WORKER_NUM = 8
OUT_CNT = 0
MAX_ITEM_CNT = 100
PRINT_DBG = True

# for debug
FileCollectDBG = False
ParseTaskDbg = False


# error print and exit ,thread safety
def errPrint(ifExit=True, msg='_'):
    global PRINT_LOCK
    try:
        if PRINT_LOCK.acquire(10):
            print >> sys.stderr, msg
            if ifExit:
                sys.exit()
    finally:
        PRINT_LOCK.release()


# dbg print
def dbgPrint(msg):
    global PRINT_LOCK
    if PRINT_LOCK.acquire(10):
        print msg
    PRINT_LOCK.release()


import inspect


def lineno():
    """Returns the current line number in our program."""
    line = inspect.currentframe().f_back.f_lineno
    return str(line)


# for LeiPhone.com
def SaveResLP(doc, filename, mode="a"):
    fp = None
    try:
        fp = open(filename, mode)
        fp.write(doc)
    except IOError as errStr:
        dbgPrint("lines:" + lineno())
        errPrint(True, errStr)
    finally:
        fp.close()
    return True


# foe 36kr.com
def SaveRes36K(doc, filename):
    return True


class FileCollect:
    def __init__(self, root):
        if root[len(root) - 1] != '\\':
            root += "\\"
        self.root = root
        self.dlist = []
        self.fqueue = Queue.Queue(0)

    def init(self):
        for root, dirs, files in os.walk(self.root):
            self.dlist += dirs
            for afile in files:
                # if file ends with '.html',add it
                if re.search('.html$', afile) is not None:
                    self.fqueue.put(root + afile)
        return True


class ParseTask:
    def __init__(self, savedFileName=None):
        self.soup = None
        self.savedFileName = savedFileName

    def parse(self, readFileName):
        fp = None
        content = None
        try:
            fp = open(readFileName, "r")
            if fp is not None:
                self.soup = BeautifulSoup(fp.read())
            else:
                msg = "fopen" + readFileName + "failed"
                errPrint(True, msg)
            content = self.soup.find("article")
            if content is not None:
                # self.soup = BeautifulSoup(str(content))
                # remove other tags
                tag = content.find("p").find("a")
                if not tag:
                    return False
                tag.clear()

                tag = content.find("footer")
                if not tag:
                    return False
                tag.clear()

                tag = content.find(class_="alipayzone")
                if not tag:
                    return False
                tag.clear()

                tag = content.find(class_="authorpigtwo")
                if not tag:
                    return False
                tag.clear()

                tag = content.find(id="jiathis_style_32x32")
                if not tag:
                    return False
                tag.clear()

                tag = content.find(class_="wumii-hook")
                if not tag:
                    return False
                tag.clear()

                tag = content.find("center")
                if not tag:
                    return False
                tag.clear()

                tags = content.find_all(rel="bookmark")
                for tag in tags:
                    tag.clear()
                SaveResLP(str(content), self.savedFileName)
            else:
                return False
            # file handled done
            return True
        except IOError as errStr:
            errPrint(True, errStr)
        except Exception as errStr:
            dbgPrint("lines:" + lineno())
            errPrint(True, errStr)
            # errPrint(True,errStr)
        finally:
            if fp is not None:
                fp.close()


# get out filename,thread safety
def newOutName():
    global OUT_CNT_LOCK
    # block here until get the lock
    if (OUT_CNT_LOCK.acquire(10)):
        # get the lock
        global OUT_CNT
        OUT_CNT += 1
        filename = str(OUT_FILE_PREFIX) + str(OUT_CNT) + str(".html")
        OUT_CNT_LOCK.release()
        return filename


class TaskThread(threading.Thread):
    def __init__(self, tid, tname, queue):
        threading.Thread.__init__(self, name=tname)
        self.tid = tid
        self.queue = queue
        self.parserTask = None
        self.stop = False
        self.savedCnt = 0

    def run(self):
        outName = newOutName()
        self.parserTask = ParseTask()
        while not self.stop:
            try:
                # if no obj exist,throw exception
                inName = self.queue.get_nowait()
                dbgPrint("handle:" + inName)
                self.parserTask.savedFileName = outName
                if self.parserTask.parse(inName):
                    self.savedCnt += 1
                    if self.savedCnt > MAX_ITEM_CNT:
                        # create new saved file
                        outName = newOutName()
                        self.savedCnt = 0
                else:
                    # parsed failed
                    continue
            except Queue.Empty:
                self.stop = True
                if self.savedCnt != 0:
                    msg = "ethread [" + self.name + "] out:'" + outName + "' with " + str(
                        self.savedCnt) + " items success"
                    errPrint(False, msg)
                else:
                    msg = "ethread [" + self.name + "] exit with " + str(self.savedCnt) + " items"
                    errPrint(False, msg)
                return
            except Exception as ex:
                errPrint(True, "lines:" + lineno() + "," + ex)
                return


# main
def main():
    taskThreads = {}
    # fc = FileCollect("E:\project\python\Parser\page")
    fc = FileCollect("F:\myweb\leiphone\web")
    print "Start add files..."
    fc.init()
    print "Added files count:%d" % fc.fqueue.qsize()
    print("Starting threads ...")
    try:
        for tid in range(0, WORKER_NUM):
            tobj = TaskThread(tid, "thread-" + str(tid), fc.fqueue)
            taskThreads[tid] = tobj
            tobj.start()
        for tid in range(0, WORKER_NUM):
            taskThreads[tid].join()
    except Exception as ex:
        errPrint(True, ex)
    print('All threads have terminated.')


if __name__ == '__main__':
    main()
    afile = "03-31-dan-talk-omgpop.html"
    if re.search('.html$', afile) is not None:
        print "matched!"
    else:
        print "mismatched!"
    if re.search('.jpg$', afile) is not None:
        print "matched2!"
