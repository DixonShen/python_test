#coding=utf8

__author__ = 'DixonShen'

import os
import codecs
from scrapy import Selector

def GetFileList(dir,filelist):
    if os.path.isfile(dir):
        filelist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newdir = os.path.join(dir,s)
            GetFileList(newdir,filelist)
    return filelist

"""
firm url extract using scrapy.Selector

"""
def get_And_save_url(flist):
    touzi = []
    firms = []
    persons = []
    count = 0
    for f in flist:
        # if count>=10:
        #     continue
        print f
        with codecs.open(f,'r') as fhandler:
            html_str = fhandler.read()
            fhandler.close()
        if '404错误' in html_str:
            with codecs.open('404.txt','a') as tempf:
                tempf.write(f+'\n')
                tempf.close()
            continue
        sel = Selector(text=html_str)
        try:
            name = sel.xpath('//title/text()').extract()[0].split('-')[0]
            print name
            touzi_url = sel.xpath('//a[@class="title"]/@href').extract()[0]
            url1 = 'www.qichacha.com' + touzi_url + '_touzi'
            touzi.append(url1)
            print url1
        except:
            pass
        try:
            maininfo = sel.xpath('//ul[@class="company-info"]')
            faren_url = maininfo.xpath('.//a/@href').extract()[0].split('&')[0].strip().encode('utf8') + '&index=opername'
            faren_url = faren_url.encode('utf8')
            persons.append(faren_url)
            print faren_url.decode('utf8')
        except:
            pass
        par = sel.xpath('//div[@class="detail-partner clearfix"]')
        for partner in par.xpath('.//a'):
            partner_url = partner.xpath('.//@href').extract()[0]
            if partner_url == faren_url:
                continue
            if 'firm' in partner_url:
                firm_url = 'www.qichacha.com' + partner_url
                firms.append(firm_url)
                print firm_url
            else:
                person_url = partner_url.split('&')[0].strip().encode('utf8') + '&index=opername'
                person_url = person_url.encode('utf8')
                persons.append(person_url)
                print person_url.decode('utf8')
        # count += 1
    with codecs.open('touziUrl.txt','a+') as fd1:
        for url in touzi:

            # if url in str1:
            #     with codecs.open('repeatedUrl.txt','a+') as fd4:
            #         fd4.write(url+'\n')
            #         print url
            #     continue

            fd1.write(url+'\n')
    fd1.close()
    with codecs.open('firmUrl.txt','a+') as fd2:
        for url in firms:

            # if url in str1:
            #     with codecs.open('repeatedUrl.txt','a+') as fd4:
            #         fd4.write(url+'\n')
            #     continue

            fd2.write(url+'\n')
    fd2.close()
    with codecs.open('personUrl.txt','a+') as fd3:
        for url in persons:

            # if url in str1:
            #     with codecs.open('repeatedUrl.txt','a+') as fd4:
            #         fd4.write(url+'\n')
            #     continue

            fd3.write(url+'\n')
    fd3.close()

def get_And_save_url1(list):
    count = 0
    firms = []
    persons = []
    touzi = []
    for f in list:
        # if count==10:
        #     break
        print f
        with codecs.open(f,'r') as fhandler:
            html_str = fhandler.read()
            fhandler.close()
        if '404错误' in html_str:
            with codecs.open('404.txt','a') as tempf:
                tempf.write(f+'\n')
                tempf.close()
            continue
        sel = Selector(text=html_str)
        name = sel.xpath('//h3[@class="detail-header-title"]/span/text()').extract()[0]
        print name
        firm = sel.xpath('//nav[@id="company-nav"]/p/a[1]/@href').extract()[0]
        firm_url = 'www.qichacha.com' + firm
        touzi_url = firm_url + '_touzi'
        firms.append(firm_url)
        touzi.append(touzi_url)
        print firm_url,'\n',touzi_url
        try:
            infos = sel.xpath('//ul[@class="company-info"]/li')
            for info in infos:
                info1 = info.xpath('.//text()').extract()[0]
                if info1=='法定代表：':
                    person = info.xpath('.//text()').extract()[1]
                    person_url = 'http://qichacha.com/search?key=' + person.strip().encode('utf8') + '&index=opername'
                    person_url = person_url.encode('utf8')
                    persons.append(person_url)
                    print person_url.decode('utf8')
                    break
        except:
            pass

        # count += 1
    with codecs.open('touziUrl1.txt','a+') as fd1:
        for url in touzi:

            # if url in str1:
            #     with codecs.open('repeatedUrl.txt','a+') as fd4:
            #         fd4.write(url+'\n')
            #         print url
            #     continue

            fd1.write(url+'\n')
    fd1.close()
    with codecs.open('firmUrl1.txt','a+') as fd2:
        for url in firms:

            # if url in str1:
            #     with codecs.open('repeatedUrl.txt','a+') as fd4:
            #         fd4.write(url+'\n')
            #     continue

            fd2.write(url+'\n')
    fd2.close()
    with codecs.open('personUrl1.txt','a+') as fd3:
        for url in persons:

            # if url in str1:
            #     with codecs.open('repeatedUrl.txt','a+') as fd4:
            #         fd4.write(url+'\n')
            #     continue

            fd3.write(url+'\n')
    fd3.close()

def get_list(flist):
    f = flist.pop()
    with codecs.open(f,'r') as fhandler:
        html_str = fhandler.read()
        fhandler.close()
    sel = Selector(text=html_str)
    for row in sel.xpath('//ul[@class="site-list-group"]/li'):
        name = row.xpath('.//h3/a/text()').extract()[0]
        firm_url = row.xpath('.//h3/a/@href').extract()[0]
        print name,firm_url


def get_url(flist):
    url_list = []
    for f in flist:
        with codecs.open(f,'r') as fhandler:
            urls = fhandler.read()
            url = 'www.qichacha.com/' + urls.split('/')[1]
        fhandler.close()
        url_list.append(url)
    with codecs.open('firmUrl2.txt','a+') as fd:
        for url in url_list:

            # if url in str1:
            #     with codecs.open('repeatedUrl.txt','a+') as fd4:
            #         fd4.write(url+'\n')
            #     continue

            fd.write(url+'\n')
        fd.close()



if __name__ == '__main__':
    flist = GetFileList('C:\Users\DixonShen\Desktop\qichachaNotLogin1',[])
    get_url(flist)
    print '读取完成！'.decode('utf8')