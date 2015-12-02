from libs.xsscan.main import xsser
from libs.flowhandle import *
from libmproxy import flow

class XsserScan(object):
    def __init__(self,scan_flow = ''):
        self.flow = scan_flow
        """
        self.options['url'] = self.flow.request.url
        self.options['postdata']  = self.flow.request.body
        self.options['headers'] = get_req_header(self.flow)
        """
    
    def run(self):
        app = xsser()
        options = app.create_options()
        options.url = self.flow.request.url
        options.fuzz = True
        options.heuristic = True
        if self.flow.request.body != '':
            options.postdata = self.flow.request.body
        options.headers = str(self.flow.request.headers)    
        if options:
            app.set_options(options)
            app.run()
            print app.heuris_test
            print app.taskid        
        app.land(True)

        

