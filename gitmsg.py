#!/usr/bin/python
import sys
import base64
import argparse
import smtplib
from gi.repository import Gtk, GLib,Gdk,Pango
import threading 
import time
from multiprocessing import Process
import bz2 
from email.mime.text import MIMEText
from email.header import Header
from random import randint
import os
global homer_simpson
homer_simpson = """  
      _____         
     /     \       
     \/\/     |      
    |  (o)(o)       
    C   .---_)    
      | |.___|    
      |  \__/     
     /_____\       
    /_____/ \       
   /         \     

  HOMER         


"""
try:
 import pyttsx
 print "Succesfully imported pyttsx"
 print "Speech enabled!"

except:
 print "Unable to import pyttsx"
 print "Text to speech won't be enabled"



global win




global MAIN_PATH







com_line = argparse.ArgumentParser(description='mail reader/mail sender')
com_line.add_argument('-a', help='address', required=True)
com_line.add_argument('-u', help='username', required=True)
com_line.add_argument('-p', help='password', required=True)
com_line.add_argument('-m', help='mail path', required=True)
inz = vars(com_line.parse_args())


class config_man:
 def __init__(self,filez,intcom=""):
  self.file = filez
  self.intcom = intcom
  self.tokens = {}
  
  if os.path.isfile(self.file) == False:
   fp = open(self.file,'w')
   fp.write(intcom+" \n")
   fp.close()
  

 def get_after(self,string,first,symbol):
  try:
   string+=" "
   start = string.index(first) + len(first)
   second = string.index(symbol,start)
   if second - start <= 1:
    second+= (1 if string[second + len(symbol)] == " " else 0)
    return string[second + len(symbol):string.index(" ",second+len(symbol))]
   else:
    return ""
  except ValueError:
   return ""

 def get_token(self,token):
  self.load_token(token)
  try:
   return self.tokens[token]
  except:
   return ""

 def load_token(self,token):
  fp = open(self.file,'r')
  file_string = fp.read().replace('\n'," ")
  fp.close()
  file_contents=filter(lambda s: s != "",file_string.split())
  self.tokens[token] = self.get_after(file_string,token,"=")
 
 
 def save_token(self,token,value):
  self.load_token(token)
  value+=" \n"
  
  with open(self.file,'r') as fp:
   txt = fp.read()
  if txt.find(token) < 0:
   with open(self.file,'a') as fp:
    fp.write(token+" = " + value)
  else:
    half1 = txt[:txt.index(token)]
    half2 = txt[txt.index(self.tokens[token],txt.index(token)) +len(self.tokens[token]):]   
    
    with open(self.file,'w') as fp:
     fp.write(half1+ token + " = "+ value + half2)
                 
    self.tokens[token] = value


 def delete_token(self,token):
  try:
   self.load_token(token)
   with open(self.file,'r') as fp:
    txt = fp.read()
   if txt.find(token) > 0:
    half1 = txt[:txt.index(token)]
    half2 = txt[txt.index(self.tokens[token]) +len(self.tokens[token]):]   
    with open(self.file,'w') as fp:
     fp.write(half1 + half2)
    
    self.tokens.pop(token, None)
  except:
   return ""



