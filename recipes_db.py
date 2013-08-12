#!/usr/bin/python
#-*- coding: utf-8 -*-
from db_format import DB_VERSION
from db_format import VERSION_TABLE_NAME
from db_format import VERSION_FORMAT
from db_format import VERSION_FETCH_QUERY
from db_format import RECIPE_TABLE_NAME
from db_format import RECIPE_FORMAT
from db_format import RECIPE_FETCH_QUERY
from db_format import INGRIDIENTS_TABLE_NAME
from db_format import INGRIDIENTS_FORMAT
from db_format import INGRIDIENTS_FETCH_QUERY
from db_format import LIST_SEPARATOR

from db import DB
from utils import writetoFilewithHTMLHeader
class RecipesDB (DB):
   def __init__(self, dbname, source):  
      DB.__init__(self, dbname)
      if not VERSION_TABLE_NAME in self._existingTables:
         self.createTable(VERSION_TABLE_NAME, VERSION_FORMAT)
         self.insert( VERSION_TABLE_NAME, DB_VERSION, True  )
      if not RECIPE_TABLE_NAME in self._existingTables:
         self.createTable(RECIPE_TABLE_NAME, RECIPE_FORMAT)
      if not INGRIDIENTS_TABLE_NAME in self._existingTables:
         self.createTable(INGRIDIENTS_TABLE_NAME, INGRIDIENTS_FORMAT)
      if self.getVersion() != DB_VERSION:
         print "Versions not matching"
      self._source = source
      self.ingridients = dict()
      f = self.fetch(INGRIDIENTS_FETCH_QUERY)
      for ingridient in f:
         key = ingridient[0]
         name = ingridient[1]
         self.ingridients[name] = key
      f = self.fetch( "select id from %s order by id DESC limit 1" % RECIPE_TABLE_NAME )
      self._greatesID = f[0][0] if len(f) else 0

   def getGreatestID(self):
      return self._greatesID

   def pushRecipe(self, id, caption, manual, ingridients, url, category):
      ingridients_ids = []
      amount_list = []
      for i in ingridients:
         recipe_id = self.getIngridientID(i[0])
         ingridients_ids.append(str(recipe_id))
         amount_list.append(i[1])
      #writetoFilewithHTMLHeader(manual, 'pov.html')
      manual = str(manual).decode('utf-8')
      self.insert(RECIPE_TABLE_NAME,
         '%d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\' ' % ( 
         id,
         DB.escape(caption), 
         DB.escape(manual),
         LIST_SEPARATOR.join(ingridients_ids), 
         LIST_SEPARATOR.join(amount_list), 
         url, 
         LIST_SEPARATOR.join(category), 
         self._source )
      )
      self._greatesID = id

   def getIngridientID(self, ingridient):
      if ingridient in self.ingridients:
         return self.ingridients[ingridient]
      q = 'NULL, \'%s\'' % ingridient
      self.insert(INGRIDIENTS_TABLE_NAME, 'NULL,\'%s\'' % ingridient)
      f = self.fetch("select id from %s where name=\'%s\'" % (INGRIDIENTS_TABLE_NAME, ingridient) )
      id =  f[0][0]
      self.ingridients[ingridient] = id
      return id

   def getVersion(self):
      if not VERSION_TABLE_NAME in self._existingTables:
         print "no version table"
         return None
      f = self.fetch(VERSION_FETCH_QUERY)
      if len(f) != 1:
         print len(f)
         return None
      return f[0][0]

if __name__ == '__main__':
   db = RecipesDB('example.db', 'example.com')
   db.pushRecipe(2, "'v \"ie", "narezat i razmewat", [("goroshok", "2 kg"), ("morkovka", "2 wtyki")], "htpp://google.com/", ["salati"] )
   db.commit()
   print LIST_SEPARATOR
