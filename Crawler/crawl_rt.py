import sys
import MySQLdb
import time
import datetime
import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from bs4 import BeautifulSoup

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
        print title.text

start = ''
end = ''

urls = ['http://ec.rt-mart.com.tw/direct/index.php?action=product_detail&prod_no=P0000200036340'] # url list
'''
for i in range(start, end):  
    url = 'http://www.rt-drive.com.tw/shopping/index.php?st=16&trs=y&now_page=0&row_limit=1&product=' + str(i)
    urls.append(url)
'''  
r = Render(urls)