#coding:utf-8
#启动脚本，程序入口，负责启动代理和Django的web服务

import os
import string
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
from libs.db import *
from myproxy.myproxy import StickyMaster
from libs.flowhandle import *
from libs.db import database

"""
db = database()
cur = db.connectdb('./db.sqlite3')
settings = db.query(cur,'''select value from webmanager_settings where module='proxy' ''')
db.closedb(cur)

p_e = settings[0][0]
p = int(settings[1][0])
u_p = settings[2][0].split(':')
n_t = settings[3][0].split('|')
t = settings[4][0].split(';')
u_e = settings[5][0]


u_s = [False, False,u_p[0], int(u_p[1])]
c_d = os.path.expanduser("~/.mitmproxy/")
print c_d

if u_e == 'true':
    config = proxy.ProxyConfig(mode='upstream',port=p,upstream_server=u_s)
else:
    config = proxy.ProxyConfig(port=p)

server = ProxyServer(config)
m = StickyMaster(server,proxy_enabled=p_e,negative_type=n_t,target=t)
m.run()
"""

#coding:utf-8
#启动脚本，程序入口，负责启动代理和Django的web服务

import os
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
from libs.db import *
from myproxy.myproxy import StickyMaster
from libs.flowhandle import *


u_s = [False, False,"proxy.zte.com.cn", 80]
c_d = os.path.expanduser("~/.mitmproxy/")

config = proxy.ProxyConfig(mode='upstream',port=8088,upstream_server=u_s)
#config = proxy.ProxyConfig(port=8088)
server = ProxyServer(config)
m = StickyMaster(server)
m.run()


