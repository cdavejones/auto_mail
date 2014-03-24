#!/usr/bin/env python
'''
auto_mail.py: Automatic mail grabber for GNU/Linux using poplib 
              Also launcher for simple message viewer gitmsg.py

__author__ = "C Jones"
__copyright__ = "2014"
__license__ = "GPL"
__version__ = ".05"


'''
import bz2 
import os
import sys
import socket
import subprocess
import time
from time import gmtime, strftime
import threading
from email import parser
import commands
import poplib
try:
 import pyttsx
 print "Succesfully imported pyttsx"
 print "Speech enabled!"
except:
 print "Unable to import pyttsx"
 print "Text to speech won't be enabled"











# SOME GLOBAL VARIBLES===================================================================

global shutDown
global wait_state # global integer containing seconds to wait before polling mail server
global wait_min
global wait_max

global pop_server
global main_path

wait_min = 30
wait_max = 5
wait_state = 0
shutDown = False

main_path = "/home/winston/main_mail/"
pop_server = "pop.gmail.com"
# ========================================================================================



# death_daemon()============================================
# monitor threads  
# and split into words then check input string for commands

def death_daemon():
 global shutDown
 while(1):
  if t1.isAlive() == False or t2.isAlive() == False:
   #print "ok"
   shutDown=True
   sys.exit()
#===========================================================




# play_tone()============================================
# use system call for to create tone 



def play_tone(tone,step,mod):

 t = 0 
 while(t != step):
 
  os.system('play --no-show-progress --null --channels 1 synth %s square %f' % ( .02, tone))
  tone=tone/mod
  t+=1
 return tone


# END=======================================================













# open_cred()============================================
# run bz2 decompress on file containing login data
# this isn't secure to be imporved in future


def open_cred(file_path):
 global shutDown
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

#===========================================================



# print_log()============================================
# write email activity to text log
# address of incoming message as well as time and date is written
# Note: future plans to implement this as tracker for unread messages

def print_log(strng):
 log_path=main_path+"mail_log"
 if os.path.isfile(log_path) == True:
  fp=open(log_path,'a')
  fp.write("?:"+strng) # '?:' is written first. this is to mark unread messages
                       # in the future after a messages has been viewed '?' will be removed and '!" will be added
  fp.close()

 else: 
  fp=open(log_path,'w')
  fp.write("")
  fp.close()
  print_log(strng)




# getIn()============================================
# get text input using "raw_input"
# and split into words then check input string for commands
def getIn():

 global shutDown
 global wait_state
 global wait_min
 global wait_max

 while(shutDown!=True):  # monitor for "kill signal" issued (either by command in getIn() or by death_daemon() in "kill" thread)
   
  com_in=raw_input("")# get input
  ok=com_in.split(" ")# break string up in indivdaul words by removing spaces
  num=0
  
  for i in ok:       # loop through ok's list of words
                     # check for commands
   if i == "wait_max": 
    if num < len(ok):
     try:
      wait_max = int(ok[num+1])
      print("wait_max set")
     except ValueError:
      print("MUST BE A NUMBER")

   if i == "wait_min":
    if num < len(ok):
     try:
      wait_min = int(ok[num+1])
      print("wait_min set")
     except ValueError:
      print("MUST BE A NUMBER")
   if i == "refresh":
    
    saveMail(getMail())
    print "refresh called"
   
   if i == "kill":
    shutDown = True
    
    print "shutting down"
   
    
   if i == "clear":
    os.system("clear")
   num+=1
 sys.exit() # exit function(ending thread "t1")

#END=================================================

# getName()============================================
# find name's of email adresses(and phone numbers) in a text file called addBook
# email address and names are stored in the format of "addresshere@domian.net:John Doe"
#'data' contains email address passed from function caller
#'data' is searched for in addBook and when found removed from left side of ":" character
# the right is returned as string
# 'None' is returned is nothing is found'
# if file give in add_book is not found none is return and message is printed
def getName(data):
 add_book=main_path+"addBook"
 try:
  with open(add_book,'r') as addBook:
   for s in addBook:
    if len(s)> 1:
     if data.find(s.split(":")[0]) == 0:
      return s.split(":")[1]
   return None
 except:
  print "no address book found"
  return None
#END===================================================

# speaK()============================================
# utlize's pyttsx text to speech module
# it creates  a pyttsx object and
# assigns relevent properties
# text string to vocalize is passed as 'sayString'
# 
def speaK(sayString):
  try:
   engine = pyttsx.init()
   rate = engine.getProperty('rate')
   engine.setProperty('rate', rate-50)
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
#END===================================================

# getMail()============================================
# Create poplib object and pass username and password to it
# check for messages
# return  messages if present otherwise return 'None'
# email address of each sender is passed to getName()
# if a result is returned this passed to speaK()


