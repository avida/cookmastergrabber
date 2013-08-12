#!/usr/bin/python
DB_VERSION = 1

VERSION_TABLE_NAME = "version"
VERSION_FORMAT = "version integer"
VERSION_FETCH_QUERY = "select version from %s" % VERSION_TABLE_NAME

RECIPE_TABLE_NAME = "recipes"
RECIPE_FORMAT = "id integer primary key, caption text, manual text, ingridients text , amount text ,url text ,category text, source  text"
RECIPE_FETCH_QUERY = "select id, caption, manual, ingridients, amount, url, category, source from %s " % RECIPE_TABLE_NAME

INGRIDIENTS_TABLE_NAME = "ingridients"
INGRIDIENTS_FORMAT = "id integer primary key asc AUTOINCREMENT, name text"
INGRIDIENTS_FETCH_QUERY = "select id, name from %s" % INGRIDIENTS_TABLE_NAME

LIST_SEPARATOR = "|-|-|"