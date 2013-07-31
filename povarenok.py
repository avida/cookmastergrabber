#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup
from utils import printToConsole
from grabber_common import IGrabber
url_format = "http://www.povarenok.ru/recipes/show/%s/"

class PovarenokGrabber(IGrabber):
   def __ionit__(self):
      self._ingridients = None
      self._manual = None
      self._caption = None
      self._url = None
      self._category = []
   def getRange(self):
      return range(0,77000)
   def getIngridients(self):
      return self._ingridients
   def getManual(self):
      return self._manual
   def getCaption(self):
      return self._caption
   def getCategory(self):
      return self._category
   def getUrl(self):
      return self._url
      
   def doParse(self, id):
      self._url = url_format % id
      try:
         page = urllib2.urlopen(self._url)
         soup = BeautifulSoup(page.read(), from_encoding="cp1251")
         if soup is None:
            print "error parsing html"
            return 
         body = soup.find(id="print_body")
         if body is None:
            print "Page Not Foud"
            return
         self._caption = body.find("h1").getText()
         recipe = body.find(attrs={'class':'recipe-steps'})
         category = body.find(attrs={'class':'recipe-infoline'})
         self._category = []
         for i in category.find_all('nobr'):
            self._category.append(i.getText())
         if not recipe:
            recipe = body.find(attrs={'class':'recipe-text'})
         self._manual = recipe
         ingridients = body.find(attrs={"class":"recipe-ing"})
         self._ingridients = []
         ingridients = ingridients.find_all("li")
         for ingridient in ingridients:
            name = ingridient.find(itemprop="name")
            if name:
               name = name.getText()
            else:
               name = "Unknown"
            amount = ingridient.find(itemprop="amount")
            if amount:
               amount = amount.getText()
            else:
               amount = "Unknown"
            self._ingridients.append( (name, amount) )
         return True
      except urllib2.HTTPError as e :
         print str(e)
         return False
if __name__ == '__main__':
   grb = PovarenokGrabber()
   import random
   ID = random.choice( grb.getRange() )
   print ID
   if grb.doParse(ID):
      print  grb.getUrl()
      printToConsole( grb.getCaption() )
      for ing in grb.getIngridients():
         printToConsole( "%s: %s" % (ing[0], ing[1] ) )
      printToConsole ( "; ".join(grb.getCategory()))



	