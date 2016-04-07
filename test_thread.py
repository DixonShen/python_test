#coding=utf-8
__author__ = 'DixonShen'

import time
import urllib2
from threading import Thread,Lock


#Sample3
lock = Lock()

class CreateListThread(Thread):
    def run(self):
        self.entries = []
        for i in range(100):
            time.sleep(0.5)
            self.entries.append(i)
        lock.acquire()
        print self.entries
        lock.release()

def use_create_list_thread():
    start = time.time()
    threads = []
    for i in range(3):
        t = CreateListThread()
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print time.time()-start

use_create_list_thread()


# #Sample2 多线程间资源竞争,
# #define a blobal variable
# lock = Lock()
# some_var = 0
#
# class IncrementThread(Thread):
#     def run(self):
#         #we want to read a global variable
#         #and then increment it
#         global some_var
#         lock.acquire()
#         read_value = some_var
#         print "some_var in %s is %d" % (self.name, read_value)
#         some_var = read_value + 1
#         print "some_var in %s after increment is %d" % (self.name, some_var)
#         lock.release()
#
# def use_increment_thread():
#     threads = []
#     for i in range(1000000):
#         t = IncrementThread()
#         threads.append(t)
#         t.start()
#     for t in threads:
#         t.join()
#     print "After 50 modifications, some_var should have become 50"
#     print "After 50 modifications, some_var is %d" % (some_var,)
#
# use_increment_thread()


#Multi Thread
# class GetUrlThread(Thread):
#     def __init__(self,url):
#         self.url = url
#         super(GetUrlThread, self).__init__()
#
#     def run(self):
#         resp = urllib2.urlopen(self.url)
#         print self.url,resp.getcode()
#
# def get_response():
#     urls = [
#         'http://www.baidu.com',
#         'http://www.sina.com.cn',
#         'http://www.qq.com',
#         'http://www.taobao.com',
#         'http://www.alibaba.com'
#     ]
#     start = time.time()
#     threads = []
#     for url in urls:
#         t = GetUrlThread(url)
#         threads.append(t)
#         t.start()
#     for t in threads:
#         t.join()
#     print "Elapsed time:%s" %(time.time()-start)
# get_response()


#Single Thread
# def get_responses():
#     urls = [
#         'http://www.baidu.com',
#         'http://www.sina.com.cn',
#         'http://www.qq.com',
#         'http://www.taobao.com',
#         'http://www.alibaba.com'
#     ]
#     start = time.time()
#     for url in urls:
#         print url
#         resp = urllib2.urlopen(url)
#         print resp.getcode()
#     print "Elapsed time: %s" % (time.time()-start)
#
# get_responses()