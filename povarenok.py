#!/usr/bin/python
import urllib2
from bs4 import BeautifulSoup
from utils import printToConsole
url_format = "http://www.povarenok.ru/recipes/show/%s/"
url = url_format % 7258

try:
   page = urllib2.urlopen(url)
   soup = BeautifulSoup(page.read(), from_encoding="cp1251")
   if soup is None:
      print "error parsing html"
      exit 
   body = soup.find(id="print_body")
   if body is None:
      print "Page Not Foud"
      exit
   caption = body.find("h1").getText()
   
   recipe = body.find(attrs={'class':'recipe-steps'})
   if not recipe:
      recipe = body.find(attrs={'class':'recipe-text'})
   ingridients = body.find(attrs={"class":"recipe-ing"})
   printToConsole(caption)
   if len(ingridients) == 0:
      ingridients = recipe.find_all("li")
      for ingridient in ingridients:
         print ingridient.getText()
   else:
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
         print name + ": "+ amount 
   manual = recipe
   file = open("manual.html","w")
   header = """
   <meta http-equiv="content-type" content="text/html; charset=UTF-8">
   """
   file.write(header)
   file.write(str(manual))
   file.close()
except urllib2.HTTPError as e:
   print str(e)
   

	