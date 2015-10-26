#!/usr/bin/env python
#coding:utf-8
"""
This example builds on mitmproxy's base proxying infrastructure to
implement functionality similar to the "sticky cookies" option.

Heads Up: In the majority of cases, you want to use inline scripts.
"""
import os
import string
import sys
import urlparse
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
from libs.db import database
from libs.flowhandle import *
from libs.vulscan import Vulscan
import threading
import time
import base64
import magic


class StickyMaster(controller.Master):
    def __init__(self, server):
        controller.Master.__init__(self, server)
        self.stickyhosts = {}

    def run(self):
        try:
            return controller.Master.run(self)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_request(self, flow):
        hid = (flow.request.host, flow.request.port)
        if flow.request.headers["cookie"]:
            self.stickyhosts[hid] = flow.request.headers["cookie"]
        elif hid in self.stickyhosts:
            flow.request.headers["cookie"] = self.stickyhosts[hid]
        flow.reply()      
        
    def handle_response(self, flow):
        
        hid = (flow.request.host, flow.request.port)
                  
        if flow.response.headers["set-cookie"]:
            self.stickyhosts[hid] = flow.response.headers["set-cookie"]
        flow.reply()
        db = database()
        cur = db.connectdb('./db.sqlite3')
        negative_type = db.query(cur,'''select negative_type from webmanager_setting''')[0][0].split('|')
        if flow.response.headers['content-type'] != []:
            content_type = flow.response.headers['content-type'][0].split(';')[0].split('/')[1].lower()       #如content-type存在，过滤content-type类型为css等
        else:
            content_type = ''                                                            #不存在，过滤url中的文件类型类型为css等
        file_type = urlparse.urlparse(flow.request.url)[2].split('.')[-1].lower()
        if file_type not in negative_type:# and file_type not in negative_type:           
            req = get_raw_req(flow)
            rsp = get_raw_rsp(flow)
            sqlcmd = '''insert into webmanager_proxydata(status_code,method,host,url,request,response,timestamp)values(%d,'%s','%s','%s','%s','%s',%f)''' % (flow.response.status_code,flow.request.method,flow.request.host,flow.request.url,req,rsp,flow.request.timestamp_start)
            db.modify(cur,sqlcmd)    
            db.closedb(cur)
            v = Vulscan(flow)                  #调用扫描类，进行扫描，测试网站http://www.tjwfn.com/net_list.jsp?ieb12eki&zxlb=1
            v.start()          

    



