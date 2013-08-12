#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys

def printToConsole(unicode_str):
   print unicode_str.encode(sys.stdin.encoding,"replace")

def writetoFilewithHTMLHeader(body, filename):
      file = open(filename,"w")
      header = """
      <meta http-equiv="content-type" content="text/html; charset=UTF-8">
      """
      file.write(header)
      file.write(str(body))
      file.close()
       