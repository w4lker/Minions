#!/usr/bin/python
#coding:utf-8

import threading
import time  
import thread
from db import database
from libmproxy import flow
from autosqli import AutoSqli
from xsscan.main import xsser
from flowhandle import *
from xsserscan import XsserScan



class Vulscan(threading.Thread):                    #漏洞(sql注入，xss等)扫描入口类，具体漏洞扫描模块在这里调用
    def __init__(self,flow):
        threading.Thread.__init__(self)
        self.flow = flow  
        
    def run(self):
        print "thread is running!"
        db = database()
        cur = db.connectdb('./db.sqlite3')
        sqlmap_srv = db.query(cur,'''select sqlmap_srv from webmanager_setting''')[0][0]
        db.closedb(cur)
        sqliscan = AutoSqli(server= sqlmap_srv,scan_flow = self.flow)
        thread.start_new_thread(sqliscan.run,())              #考虑到调用不同扫描模块，这里再次利用线程调用sqlmap
         
        xsserscan = XsserScan(scan_flow = self.flow) 
        thread.start_new_thread(xsserscan.run,())                #调用xsser

