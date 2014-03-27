#!/usr/bin/env python
import poplib
import time
import os
import threading
import sys
from time import gmtime, strftime
from email import parser
class autoMail:

 def __init__(self,server,user,password,save_dir):
  
  self.pop_server = server
  self.password = password
  self.user = user
  self.shutDown = False
  self.save_dir = save_dir
  self.wait_min = 30
  self.wait_max = 120
  self.wait_state = 0
  self.numMsgs = 0
  self.who = []
  self.finish = True
  self.outMessage = ""
 def MAIN(self):
  self.wait_min 
  self.wait_max
  self.wait_state
  self.shutDown
  while(self.shutDown == False):
   self.outMessage = "tick"
   self.outMessage = "tock"
   
   time.sleep(self.wait_state)
   self.wait_state=self.wait_max
   ping = 1
   while(ping != 0):                          
    ping = os.system("ping -c 1 " + self.pop_server)                                           
                              
   self.finish = False                            
   if self.saveMail(self.getMail()) != None:
    self.wait_state=self.wait_min
   self.finish = True
  sys.exit()  # kill thread after while is exited
 
 

 def getMail(self):

  self.outMessage = "Fetching mail"
 
  try:
   mailObj  = poplib.POP3_SSL(self.pop_server)
   mailObj.user(self.user)
   mailObj.pass_(self.password)
   (numMsgs, totalSize) = mailObj.stat()
   if numMsgs > 0:
    self.outMessage = ("You have "+str(numMsgs)+" new e mails")
    self.numMsgs+= numMsgs
    messages = [mailObj.retr(i) for i in range(1, len(mailObj.list()[1]) + 1)]
    messages = ["\n".join(mssg[1]) for mssg in messages]
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]
    mailObj.quit()
    del mailObj
    return messages
   else:
    mailObj.quit()
    del mailObj
    self.outMessage = (strftime("%m-%d-%Y- %H:%M:%S", time.localtime())+":NO MAIL FOUND")
    return None
  except poplib.error_proto, detail:
   self.wait_state=180
   self.outMessage = str(detail)



 def saveMail(self,messages):
 
  if messages != None:
   for message in messages:
    
    mail_add = str(message['From'])[str(message['From']).find('<')+1:].strip('>')
    
    out_dir=self.save_dir+mail_add
    if os.path.isfile(out_dir) == False:
     fp=open(out_dir,'w')
     fp.write("")
     fp.close()
    outFile =open(out_dir,'a')
    self.outMessage = (strftime("%m-%d-%Y- %H:%M:%S", time.localtime())+":New message from " + mail_add) 
    self.who.append(mail_add)
    st = str(message).find('\n\n')
    outFile.write('************MESSAGE**************\n')
    outFile.write((str(message)))
    outFile.write('\n')
    outFile.close()

   return messages
  else:
   return None















 def setWaitMax(self,wait_max):
  self.wait_max = wait_max
 def setWaitMin(self,wait_min):
  self.wait_min = wait_min
 def reFresh(self):
  if self.saveMail(self.getMail()) != None:
    self.wait_state=self.wait_min


 def startMail(self):
  t1 = threading.Thread(target=self.MAIN)
  t1.start()


 def killMail(self):
  self.shutDown = True
  sys.exit()

 def newMsgs(self):
  n = 0
  if self.finish == True:
   n = self.numMsgs
   self.numMsgs = 0
   
  return n
  
 

 def whoMail(self):
  m =[]
  
  if self.finish == True:
   m = self.who
   self.who = []
  return m


 def getStatus(self):
  
  return self.outMessage



 def sendCommand(self,txt):


 # 	will contain code to carry out commands-
 # sent to modlue(kill,refresh,etc etc)



  return "pop"

  
