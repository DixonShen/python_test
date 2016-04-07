#coding=utf8
__author__ = 'DixonShen'

import bs4
from bs4 import BeautifulSoup
import os
import codecs
import MySQLdb
import MySQLdb.cursors

def GetFileList(dir, fileList):
    newDir = dir
    if os.path.isfile(dir):
        fileList.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            #如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            newDir=os.path.join(dir,s)
            GetFileList(newDir, fileList)
    return fileList

"""
qichacha data extract using bs4
"""

dict_link = {"注册号":"RegisterID","经营状态":"State","公司类型":"CompanyType","成立日期":"RegTime","法定代表":"LegalEntity","注册资本":"RegisterCapital","营业期限":"Period","登记机关":"Authority","发照日期":"IssueDate","住所":"Location","经营范围":"BusinessScope"}

list = GetFileList('C:\Users\DixonShen\Desktop\qichachatest', [])
for e in list:
    print e
    dict_info = {"CompanyName":"","RegisterID":"","RegisterCapital":"","State":"","Tel":"","Email":"","Website":"","CompanyType":"","RegTime":"","LegalEntity":"","Period":"","Authority":"","IssueDate":"","Location":"","BusinessScope":"","IECode":"","RCurrency":"","Currency":"","Capital":"","LocalTaxCode":"","StateTaxCode":"","QSCode":"","SIRCode":""}
    with codecs.open(e,'r') as filehandler:
        html_str = filehandler.read()
        soup = BeautifulSoup(html_str,"lxml")
        count = 1

        #maininfo
        # RegisterID,CompanyName,State,CompanyType,RegTime,LegalEntity,RegisterCapital,Tel,Email,Website,Period,Authority,IssueDate,Location,BusinessScope,IECode,RCurrency,Currency,Capital,LocalTaxCode,StateTaxCode,QSCode,SIRCode = '','','','','','','','','','','','','','','','','','','','','','',''
        try:
            dict_info['CompanyName'] = soup.find("a",class_="title").string
        except:
            continue
        tel = soup.find("p",class_="contact-info").descendants
        for te in tel:
            if count==3:
                dict_info['Tel'] = str(te).strip()
                # print Tel
            elif count==7:
                dict_info['Email'] = str(te).strip()
                # print Email
            count =count+1
        count = 1
        Website = ''
        website = soup.find("p",class_="contact-link").find_all("a")
        for web in website:
            Website = Website + str(web.get_text()) + ' '
            count = count + 1
        dict_info['Website'] = Website
        count = 1
        info1 = soup.find("ul",class_="company-info").find_all("li")
        for li in info1:
            str0 = str(li.get_text())
            str1 = str0.split('：')[0].strip()
            str2 = str0.split('：',1)[1].strip()
            dict_info[dict_link[str1]] = str2
        try:
            str_temp = str(soup.find("a",id="mapPreview").get_text()).decode('utf8')
            dict_info['Location'] = dict_info['Location'].strip(str_temp)
        except:
            pass

        # Partners
        PartnersName = []
        Details = []
        detail = ''
        partner = soup.find_all("div",class_="detail-partner-list")
        for ps in partner:
            partners = ps.find_all("p")
            count = 1
            for p in partners:
                if count==1:
                    PartnersName.append(p.get_text().strip())
                else:
                    detail = detail + p.contents[0].strip() + ' '
                count = count + 1
            Details.append(detail)
        count = 1

        #main employees
        EmName = []
        Position = []
        employee = soup.find_all("div",class_="people-block")
        for em in employee:
            EmName.append(em.find("h4").get_text().strip())
            Position.append(em.find("h5").get_text().strip())
        # for i in range(len(EmName)):
        #     print EmName[i],Position[i]

        #branches
        branches = []
        branch = soup.find_all("li",class_="list-group-item")
        for br in branch:
            branches.append(br.get_text().split('.')[1].strip())
        # for ep in branches:
        #     print ep

        #ChangeRecords
        ChangeItem = []
        ChangeBefore = []
        ChangeAfter = []
        ChangeDate = []
        try:
            change = soup.find("div",class_="company-record").find("table",class_="corde-table").find("tbody").find_all("tr")
            for c in change:
                for ctd in c.find_all("td"):
                    if count==1:
                        ChangeItem.append(ctd.get_text().strip())
                    elif count==2:
                        ChangeBefore.append(ctd.get_text().strip())
                    elif count==3:
                        ChangeAfter.append(ctd.get_text().strip())
                    else:
                        ChangeDate.append(ctd.get_text().strip())
                    count = count + 1
                count = 1
            # for i in range(len(ChangeItem)):
            #     print ChangeItem[i],'---\n',ChangeBefore[i],'---\n',ChangeAfter[i],'---\n',ChangeDate[i],'---\n'
        except:
            pass
        try:
            connection = MySQLdb.connect('127.0.0.1','root','','companycredit',charset='utf8')
        except:
            print "ERROR CONNECTING TO MYSQL"
        finally:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO maininfo
                               (RegisterID,CompanyName,State,CompanyType,RegTime,LegalEntity,RegisterCapital,Tel,Email,Website,Period,
                               Authority,IssueDate,Location,BusinessScope,IECode,RCurrency,Currency,Capital,LocalTaxCode,StateTaxCode,QSCode,SIRCode)
                               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                               """,(dict_info['RegisterID'],dict_info['CompanyName'],dict_info['State'],dict_info['CompanyType'],
                                    dict_info['RegTime'],dict_info['LegalEntity'],dict_info['RegisterCapital'],dict_info['Tel'],
                                    dict_info['Email'],dict_info['Website'],dict_info['Period'],dict_info['Authority'],dict_info['IssueDate'],
                                    dict_info['Location'],dict_info['BusinessScope'],dict_info['IECode'],dict_info['RCurrency'],
                                    dict_info['Currency'],dict_info['Capital'],dict_info['LocalTaxCode'],dict_info['StateTaxCode'],
                                    dict_info['QSCode'],dict_info['SIRCode']))
            for i in range(len(PartnersName)):
                cursor.execute("""INSERT INTO partners
                                  (RegisterID,PartnersName,Details)
                                  VALUES (%s,%s,%s)""",(dict_info['RegisterID'],PartnersName[i],Details[i]))
            for j in range(len(EmName)):
                cursor.execute("""INSERT INTO employees
                                  (RegisterID,EmName,Position)
                                  VALUES (%s,%s,%s)""",(dict_info['RegisterID'],EmName[j],Position[j]))
            for ep in branches:
                cursor.execute("""INSERT INTO branches
                                  (RegisterID,BranchName)
                                  VALUES (%s,%s)""",(dict_info['RegisterID'],ep))
            for k in range(len(ChangeItem)):
                cursor.execute("""INSERT INTO changerecords
                                  (RegisterID,ChangeItem,ChangeBefore,ChangeAfter,ChangeDate)
                                  VALUES (%s,%s,%s,%s,%s)""",(dict_info['RegisterID'],ChangeItem[k],ChangeBefore[k],ChangeAfter[k],ChangeDate[k]))
            connection.commit()
            cursor.close()
            print dict_info['CompanyName'].decode('utf8'),dict_info['RegisterID']
        filehandler.close()



# html_doc = """
# <html>
#  <head>
#   <base href='http://example.com/' />
#   <title>Example website</title>
#  </head>
#  <body>
#   <div id='images'>
#    <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
#    <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
#    <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
#    <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
#    <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
#   </div>
#  </body>
# </html>
# """