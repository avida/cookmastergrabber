#!/usr/bin/python
#-*- coding: utf-8 -*-
import sqlite3

def printToConsole(unicode_str):
   print unicode_str.encode('866', errors="replace")

def writetoFilewithHTMLHeader(body, filename):
      file = open(filename,"w")
      header = """
      <meta http-equiv="content-type" content="text/html; charset=UTF-8">
      """
      file.write(header)
      file.write(str(body))
      file.close()
WRITE_QUEUE_LIMIT = 5
class DB:
   _db = None
   _c =  None
   _queries_pending_commit = 0
   _existingTables = None
   def __init__(self, dbname):
      self._db = sqlite3.connect(dbname)
      self._c = self._db.cursor()
      self._updateTables()
      print self._existingTables
   def _updateTables(self):
      self._existingTables = self.fetch("select name from  %s where type='table'" %  "sqlite_master")
      self._existingTables = map( lambda x: x[0], self._existingTables )
   def createTable(self, name, values):
      if name in self._existingTables:
         return
      query = "create table %s (%s)"
      self._c.execute(query)
      self._db.commit()
      self._updateTables()
   def insert(self, name, values ):
      query = 'insert into %s values (%s)' % (name, values)
      try:
         self._c.execute(query)
         self._queries_pending_commit += 1
      except sqlite3.IntegrityError as a:
         print str(a)
      self._processQueue()
      
   def _processQueue(self):
      if self._queries_pending_commit > WRITE_QUEUE_LIMIT:
            self._db.commit()
            self._queries_pending_commit = 0
   
   def execute(self, query):
      self._c.execute(query)
      self._db.commit()

   def fetch(self, query):
      self._processQueue()
      self._c.execute(query)
      return self._c.fetchall()

   def commit(self):
      self._db.commit()

if __name__ == '__main__':
   db = DB('example.db')
   db.createTable('ingridients', "id integer primary key asc AUTOINCREMENT, name text unique")
   db.createTable('sites', 'id integer, url text')
   #db.execute('create table ingridients (id integer primary key asc AUTOINCREMENT, name text unique)')

   value = 'хуцй'
   db.insert('ingridients', 'NULL, \'%s\'' % (value))
   db.commit()
#print db.fetch('select id, name from ingridients')
        