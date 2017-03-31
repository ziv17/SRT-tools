'''
Created on Mar 26, 2017

@author: Ziv
'''
#  -*- coding: utf-8 -*-
import subprocess
import urllib.parse
import urllib.request


class Translator(object):
    '''
    classdocs
    '''
    origURL= 'https://translate.google.com/translate_a/single?client=t&sl=en&tl=iw&hl=iw&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=7&q=how%20to%20translate&tk=293149.141394'
    transURL = 'https://translate.google.com/translate_a/single'
    transParams = {'client':'t','sl':'en','tl':'iw','hl':'iw','dt':'at','dt':'bd','dt':'ex','dt':'ld','dt':'md','dt':'qca','dt':'rw','dt':'rm','dt':'ss','dt':'t','ie':'UTF-8','oe':'UTF-8','otf':'1','ssel':'0','tsel':'0','kc':'7','q':'how to translate','tk':'293149.141394'}
    trnJSFile = "d:/DATA/Ziv/Programming/trials/trans-api/trn.js"
    
    def __init__(self, fromLang, toLang, toTrans):
        '''
        Constructor
        '''
        self.transParams = Translator.transParams 
        self.transParams['sl']=fromLang
        self.transParams['tl']=toLang
        self.transParams['hl']=toLang
        self.transParams['q']=toTrans
    
    def GetTranslateGoogleAPI(self):
        url_parts = list(urllib.parse.urlparse(self.transURL))
        print(url_parts)
        query = dict(urllib.parse.parse_qsl(url_parts[4]))
        query.update(self.transParams)
        print(query)
        url_parts[4] = urllib.parse.urlencode(query)
        url = urllib.parse.urlunparse(url_parts)
        print(url)
        res = urllib.request.urlopen(Translate.origURL).read()  # @UndefinedVariable
        print(res)
  
    def TraslateNodeAPI(self, fl, tl, toTrans):
      res = subprocess.check_output(["node", Translator.trnJSFile, fl, tl, toTrans],shell=True)   # @UndefinedVariable
      print(res)
      print("{}->{}\n{}->{}".format(fl, tl, toTrans,res))
      return res.decode('UTF-8')
  
    def tst(self, fl, tl, toTrans):
      res = subprocess.check_output(["node", Translator.trnJSFile, fl, tl, toTrans],shell=True)   # @UndefinedVariable
  
if __name__ == '__main__':
  r=Translator('en', 'iw', "I am happy")
  print (r.TraslateNodeAPI('en', 'iw', "I am happy"))
  #r.tst('en', 'de', "I am happy")
  
#   url = "http://stackoverflow.com/search" #/* ?q=myquestion" */
#   params = {'q':'question','lang':'en','tag':'python'}
# 
#   url_parts = list(urllib.parse.urlparse(url))
#   print(url_parts)
#   query = dict(urllib.parse.parse_qsl(url_parts[4]))
#   query.update(params)
#   print(query)
#   url_parts[4] = urllib.parse.urlencode(query)
#   
#   print(urllib.parse.urlunparse(url_parts))