#coding=utf8
__author__ = 'DixonShen'

from scrapy import Selector
import codecs
import os
from datetime import *
import time
import re

with codecs.open('nt1.txt','r') as fd:
    html_str = fd.read()
    fd.close()
    sel = Selector(text=html_str)
    tr = sel.xpath('//tr')
    print type(tr)
    i = 0
    for ttr in tr:
        td = ttr.xpath('.//td')
        if td:
            print i+1
            i = i+1
            # llist =
            ip = td[2].xpath('.//text()').extract()[0]
            port = td[3].xpath('.//text()').extract()[0]
            dt = td[9].xpath('.//text()').extract()[0]
            location =' '.join(td[4].xpath('.//descendant::text()').extract())
            sp = td[7].xpath('.//div[@class="bar"]/@title').extract()[0]
            sp = re.findall('\d+.\d+',sp).pop()
            ltime = td[8].xpath('.//div[@class="bar"]/@title').extract()[0]
            ltime = re.findall('\d+.\d+',ltime).pop()
            # if
            m = dt.split('-')
            year = '20' + m[0]
            month = m[1]
            day = m[2].split(' ')[0]
            ttime = m[2].split(' ')[1]
            hour = ttime.split(':')[0]
            min = ttime.split(':')[1]
            date1 = datetime(int(year),int(month),int(day),int(hour),int(min))
            date2= datetime.now()
            duration = timedelta(4)
            # print sp,ltime
            if ((date2-date1)<duration and float(sp)<=5 and float(ltime)<=2):
                print ip,':',port,\
                       location.strip(),\
                       td[5].xpath('.//text()').extract()[0],\
                       td[6].xpath('.//text()').extract()[0],\
                       sp,ltime,dt
                with codecs.open('ValidIP.txt','a') as filehandler:
                    filehandler.write(ip+':'+port+'\n')
                filehandler.close()

    #print sel.xpath('//tr[2]/td[3]/text()').extract().pop()
