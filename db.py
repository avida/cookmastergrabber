#!/usr/bin/python
#-*- coding: utf-8 -*-
import sqlite3
import re
from utils import printToConsole

WRITE_QUEUE_LIMIT = 150
class DB:
   _db = None
   _c =  None
   _queries_pending_commit = 0
   _existingTables = None
   def __init__(self, dbname):
      self._db = sqlite3.connect(dbname)
      self._c = self._db.cursor()
      self._updateTables()
   def _updateTables(self):
      self._existingTables = self.fetch("select name from  %s where type='table'" %  "sqlite_master")
      self._existingTables = map( lambda x: x[0], self._existingTables )
   def createTable(self, name, values):
      if name in self._existingTables:
         return
      query = "create table %s (%s)" % (name, values)
      self._c.execute(query)
      self.commit()
      self._updateTables()
   def insert(self, name, values, commitNow = False ):
      query = 'insert into %s values (%s)' % (name, values)
      try:
         self._c.execute(query)
         self._queries_pending_commit += 1
      except sqlite3.IntegrityError as e:
         print "insert SQL Error: " + str(e)
      except sqlite3.OperationalError as e:
         print "error"
         printToConsole( e.message.decode('utf-8') )
      if commitNow:
         self.commit()
      self._processQueue()
      
   def _processQueue(self):
      if self._queries_pending_commit > WRITE_QUEUE_LIMIT:
            self._db.commit()
   
   def execute(self, query):
      self._c.execute(query)
      self._db.commit()

   def fetch(self, query):
      self._processQueue()
      self._c.execute(query)
      return self._c.fetchall()

   def commit(self):
      self._db.commit()
      self._queries_pending_commit = 0

   @staticmethod
   def escape(s):
      return s.replace("'", "''")

if __name__ == '__main__':
   db = DB('example.sqlite')
   db.createTable('ingridients', "id integer primary key asc AUTOINCREMENT, name text unique")
   db.createTable('sites', 'id integer, url text')
   #db.execute('create table ingridients (id integer primary key asc AUTOINCREMENT, name text unique)')

   value = 'υσφι'
   db.insert('ingridients', 'NULL, \'%s\'' % (value))
   #print db.fetch('select id, name from ingridients')
   db.commit()