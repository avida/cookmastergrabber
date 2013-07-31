#!/usr/bin/python

import sys
from foodclub import FoodclubGrabber
from povarenok import PovarenokGrabber
from utils import DB

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
 
if __name__ == '__main__':
   try:
      module = sys.argv[1]
      job_range = [ int(x) for x in  sys.argv[2].split('-') ]
      job_range.sort()
      if job_range[1] > 100 or  job_range[1] < 0 or  job_range[1] == job_range[0]:
         raise Exception()
   except Exception as e: 
      printHelp()
      exit()
   print job_range
   grb = None
   if module == 'povarenok':
      grb = PovarenokGrabber()
   elif module == 'foodclub':
      grb = FoodclubGrabber()
   if grb:
      range = grb.getRange()
      range = range[ job_range[0]* len(range)/100 : job_range[1]* len(range)/100 ]
      db_name = module + '_'+'-'.join([str(x) for x in job_range ])  + '.db'
      db = DB(db_name)
      
      print db_name
      print range
      
   else:
      printHelp()  