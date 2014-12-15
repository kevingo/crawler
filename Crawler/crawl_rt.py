import sys
import MySQLdb
import time
import datetime
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from bs4 import BeautifulSoup

db = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='', db="crawl_products", charset='utf8')
cursor = db.cursor()     

class Render(QWebPage):
    
    def __init__(self, urls):  
        print 'init'
        self.app = QApplication(sys.argv)  
        QWebPage.__init__(self)  
        self.loadFinished.connect(self._loadFinished)  
        self.urls = urls  
        self.data = {} # store downloaded HTML in a dict  
        self.crawl()  
        self.app.exec_()  
    
    def crawl(self):
        print 'crawl'
        if self.urls:      
            url = self.urls.pop(0)
            self.mainFrame().load(QUrl(url))      
        else:  
            self.app.quit()  
        
    def _loadFinished(self, result):  
        print 'loadFinished'
        frame = self.mainFrame()  
        url = str(frame.url().toString())
        html = frame.toHtml().toUtf8()    
        self.parse(html, url)
        self.crawl()  
    
    def parse(self, html, url):
        print 'parse'
        soup = BeautifulSoup(''.join(html))
        title = soup.title
        
        name = title.text
        price = soup.find('span', {'class':'price_num'}).get_text().replace('$', '').strip()
        div_rItems = soup.find('div', {'class':'product_indexPro'}).find_all('div', {'class':'indexProList'})
        r_items = ''
        for i in range(len(div_rItems)):
            r_name = div_rItems[i].find('h5', {'class':'for_proname'}).get_text()
            r_price = div_rItems[i].find('div', {'class':'for_pricebox'}).get_text().replace('$', '').strip()
            r_url = div_rItems[i].find('h5', {'class':'for_proname'}).a['href']
            r_image = div_rItems[i].find('div',{'class':'for_imgbox'}).img['src']
            
            r_items += r_name + '||' + r_price + '||' + r_url + '||' + r_image
        
        date = datetime.datetime.now()    
        source = url
        html_src = html
        also_like = ''
        buy_and_buy = ''
        see_and_see = ''
        source_pid = soup.find('h3',{'class':'subproductname'}).get_text()
        version = 'v1'

        classify = ''
        category = soup.find('div',{'class':'siteMargin'}).find_all('li')
        for i in range(len(category)):
            if i % 2 == 0 and i <> 0 and i <> len(category)-1:
                classify += category[i].find('a').get_text()
        
        original_price = soup.find('span', {'class':'price_snum'}).get_text().replace('$','').strip()
        origin = 'rt'
        
        self.writedb(name, price, r_items, date, source, html_src, also_like, buy_and_buy, see_and_see, source_pid, version
                     ,classify, original_price, origin)
    
    def writedb(self, name, price, r_items, date, source, html_src, also_like, buy_and_buy, see_and_see, source_pid, version
                     ,classify, original_price, origin):
        print 'write db'
        
        query = 'INSERT INTO c_products(name, price, r_items, date, source, html_src, also_like, buy_and_buy, see_and_see, source_pid, version, classify, original_price, origin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        args = (name, price, r_items, date, source, html_src, also_like, buy_and_buy, see_and_see, source_pid, version
                     ,classify, original_price, origin)       
        try:
            cursor.execute(query, args)
            db.commit()
        except Exception:
            e_type, msg, traceback = sys.exc_info()
            print msg
            db.rollback()
        
        db.close()
        
start = 1
end = 99999

urls = ['http://ec.rt-mart.com.tw/direct/index.php?action=product_detail&prod_no=P0000200057532'] # url list
'''
for i in range(start, end):  
    url = 'http://www.rt-drive.com.tw/shopping/index.php?st=16&trs=y&now_page=0&row_limit=1&product=' + str(i)
    urls.append(url)
'''  
r = Render(urls)

