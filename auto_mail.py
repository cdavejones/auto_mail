#!/usr/bin/env python
import autoMail
import os
import sys
import time
import bz2 
try:
 import pyttsx
 print "Succesfully imported pyttsx"
 print "Speech enabled!"
except:
 print "Unable to import pyttsx"
 print "Text to speech won't be enabled"



global main_path 
global pop_server
main_path = "/home/winston/"
pop_server = "pop.gmail.com"


def speaK(sayString):
  try:
   engine = pyttsx.init()
   rate = engine.getProperty('rate')
   engine.setProperty('rate', rate-60)
   volume = engine.getProperty('volume')
   engine.setProperty('volume', volume+15)
   voices = engine.getProperty('voices')
   engine.setProperty('voice', 'en-scottish')
   engine.say(sayString)
   engine.runAndWait()
  except:
   
   print "Error running text to speech"
   print "Using tone alert instead"
   play_tone(play_tone(2000,2,.05)**2/9,1,2)





def open_cred(file_path):
 
 global main_path
 try:
  fp=open(main_path+file_path,'r')
  give_back=fp.read()
  fp.close()
 except:
  print "couldn't find login info at "+ main_path + " closing"
  
  shutDown = True
  sys.exit()
  return "fail"
 return bz2.decompress(give_back)



def getName(data):
 add_book=main_path+"addBook"
 try:
  with open(add_book,'r') as addBook:
   for s in addBook:
    if len(s)> 1:
     if data.find(s.split(":")[0]) == 0:
      return s.split(":")[1]
   return data
 except:
  print "no address book found"
  return data










def play_tone(tone,step,mod):

 t = 0 
 while(t != step):
 
  os.system('play --no-show-progress --null --channels 1 synth %s square %f' % ( .02, tone))
  tone=tone/mod
  t+=1
 return tone






get_it=autoMail.autoMail(pop_server,open_cred("eac"),open_cred("kttk"),main_path)
get_it.setWaitMax(10)
get_it.setWaitMin(10)

get_it.startMail()

while 1:
 sender_list={}
 newMsg = get_it.newMsgs()
 if newMsg > 0:
  
  for i in get_it.whoMail():
   if i in sender_list:
    sender_list[i]+=1
   else:
    sender_list[i] = 1
  speaK("you have" + str(newMsg) + "new" + ("emails" if newMsg > 1 else "email"))
  for i in sender_list:
   speaK(str(sender_list[i]) + "new " + ("messages" if sender_list[i] > 1 else "message" )+ " from" +getName(str(i)))


 time.sleep(5)
 print get_it.getStatus()











