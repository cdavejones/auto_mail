#!/usr/bin/env python
import threading
import time
import bz2 
import sys
import smtplib
import os
import Tkinter
import argparse
from email.mime.text import MIMEText
from Tkinter import *

#===========================================================================
global sms_name
global MAIL_PATH
global screen_txt
global shutDown
screen_txt=""
shutDown=False
MAIL_PATH="/home/winston/main_mail/" # edit this to change directory mail is read from





com_line = argparse.ArgumentParser(description='mail reader/mail sender')
com_line.add_argument('-a', help='address', required=True)
args = vars(com_line.parse_args())


def play_tone(tone,step,mod):

 t = 0 
 while(t != step):
 
  os.system('play --no-show-progress --null --channels 1 synth %s saw %f' % ( .5, tone))
  tone=tone/mod
  t+=1
 return tone







class Window:
 
 def __init__(self,width,height,cap,**options):
  
  self.top = Tkinter.Tk()
 
  self.screen_txt=""
  self.width=width
  self.height=height
  self.cap=cap
  self.v = StringVar()
  self.top.configure(background = 'white')
  self.top.wm_attributes("-topmost", 1)
  self.top.minsize(self.width,self.height) #MIN SIZE
  self.top.maxsize(self.width,self.height) #MIN SIZE
  self.top.geometry(str(self.width)+"x"+str(self.height)) #DEFAULT SIZE
  self.top.title(self.cap)
  self.top.bind('<Return>',self.getInput)
  
  scrollbar = Scrollbar(self.top, orient=VERTICAL)
  self.w = Text(self.top, font=("Courier 10 pitch", 10),fg="black",yscrollcommand=scrollbar.set,relief="flat",width=70,height=19)
  scrollbar.config(command=self.w.yview)
  #scrollbar.pack(side=RIGHT, fill=Y)
  scrollbar.pack(side="right", fill="y", expand=False)
  self.w.place(x = 5, y = 5)
  self.e = Entry(self.top,width=96,relief="flat")
  self.e.place(x = 5, y = 473-23)
  
 def getInput(self,event):
  
  ok=self.e.get()
  
  
  self.e.delete(0, END)
  self.w.insert(END, "\n************YOU******************\n"+ ok+"\n.")
  self.w.yview(END)
  #self.w.see(Tkinter.END)
  send_mail(ok)
  time.sleep(1/10)
  
 
 def set_focus(self):
  self.top.wm_state('normal')
  self.top.attributes('-topmost', 1)

  self.top.focus_set()
  self.top.focus_force()
  self.top.lift()
  
 def set_txt(self,txt):
  
  self.w.insert(END, txt)
  self.w.yview(END)
 def add_entry(self,_width=20,_x=20,_y=110):
  e = Entry(self.top,width=_width)
  e.place(x = _x, y = _y)
 def on(self):
  self.top.mainloop()



def open_cred(file_name):
 global shutDown
 global  MAIL_PATH
 main_path= MAIL_PATH
 try:
  fp=open(main_path+file_name,'r')
  give_back=fp.read()
  fp.close()
 except:
  print "couldn't find login info closing"
  shutDown = True
  sys.exit()
  return "fail"
 return bz2.decompress(give_back)










def send_mail(msgz):
 global sms_name
 global sender_add
 to = sms_name
 email_user = open_cred("eac")
 email_pwd = open_cred("kttk")
 smtpserver = smtplib.SMTP("smtp.gmail.com",587)
 smtpserver.ehlo()
 smtpserver.starttls()
 smtpserver.ehlo
 smtpserver.login(email_user, email_pwd)
 header = 'To:' + to + '\n' + 'From: ' + email_user + '\n'
 msg = MIMEText(msgz).as_string()
 smtpserver.sendmail(email_user, to, msg)
 smtpserver.close()
 


def getAmsg(maxReturn=0):

 global shutDown
 global sms_name
 global MAIL_PATH
 global screen_txt
 last_i=0
 didRan =False
 global sms_name
 full_path=MAIL_PATH+sms_name
 if os.path.isfile(full_path) == False:
  fp=open(full_path,'w')
  fp.write("")
  fp.close()
 while(not shutDown):

  if didRan == False:
   maxReturn = 5
   didRan = True
  else:
   maxReturn = 0
  
  if shutDown==True:
   sys.exit()
  
  time.sleep(1)
  searchString="************MESSAGE**************"
  fp=open(full_path,'r')
  stIn=fp.read()
  fp.close()
  index = 0
  msgIndex={}
  i = 0
  while index < len(stIn):
   index=stIn.find(searchString,index)
   if index < 0:
    break
   else:
    i+=1
   #print index
   msgIndex[i]=index
   index+=len(searchString)
 
  if maxReturn <= i and maxReturn != 0:
   maxReturn=i-(maxReturn-1)
  elif maxReturn > i:
   maxReturn=1
  elif maxReturn == 0:
   maxReturn=i
  if last_i != i:
   
  
   
   screen_txt=stIn[msgIndex[maxReturn]:].replace("MESSAGE",sms_name)
   win.set_txt(screen_txt)
   win.set_focus()
  last_i = i


   
 




#ENTRY POINT======================================
sms_name=args['a']
t1 = threading.Thread(target=getAmsg)

win=Window(800,473,sms_name)
t1.start()
win.on()
shutDown=True


#=================================================







