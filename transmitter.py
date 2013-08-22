#!/usr/bin/python
import urllib2
import urllib
import json
import sys
from recipes_db import RecipesDB
from utils import printToConsole
from threading import Thread
import time

done  = False

url = "http://www.dima.vn.ua/db"
db_name = "povarenok_1-10.sqlite"

def MainThread():
   global done
   db = RecipesDB(db_name)
   recipes =  db.getRecipeIDs()

   last_recipe = 0
   if len( sys.argv ) > 1:
      last_recipe = recipes.index( int (sys.argv[1]) )  +  1 
      recipes = recipes[last_recipe:]
   for i in recipes:
      ID = i
      print "sending %d" % ID
      recipe = db.getRecipe(ID)
      req = urllib2.Request(url, json.dumps(recipe))
      response = urllib2.urlopen(req)
      print "Done"
      if done:
         return
      #the_page = response.read()
      #print the_page.decode("utf-8")

t = Thread(target=MainThread)
try:
   t.start()
   while(t.isAlive()):
      time.sleep(3)
except KeyboardInterrupt:
   import signal
   signal.signal(signal.SIGINT,signal.SIG_IGN)
   print "\nstopping"
   done = True;
   t.join()

