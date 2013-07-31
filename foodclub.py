#!/usr/bin/python
import urllib2
import re 
from bs4 import BeautifulSoup
from utils import printToConsole
from grabber import IGrabber
url_format = "http://www.foodclub.ru/detail/%s/"
url = "http://www.foodclub.ru/all/"

   
def getFoodclubReceipes():
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
def parseFoodClub(url):
   page = urllib2.urlopen(url) 
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
   file.close
   caption = soup.find(attrs={"class":"fn"}).getText()
   printToConsole(caption)
   ingridients = soup.find(attrs={"class":"needed"})
   ingridients = ingridients.find("table")
   ingridients = ingridients.find_all("td")
   for i in range(0, len(ingridients),2 ):
      name = ingridients[i].find(attrs={"class":"ingredient"})
      if not name is None:
         name = name.getText()
         amount = ingridients[i+1].getText()
         printToConsole(name + ": "+ amount)
recepies = getFoodclubReceipes()
import random
ID = random.choice(recepies)
print ID
parseFoodClub(url_format % ID)
