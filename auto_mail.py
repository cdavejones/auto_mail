#!/usr/bin/env python
import autoMail
import os
import sys
import time
import subprocess
import bz2 
import list_mail
import threading
global shutDown
shutDown = False
print '\x1b[1m'
print '\x1b[37m'
print '\x1b[40m'
os.system("clear")
try:
 import pyttsx
 print "Succesfully imported pyttsx"
 print "Speech enabled!"
except:
 print "Unable to import pyttsx"
 print "Text to speech won't be enabled"



global main_path 
global pop_server
main_path = "/home/winston/main_mail/"
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


def getIn():
 global shutDown
  
 while(shutDown!=True):  # monitor for "kill signal" issued (either by command in getIn() or by death_daemon() in "kill" thread)
  
  com_in =  raw_input("$: ").split(" ")
 
  perro = lambda x: "Command '" + x + "' needs value"
  
  for i in range(0,len(com_in)):
   if "delete" == com_in[i] or "del" == com_in[i]:
    try:
     print (mail_table.del_num(int(com_in[i+1])))
    except:
     print perro(com_in[i])
   elif "reply" == com_in[i] or "r" == com_in[i]:
    try:
     subprocess.Popen(main_path+("./gitmsg.py -a " + mail_table.getAdd(int(com_in[i+1])))+".mail", shell=True)
    except:
     print "fail"

  os.system("clear")
  print longtxt  
  print mail_table.list_directory()   
     

def err():
 while 1:
  print "error"
longtxt="""+
                                                                     +<<-
          _    _ _______ ____         __  __          _____ _     *    .  *       .             *   
 *    /\  | |  | |__   __/ __ \       |  \/  |   /\   |_   _| |              \ /     \|/         *  
   . /  \ | |  | |  | | | |  | |  *   | \  / |  /  \    | | | |    *   .    -(+)-     *    .   .       .       * 
+   / /\ \| |  | |  | | | |  | |   +  | |\/| | / /\ \   | | | |   .     *    / \  
   / ____ \ |__| |  | | | |__| |      | |  | |/ ____ \ _| |_| |____             >    +    .  *        *
+ /_/    \_\____/   |_|  \____/   .   |_|  |_/_/    \_\_____|______|  .       *         .      

       .                .       .  *           *                     *    *  . +aut0_mail
 +                                                                           +<         portable*...
         *          .   
"""














mail_table=list_mail.listMail(main_path)
get_it=autoMail.autoMail(pop_server,open_cred("eac"),open_cred("kttk"),main_path)
get_it.setWaitMax(30)
get_it.setWaitMin(10)
get_it.startMail()


print longtxt
print mail_table.list_directory()
t1 = threading.Thread(target=getIn)
t1.start()
while 1:
 sender_list={}
 newMsg = get_it.newMsgs()
 if newMsg > 0:
  
  for i in get_it.whoMail():
   sender_list[i]=((sender_list[i]+1) if i in sender_list else 1)
  
  speaK("you have" + str(newMsg) + "new" + ("emails" if newMsg > 1 else "email"))
  for i in sender_list:
   speaK(str(sender_list[i]) + "new " + ("messages" if sender_list[i] > 1 else "message" )+ " from" +getName(str(i)))
   #if i not in subprocess.check_output("ps aux|grep gitmsg.py", shell=True): subprocess.Popen(main_path+("./gitmsg.py -a " + i), shell=True) 
  os.system("clear")
  print longtxt
  print mail_table.list_directory()
 time.sleep(5)
 











