#!/usr/bin/env python
import poplib
import time
import os
import threading
import sys
from time import gmtime, strftime
from email import parser

class autoMail:

 def __init__(self,server,user,password,save_dir,mail_log="mail_log.log"):
  self.mail_log = mail_log
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
  self.verbose = False
 def MAIN(self):
  self.wait_min 
  self.wait_max
  self.wait_state
  self.shutDown
  while(self.shutDown == False):
   self.print_screen("tick")
   self.print_screen("tock")
   
   time.sleep(self.wait_state)
   self.wait_state=self.wait_max
   ping = 1
   while(ping != 0):                          
    ping = os.system("ping -c 1 " + self.pop_server+ "> /dev/null")                                           
                     
   self.finish = False                            
   if self.saveMail(self.getMail()) != None:
    self.wait_state=self.wait_min
   self.finish = True
  print "good bye"
  sys.exit()  # kill thread after while is exited
 
 

 def getMail(self):

  self.print_screen("Fetching mail")
 
  try:
   mailObj  = poplib.POP3_SSL(self.pop_server)
   mailObj.user(self.user)
   mailObj.pass_(self.password)
   (numMsgs, totalSize) = mailObj.stat()
   
   if numMsgs > 0:
    self.print_screen("You have "+str(numMsgs)+" new e mails")
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
    self.print_screen(strftime("%m-%d-%Y- %H:%M:%S", time.localtime())+":NO MAIL FOUND")
    return None
  except poplib.error_proto, detail:
   self.wait_state=180
   self.print_screen(str(detail))



 def saveMail(self,messages):
 
  if messages != None:
   for message in messages:
    
    mail_add = str(message['From'])[str(message['From']).find('<')+1:].strip('>')
    
    out_dir=self.save_dir+mail_add+".mail"
    if os.path.isfile(out_dir) == False:
     fp=open(out_dir,'a')
     fp.write("#$auto_mail@MAIL FILE$\n")
     fp.close()
    outFile =open(out_dir,'a')
    self.print_screen(strftime("%m-%d-%Y- %H:%M:%S", time.localtime())+":New message from " + mail_add) 
    self.who.append(mail_add)
    self.print_log("Date: "+str(message['Date'])+"|Local: "+strftime("%m-%d-%Y- %H:%M:%S", time.localtime())+"|From: "+mail_add+"|Message-ID: "+str(message['Message-Id'])+"|Subject: "+str(message['Subject'])+"|\n")
   
    st = str(message).find('\n\n')
    outFile.write('************MESSAGE**************\n')
    outFile.write((str(message)))
    outFile.write('\n')
    outFile.write('************!!!!!!!**************\n')
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


 def delete_inbox(self,num):
 


  for i in range(0,num-1):
   mailObj.dele(i)

 def print_screen(self,txt):
  self.verbose = False
  if self.verbose == True:
   print txt
 
 
 def set_verbose(boo):
  self.verbose = boo
  







 def print_log(self,strng):
  log_path=self.save_dir+self.mail_log
  fp=open(log_path,'a')
  fp.write(strng) 
  fp.close()



















class mail_table:
 def __init__(self,directory,mail_log="mail_log.log"):
  self.directory = directory

  self.mail_log = mail_log
  if os.path.isfile(self.directory+self.mail_log) == False:
   fp = open(self.directory+self.mail_log,"w")
   fp.write("")
   fp.close()
  if os.path.isfile(self.directory+"addBook") == False:
   with open(self.directory+"addBook","w") as fp:
    fp.write("")
  fp = open(self.directory+self.mail_log,"r")
  self.log_file = fp.readlines()
  fp.close()
  self.menu_dictionary = {}
  self.how_many = len(self.log_file)
 def reload_data(self):
  
  fp = open(self.directory+self.mail_log,"r")
  self.log_file = fp.readlines()
  fp.close()
  self.menu_dictionary = {}
  self.how_many = len(self.log_file)
 def getAdd(self,index):
  try:
   return self.menu_dictionary[index].split("|")[2][len("From: "):]
  except:
   return str(index)
 def list_directory(self):
  
  old_log = self.log_file
  menu_print = ""
  self.reload_data()

  old_menu = menu_print
  
  lines = self.log_file
  for i in range(0,len(lines)):
   self.menu_dictionary[i] = lines[i]
   item = lines[i].split("|")
   num_string = str(i)+"    "
  
   if lines[i] not in old_log:
     menu_print+="\x1b[32m"
   menu_print+=" ".join([num_string[0:len(num_string)-len(str(i))],item[0],item[2],item[4]])
   menu_print+="\x1b[37m"
   menu_print+="\n"

  return menu_print

 def del_person(self,person):
  found = "no messages from " + person+" found!"
  for i in range(0,len(self.menu_dictionary)):
   if person in self.menu_dictionary[i].split("|")[2][len("From: "):]:
    self.del_num(i)
    print i
    found = "all messages from " + person+" deleted."
  return found
  

 def del_num(self,index):
  try:
   sender = self.menu_dictionary[index].split("|")[2][len("From: "):]
   msg_id = self.menu_dictionary[index].split("|")[3]
  
   self.del_mail(sender,msg_id)
   return "Deleted message " + str(index)
  except:
   return "Option out of range!(message does not exist)"
         



    
      
 def del_mail(self,sender,msg_id):
  msg_id=msg_id.upper()
  path=self.directory+sender+".mail"
  fp=open(path,"r")
  t = fp.read()
  fp.close()
  exitLoop = False
  itemized=t.split("************MESSAGE**************")
  for i in range(0,len(itemized)):
   if msg_id in itemized[i].upper():
    del itemized[i]
    break


  t="************MESSAGE**************".join(itemized)
  fp=open(path,"w")
  fp.write(t)
  fp.close()
  for i in range(0,len(self.log_file)):
   if self.log_file[i].upper().find(msg_id) > -1:
    del self.log_file[i]
    break
  fp=open(self.directory+self.mail_log,"w")

  fp.write("".join(self.log_file))
  fp.close()
  self.reload_data
  self.list_directory


 def getName(self,data):
  main_path = self.directory
  add_book=main_path+"addBook"
  try:
   with open(add_book,'r') as addBook:
    for s in addBook:
     if len(s)> 1:
      if data.find(s.split(":")[0]) == 0:
       return s.split(":")[1]
    return data
  except:
   fp  = open(add_book, "w")
   fp.write("")
   fp.close()
   return data



 def num_Ofmail(self):
  return self.how_many









  
