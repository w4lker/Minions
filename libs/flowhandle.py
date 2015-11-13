#!/usr/bin/python27
#coding:utf-8
import chardet
import magic
import base64
from libmproxy import flow
from db import database

def get_req_header(flow):
    httpversion = "HTTP/" + str(flow.request.httpversion[0]) + '.' + str(flow.request.httpversion[1])
    headers = flow.request.method +' ' + flow.request.url + ' ' + httpversion + '\n'
    for key,value in flow.request.headers:
        headers += key + ':' +' ' + value + '\n'  
    return headers


def get_raw_req(flow):
    """
    httpversion = "HTTP/" + str(flow.request.httpversion[0]) + '.' + str(flow.request.httpversion[1])
    req = flow.request.method +' ' + flow.request.url + ' ' + httpversion + '\n'
    for key,value in flow.request.headers:
        req += key + ':' +' ' + value + '\n'
    """
    headers = get_req_header(flow)
    req = headers + '\n' + flow.request.body
    req = req.replace("'","''")
    return req

def get_raw_rsp(flow):
    httpversion = "HTTP/" + str(flow.response.httpversion[0]) + '.' + str(flow.response.httpversion[1])
    rsp = httpversion +' ' + str(flow.response.status_code) +' ' + flow.response.msg + '\n'
    for key,value in flow.response.headers:
        rsp += key + ':' +' ' + value + '\n'
    body = flow.response.body
    
    db = database()
    cur = db.connectdb('./db.sqlite3')
    negative_type = db.query(cur,'''select value from webmanager_settings where setting='negative_type' ''')[0][0].split('|')
    print negative_type
    print type(negative_type)
    
    if flow.response.headers['content-type'] != []:
        content_type = flow.response.headers['content-type'][0].split(';')[0].split('/')[1].lower()       #如content-type存在，过滤content-type类型为css等
    else:
        m = magic.Magic(magic_file=r'C:\python27\magicfile\magic',mime=True)
        content_type = m.from_buffer(body)        
          
    if content_type in negative_type:
        body = base64.b64encode(body)
    else:
        if chardet.detect(body)['encoding']:
            encode_type = chardet.detect(body)['encoding']
            body = body.decode(encode_type,'replace')        
    rsp += '\n' + body     
    rsp = rsp.replace("'","''")
    return rsp
