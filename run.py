#�����ű���������ڣ��������������Django��web����

import os
from libmproxy import controller, proxy
from libmproxy.proxy.server import ProxyServer
from libs.db import *
from myproxy.myproxy import StickyMaster


config = proxy.ProxyConfig(port=8088)
server = ProxyServer(config)
m = StickyMaster(server)
m.run()



