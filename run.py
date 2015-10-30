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

#config = proxy.ProxyConfig(mode='upstream',port=8088,upstream_server=u_s)
config = proxy.ProxyConfig(port=8088)
server = ProxyServer(config)
m = StickyMaster(server)
m.run()



