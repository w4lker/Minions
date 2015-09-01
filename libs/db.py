#!/usr/bin/python27
#coding:utf-8

import sqlite3
import string

class database:
    conn = None
    def connectdb(self,path):
        self.conn = sqlite3.connect(path)
        if self.conn is not None:
            return self.conn.cursor()
        else:
            print "something wrong with database!"
            
    def closedb(self,cur):              #query和modify会调用closedb()，无需再关闭
        if cur is not None:
            cur.close()
            self.conn.close()
            return True
          
          
    def query(self,cur,sql):
        if sql is not None and sql != '':
            cur.execute(sql)
            data = self.cur.fetchall()
            print data
            self.closedb(cur)
        else:
            print "sqlCommand can not be null!"
   
    def  modify(self,cur,sql):
        if sql is not None and sql != '':
            cur.execute(sql)
            self.conn.commit()
            self.closedb(cur)
        else:
            print "sqlCommand can not be null!"        
            
            
    def injectPrevention(param):
        return (param.replace("'",'')).replace('=','')
    