def getMail():

 print "Fetching mail"
 global wait_state
 global pop_server
 try:
  mailObj  = poplib.POP3_SSL(pop_server)
  mailObj.user(open_cred("eac"))
  mailObj.pass_(open_cred("kttk"))
  (numMsgs, totalSize) = mailObj.stat()
  if numMsgs > 0:
   speaK("You have "+str(numMsgs)+" new e mails")
   messages = [mailObj.retr(i) for i in range(1, len(mailObj.list()[1]) + 1)]
   messages = ["\n".join(mssg[1]) for mssg in messages]
   messages = [parser.Parser().parsestr(mssg) for mssg in messages]
   mailObj.quit()
   del mailObj
   return messages
  else:
   mailObj.quit()
   del mailObj
   print (strftime("%m-%d-%Y- %H:%M:%S", time.localtime())+":NO MAIL FOUND")
   return None
 except poplib.error_proto, detail:
  wait_state=180
  speaK("There has been an error checking mail")
  print str(detail)
# =====================END============================



# saveMail()============================================
# Extract email address of sender and message body from each message in messages
# write extracted message to file. File name is the same as the email address of sender
# before each message is written add string '************MESSAGE**************' as header

def saveMail(messages):
 save_path = main_path
 viewer_path = main_path
 if messages != None:
  for message in messages:
   mail_add = str(message['From'])[str(message['From']).find('<')+1:].strip('>') # email address contained in 'FROM' field is enclosed in '<>' these are removed
   out_dir=save_path+mail_add # path to plain text file containing email. name of file is simply email adress
                                               # Note: in future the directory path is going to be modifiable global setting         
   run_string=viewer_path+"./gitmsg.py -a "+mail_add # path to mail reader, 'gitmsg.py' with input(-a option) consisting of email adress of sender
   output=subprocess.check_output("ps aux|grep gitmsg.py", shell=True) # gitmsg.py is searched for using system call to ps
   if mail_add not in output:   
    try:                                                                # output is searched for an instance of gitmsg running with '-a mail_add' of current sender
     subprocess.Popen(run_string, shell=True)                           # if no such instance is found runing Popen creates one(passing run_string as command)
    except:
     print "gitmsg.py not found at path provided"
  
  
   
   print mail_add
   if os.path.isfile(out_dir) == False:
    fp=open(out_dir,'w')
    fp.write("")
    fp.close()
   outFile =open(out_dir,'a')
   who = getName(mail_add)
   if who != None:
    speaK("New message from " + who) # call wraper function for speech engine(called from pyttsx module)
    print (strftime("%m-%d-%Y- %H:%M:%S", time.localtime())+":New message from " + who) 
    
   st = str(message).find('\n\n')
   outFile.write('************MESSAGE**************\n')
   outFile.write(str(message['Date']))
   print_log(str(message['Date'])+":" + mail_add+"\n" )
   msg_read = str(message)[st:]
   if msg_read.find("SPK1") > -1 and msg_read.find("SPK0") > -1:
    speaK(msg_read[msg_read.find("SPK1")+4:msg_read.find("SPK0")].lower()) # speech
   outFile.write(str(message)[st:])
   outFile.write('\n')
   outFile.close()
  
  return messages
 else:
  return None
#=======================END============================



#================Entry Point===========================




# MAIN()============================================
# main loop of function the handles program actions outside of user input
# calls to check mail is made perodically, determined in seconds, by wait_min and wait_max
# wait_min sets check rate after a message is recieved. wait_max while "idle"
# connectivity is also checked before each call(see below)


def MAIN():
 global wait_min
 global wait_max
 global wait_state
 global shutDown


 while(shutDown == False):
  
  

  print "tick"
  print "tock"
   
  time.sleep(wait_state)
  
  wait_state=wait_max
 
  isCon = False             
  while(isCon == False):                          # loop checking each time for internet 
   try:                                           # this is done by attempting to access google
                                                  # and catching error returned is no connection is present
    host = socket.gethostbyname("www.google.com") # a successful check sets isCon to True and the loop stops
    s = socket.create_connection((host, 80), 2)   # would like a better way to do this
    isCon= True                                   
    
   except:
    print "connection error"
    isCon= False



  if saveMail(getMail()) != None:
   
   wait_state=wait_min
 sys.exit()  # kill thread after while is exited
# =====================END============================






# Entry Point=========================================
wait_state=wait_min
t1 = threading.Thread(target=getIn)
t2 = threading.Thread(target=MAIN)
kill = threading.Thread(target=death_daemon)
#time.sleep(5)
t1.start()
t2.start()
kill.start()
# ====================================================