class Window(Gtk.Window):
 def __init__(self,Title):
       
        Gtk.Window.__init__(self, title=Title)
        self.selected_txt =""
        self.screen=""
        self.shutDown = False
        self.scroll_win=Gtk.ScrolledWindow()
        self.set_resizable(False)
        self.scroll_win.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.text_view = Gtk.TextView()
        fontdesc = Pango.FontDescription("FreeMono 7")
        
        self.text_view.modify_font(fontdesc)
        
        self.text_view.set_wrap_mode(True)
        self.text_view.set_editable(False)
        self.text_view.set_cursor_visible(False)
        self.scroll_win.add(self.text_view)
        self.set_size_request(600, 250)
        self.set_default_size(600, 250)
        self.entry = Gtk.Entry()
        self.button = Gtk.Button(label="Send")
        
        self.hbox = Gtk.Box(spacing=10)
        self.hbox2 = Gtk.Box(spacing=10)
        self.mbox =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
   
        self.entry.connect("activate", self.on_button_clicked)
        self.textbuffer = self.text_view.get_buffer()
        self.button.connect("clicked", self.on_button_clicked)
      
        self.hbox.pack_start(self.button, False, False, 0)
        self.hbox.pack_start(self.entry, True, True, 0)
        self.hbox2.pack_start(self.scroll_win, True, True, 0)
        self.mbox.pack_start(self.hbox2, True, True, 0)
        self.mbox.pack_start(self.hbox, False, False, 0)
        self.add(self.mbox)
        
 def on_button_clicked(self, widget):
  
  #st=self.textbuffer.get_insert()
    
  #ed =self.textbuffer.get_selection_bound()
  #self.selected_txt = self.textbuffer.get_text(self.textbuffer.get_iter_at_mark(st),self.textbuffer.get_iter_at_mark(ed),False)
  temp = self.entry.get_text()
  self.entry.set_text("")
  if temp == "homer":
   send_it.send((homer_simpson))
   return
  send_it.send((temp))
  self.write_text("\nYou: "+(temp))
 

  
  self.text_view.scroll_mark_onscreen(self.textbuffer.get_insert())

 def write_text(self,text):
  txt_start, txt_end = self.textbuffer.get_bounds()
  self.textbuffer.set_text( self.textbuffer.get_text(txt_start,txt_end,True)+text)
  self.text_view.scroll_mark_onscreen(self.textbuffer.get_insert())
 def start_back(self):
  
  t1 = threading.Thread(target=background_thread)
  t1.start()




class sendMail:
 def __init__(self,sender,pwd,server,port):
  
  self.sms_name =""
  self.server = server
 
  self.sender_add = sender
  self.pwd = pwd
  self.port = port

 def send(self,msgz):
  sms_name=self.sms_name
  self.msg = msgz
  to = sms_name

 
  smtpserver = smtplib.SMTP(self.server,self.port)
  smtpserver.ehlo()
  smtpserver.starttls()
  smtpserver.ehlo
  smtpserver.login(self.sender_add, self.pwd)
 
  msg = MIMEText(self.msg)
  msg['Subject'] =""
  msg['From'] = self.sender_add
  msg['To'] = to
  msg['Subject'] = " "
  msg['Reply-to'] = self.sender_add
 

 
  smtpserver.sendmail(self.sender_add, to,  msg.as_string())
  smtpserver.close()



"""
def open_cred(MAIN_PATH,file_path):
 

 try:
  fp=open(MAIN_PATH+file_path,'r')
  give_back=fp.read()
  fp.close()
 except:
  print "couldn't find login info at "+ MAIN_PATH + " closing"
  
  win.shutDown = True
  sys.exit()
  return "fail"
 return bz2.decompress(give_back)

"""

def save_img(path,out_name,img):


 loc = open (path+out_name, "w")
 loc.write(base64.b64decode(img))
 loc.close()





def background_thread(path,mail):
  global win
  time.sleep(1)
  old_mail = []
  
  while (not win.shutDown):
  
   
   new_mail = split_mail(path,mail)
   time.sleep(1)

   if len(new_mail) > len(old_mail):
    to_screen = []
    for i in range(len(old_mail),len(old_mail)+(len(new_mail) - len(old_mail))):
     if new_mail[i] != "\n":
      Gdk.threads_enter()
      win.write_text("\n"+new_mail[i])
      #apply_com(new[i])
      win.set_keep_above(True)
      win.present()
    
      Gdk.threads_leave()
   
    
    old_mail = new_mail
    
  
   
   
def apply_com(pop):
 a = 0
   
    


