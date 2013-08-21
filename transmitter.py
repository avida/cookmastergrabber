#!/usr/bin/python
import urllib2
import urllib
import json
from recipes_db import RecipesDB
from utils import printToConsole

url = "http://www.dima.vn.ua/db"
db_name = "povarenok_1-10.sqlite"

db = RecipesDB(db_name)
recipe = db.getRecipe(829)
#data = urllib.urlencode(recipe)
req = urllib2.Request(url, json.dumps(recipe))
response = urllib2.urlopen(req)
the_page = response.read()
print the_page.decode("utf-8")


