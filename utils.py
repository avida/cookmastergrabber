#!/usr/bin/python
#-*- coding: utf-8 -*-
import sqlite3

def printToConsole(unicode_str):
   print unicode_str.encode('866', errors="replace")
   
class DB:
   _db = None
   def __init__(self, dbname):
      
      self._db = sqlite3.connect(dbname)
   def execute(self, query):
      c = self._db.cursor()
      c.execute(query)
      self._db.commit()
   def fetch(self, query):
      c = self._db.cursor()
      c.execute(query)
      return c.fetchall()
if __name__ == '__main__':
   db = DB('example.db')
   #db.execute('create table sites (id integer, url text)')
   #db.execute('create table ingridients (id integer primary key asc AUTOINCREMENT, name text unique)')
   #db.execute('create table ingridients (id integer primary key asc AUTOINCREMENT, name text unique)')
   value = 'хуцй'
   try:
      db.execute('insert into ingridients values (NULL, \'%s\') ' % (value))
   except sqlite3.IntegrityError as a:
      print str(a)
   
   print db.fetch('select id, name from ingridients')
        