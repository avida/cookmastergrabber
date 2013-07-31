#!/usr/bin/python
class IGrabber(object):
   def getIngridients(self):
      raise NotImplementedError( "Not implemented" )
   def getManual(self):
      raise NotImplementedError( "Not implemented" )
   def getCaption(self):
      raise NotImplementedError( "Not implemented" )
   def getRange(self):
      raise NotImplementedError( "Not implemented" )
   def doParse(self, id):
      raise NotImplementedError( "Not implemented" )
   def getUrl(self):
      raise NotImplementedError( "Not implemented" )
   def getCategory(self):
      raise NotImplementedError( "Not implemented" )