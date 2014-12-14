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
        self.app = QApplication(sys.argv)  
        QWebPage.__init__(self)  
        self.loadFinished.connect(self._loadFinished)  
        self.urls = urls  
        self.data = {} # store downloaded HTML in a dict  
        self.crawl()  
        self.app.exec_()  


start = ''
end = ''

urls = [''] # url list
for i in range(start, end):  
    url = 'http://www.rt-drive.com.tw/shopping/index.php?st=16&trs=y&now_page=0&row_limit=1&product=' + str(i)
    urls.append(url)
  
r = Render(urls)