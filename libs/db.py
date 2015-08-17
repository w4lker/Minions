#!/usr/bin/python27
#coding:utf-8

import sqlite3
import string

class db:
    conn = None
    def connectdb(self,path):
        self.conn = sqlite3.connect(path)
        if conn is not None:
            return conn.cursor()
        else:
            print "something wrong with database"
            
    def closedb(cur):
        try:
            if cur is None:
                cur.close()
        finally:
            cur.close()
          
          
    def query(self,cur,sql):
        if sql is not None and sql != '':
            cur.execute(sql)
            data = self.cur.fetchall()
            print data
            self.closedb(cur)
        else:
            print "sqlCommand can not be null!"

    #create,drop,insert,upate,delete统一为数据库的修改    
    def  modify(self,cur,sql):                                 
        if sql is not None and sql != '':
            cur.execute(sql)
            conn.commit()
            self.closedb(cur)
        else:
            print "sqlCommand can not be null!"        
            
            
    def injectPrevention(param):
        return (param.replace("'",'')).replace('=','')
    