def MIMEimgs(txt):
 global win
 boundary=""
 img_data=[]
 txt_no = txt.split("\n")
 txt=str(txt.upper()).split("\n")
 for i in range(0,len(txt)):
  if "Content-Type: image/".upper() in txt[i]:
   if "jpeg".upper() in txt[i]:
    img_ext = ".jpg"
   
  
  if 'boundary="'.upper() in txt[i]:
   fst = txt[i].find('="')+len('="')
   boundary = txt[i][fst:txt[i].find('"',fst)]
   print "\n"+boundary+"\n"
  

  if "Content-Transfer-Encoding: base64".upper() in txt[i]:
   for j in range(i+1,len(txt)):
    
    if txt[j] != "\n" and boundary.upper() not in txt[j] and "Content".upper() not in txt[j]:
     img_data.append(txt_no[j])
    else:
  
     save_img(MAIN_PATH,"pic"+str(randint(0,1000))+str(randint(0,100))+ img_ext,("\n".join(img_data)))
     
def isMIME(txt):
 if "MIME-Version: 1.0".upper() in txt[:txt.find("\n\n")].upper():
  return True
 else:
 
  return False

def MIMEtype(txt):
 if "Content-Type: multipart/mixed".upper() in txt[:txt.find("\n\n")].upper():
  return "(decode error can't render multipart yet)"
  #MIMEimgs(txt)
 elif "Content-Type: multipart/alternative".upper() in txt[:txt.find("\n\n")].upper():
  return "(decode error can't render multipart yet)"
 elif "Content-Type: text/plain".upper() in txt[:txt.find("\n\n")].upper():
  return txt[txt.find("\n\n")+2:]
 elif "Content-Type: text/html".upper() in txt[:txt.find("\n\n")].upper():
  return "(decode error html/whatever not there yet)"
 elif "Content-Type: image/".upper() in txt[:txt.find("\n\n")].upper():
  return "(decode error nope no pictures either....)"
 return "Can't decode unkown type"





def split_mail(MAIN_PATH,recpt):
 return_list = []
 global win
 mail_string = "#$auto_mail@MAIL FILE$\n"
 msg_path=MAIN_PATH+recpt+".mail"
 if os.path.isfile(msg_path) == False:
  fp = open(msg_path,"w")
  fp.write(mail_string)
  fp.close()
 mail_string = "#$auto_mail@MAIL FILE$\n"
 marker = "************MESSAGE**************"
 end_marker = "************!!!!!!!**************"
 fp = open(msg_path,"r")
 msg_file = fp.read()
 fp.close()

 
 msg_list= msg_file.split(marker) 
 del msg_list[0]
 
 for i in range(0,len(msg_list)):
 
  if isMIME(msg_list[i]):
   return_list.append(recpt+": "+MIMEtype(msg_list[i].replace(end_marker,"")).strip("\n"))
   
  else:
   return_list.append(((recpt+": "+ msg_list[i][msg_list[i].find("\n\n")+2:msg_list[i].find(end_marker)])).strip("\n").strip("\n"))

 return return_list


def kill_it_all(one,two):
 win.shutDown = True
 Gtk.main_quit(one,two)



def spawn(title):
 global win
 win = Window(title)
 win.connect("delete-event",kill_it_all)
 win.show_all()
 

 GLib.threads_init()
 Gdk.threads_init()
 Gtk.main()






#port = 587
#server = "smtp.gmail.com"
MAIN_PATH = inz['m']
config = config_man(MAIN_PATH+".gitmsg.config","#gitmsg.py settings")
port = config.get_token("smtp_port")
server = config.get_token("smtp_srv")

print "port: " + port
print "server: " + server
if port =="" or server == "":
 #os.system("clear")
 print """ No port or server information found. \n These can be set from auto_mail by issuing the command 'gm_config -set'"""
 sys.exit()
send_it = sendMail(inz['u'],inz['p'],server,int(port))

send_it.sms_name = inz['a']


t2 =  threading.Thread(target=spawn,args=(inz['a'],))

t2.start()

t1 = threading.Thread(target=background_thread,args=(MAIN_PATH,inz['a']))
t1.start()











