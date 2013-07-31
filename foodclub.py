#!/usr/bin/python
import urllib2
import re 
from bs4 import BeautifulSoup
from utils import printToConsole
from grabber_common import IGrabber

url_format = "http://www.foodclub.ru/detail/%s/"
url = "http://www.foodclub.ru/all/"

class FoodclubGrabber(IGrabber):
   def __ionit__(self):
      self._ingridients = None
      self._manual = None
      self._caption = None
      self._url = None
      self._category = []
   def getRange(self):
      return self.getFoodclubReceipes()
   
   def doParse(self, id):
      receipe_url = url_format % id
      self._url = receipe_url
      page = urllib2.urlopen(receipe_url) 
      soup = BeautifulSoup(page.read())
      file  = open("gc.html", "w")
      manual = soup.find(attrs={"class":"title"})
      manual =  manual.find_next_sibling("div")
     
      header = """
      <meta http-equiv="content-type" content="text/html; charset=UTF-8">
      """
      file.write(header)
      
      images = manual.find_all(attrs={"class":"image"})
      base_url = 'http://www.foodclub.ru/'
      for image in images:
         img = image.find("img")
         img['src']= base_url+img['src']
         image.replace_with(img)

      file.write(str(manual))
      self._manual = manual
      file.close
      
      caption = soup.find(attrs={"class":"fn"}).getText()
      self._caption = caption
      self._category = []
      category = soup.find(attrs={"class":"tags"})
      for i in category.find_all(attrs={"class":"sub-category"}):
         self._category.append(i.getText())
      for i in category.find_all(attrs={"class":"category"}):
         self._category.append(i.getText())
            
      ingridients = soup.find(attrs={"class":"needed"})
      ingridients = ingridients.find("table")
      ingridients = ingridients.find_all("td")
      self._ingridients = []
      for i in range(0, len(ingridients),2 ):
         name = ingridients[i].find(attrs={"class":"ingredient"})
         if not name is None:
            name = name.getText()
            amount = ingridients[i+1].getText()
            self._ingridients.append( (name, amount) )
      return True
            
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

   def getFoodclubReceipes(self):
      page = urllib2.urlopen(url) 
      soup = BeautifulSoup(page.read())
      anchor_div = soup.find(id="fc_statistics")
      scr = anchor_div.find_next_sibling("script")
      script_body = scr.getText().strip().replace('var allRecipesResult =','').replace(';','')
      recepies =  eval(script_body)
      displayed_recepies_links = soup.find_all(attrs={'class':"item recipe_list_item"}) 
      displayed_recepies = []
      for item in displayed_recepies_links:
         link = item.find("a")['href']
         m= re.search("\d+",link)
         displayed_recepies.append(int(m.group(0)))
      recepies  = displayed_recepies + recepies
      return recepies
if __name__ == '__main__':
   grb = FoodclubGrabber()
   import random
   ID = random.choice( grb.getRange() )
   print ID
   if grb.doParse(ID):
      printToConsole( grb.getCaption() )
      for ing in grb.getIngridients():
         printToConsole( "%s: %s" % (ing[0], ing[1] ) )
      printToConsole ( "; ".join(grb.getCategory()))

