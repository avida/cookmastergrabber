#!/usr/bin/python

import sys
import time
from threading import Thread
from foodclub import FoodclubGrabber
from povarenok import PovarenokGrabber
from recipes_db import RecipesDB

def printHelp():
   print '''specify module name and range from 0 upto 100, for example:
grabber.py povarenok 0-20   
   '''

ingridients_table = {
   'name' : 'ingridients',
   'value' : ''
 }
receipe_table = {
   'name': 'recipe',
   'value': 'df'
 }
done = False 
def grabSite(grb, module, j_range):
      range = grb.getRange()
      print "thread %s started with range %s" % (module, str(j_range))
      range = range[ j_range[0]* len(range)/100 : j_range[1]* len(range)/100 ]
      recipes_left = len(range)
      db_name = module + '_'+'-'.join([str(x) for x in j_range ])  + '.sqlite'
      db = RecipesDB(db_name, module)
      #range = [782]
      for id in range:
         if done:
            break
         if id <= db.getGreatestID():
            recipes_left-=1
            continue
         print "parsing %d from %s, %d left" % (id, module, recipes_left)
         recipes_left-=1
         if grb.doParse(id):
            db.pushRecipe(id, grb.getCaption(), grb.getManual(), grb.getIngridients(), grb.getUrl(), grb.getCategory())
         time.sleep(5)
         
         
      db.commit()
      print "thread %s exited" % module

jobs = []
sys.argv = sys.argv[1:]
try:
   while len(sys.argv) != 0:
      module = sys.argv[0]
      job_range = [ int(x) for x in  sys.argv[1].split('-') ]
      job_range.sort()
      if job_range[1] > 100 or  job_range[1] < 0 or  job_range[1] == job_range[0]:
         raise Exception()
      jobs.append((module, job_range))
      sys.argv = sys.argv[2:]
except Exception as e: 
   printHelp()
   exit()
threads = []
for job in jobs:
   module = job[0]
   job_range = job[1]
   grb = None
   if module == 'povarenok':
      grb = PovarenokGrabber()
   elif module == 'foodclub':
      grb = FoodclubGrabber()
   if grb:
      threads.append(Thread(target=grabSite,args=(grb, module, job_range)))
   else:
      print "wrong module %s" % module
try:
   for t in threads:
      t.start()
   while(True):
      time.sleep(10)
      threads_done = True
      for t in threads:
         if t.isAlive():
            threads_done = False
            break
      if threads_done:   
         break
except KeyboardInterrupt:
   import signal
   signal.signal(signal.SIGINT,signal.SIG_IGN)
   print "\nstopping"
   done = True;
   for t in threads:
      t.join()