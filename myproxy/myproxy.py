#!/usr/bin/env python
"""
This example builds on mitmproxy's base proxying infrastructure to
implement functionality similar to the "sticky cookies" option.

Heads Up: In the majority of cases, you want to use inline scripts.
"""
import os
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
import sys
from libs.db import database

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
        req = self.get_raw_req(flow)
        rsp = self.get_raw_rsp(flow)
        db = database()
        cur = db.connectdb('./db.sqlite3')
        sqlcmd = '''insert into webmanager_proxydata(status_code,method,host,url,request,response,timestamp)values(%d,'%s','%s','%s','%s','%s',%f)''' % (flow.response.status_code,flow.request.method,flow.request.host,flow.request.url,req,rsp,flow.request.timestamp_start)
        db.modify(cur,sqlcmd)        
        if flow.response.headers["set-cookie"]:
            self.stickyhosts[hid] = flow.response.headers["set-cookie"]
        flow.reply()
    
    def get_raw_req(self,flow):
        httpversion = "HTTP/" + str(flow.request.httpversion[0]) + '.' + str(flow.request.httpversion[1])
        req = flow.request.method +' ' + flow.request.url + ' ' + httpversion + '\n'
        for key,value in flow.request.headers:
            req += key + ':' +' ' + value + '\n'
        req += '\n' + flow.request.body 
        return req
    
    def get_raw_rsp(self,flow):
        httpversion = "HTTP/" + str(flow.response.httpversion[0]) + '.' + str(flow.response.httpversion[1])
        rsp = httpversion +' ' + str(flow.response.status_code) +' ' + flow.response.msg + '\n'
        for key,value in flow.response.headers:
            rsp += key + ':' +' ' + value + '\n'
        rsp += '\n' + flow.request.body 
        return rsp
        



