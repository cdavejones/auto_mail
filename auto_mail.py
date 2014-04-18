#!/usr/bin/env python
import autoMail
import os
import sys
import time
import subprocess
import bz2 
import threading

homer_simpson = """    _ _,---._ 
       ,-','       `-.___ 
      /-;'               `._ 
     /\/          ._   _,'o \ 
    ( /\       _,--'\,','"`. ) 
     |\      ,'o     \'    //\ 
     |      \        /   ,--'""`-. 
     :       \_    _/ ,-'         `-._ 
      \        `--'  /                ) 
       `.  \`._    ,'     ________,',' 
         .--`     ,'  ,--` __\___,;' 
          \`.,-- ,' ,`_)--'  /`.,' 
           \( ;  | | )      (`-/ 
             `--'| |)       |-/ 
               | | |        | | 
               | | |,.,-.   | |_ 
               | `./ /   )---`  ) 
              _|  /    ,',   ,-' 
     -hrr-   ,'|_(    /-<._,' |--, 
             |    `--'---.     \/ \ 
             |          / \    /\  \ 
           ,-^---._     |  \  /  \  \ 
        ,-'        \----'   \/    \--`. 
       /            \              \   \ 

"""


# 	To do list:  

# integrate command options(spk, email to serial output etc)
# develope mailback protocol (maybe integrated into command options)
# gitmsg development





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


config_menu_string =""" 
****************Setting/Configuation Menu*******************
                                                     . *                                       
                 1. Set/change user name.                             .               
                 2. Set/change pop server.       .           .         
                 3. Set/change main directory.                    *       .           
                 4. Set/change voice default.   *<
                 5. Set/change tone default.         .               .
                 6. Command codes.                         .*
                 7. Mail password.  +<

************************************************************
Select option. Type 'back' when finished.

"""







class app_state:

  def __init__(self):

   self.print_messages = True # True enables display of messages in diretory False hides messages
  
   self.speech_enabled = True # 'True' state enables text to speech for alerts
  
   self.tone_enabled = False  # 'True' state enables tone alerts 
  
   self.shutDown = False     # 'while' condtionals check while running. 'True' state ends all threads autoMail 
                             # requires seperate call to killMail() in each instance of autoMail
   self.main_path =""
   self.pop_server = ""
   self.user_name = ""
   self.user_pass = ""
  def get_speech_state(self):
   return self.speech_enabled

  def get_tone_state(self):
   return self.tone_enabled
  
  def get_down_state(self):
   return self.shutDown

  def get_main_path(self):
   return self.main_path
   
  def get_pop_server(self):
   return self.pop_server
  def get_user_pass(self):
   return self.user_pass
  
  def get_user_name(self):
   return self.user_name

  def set_speech_state(self,boo):
   self.speech_enabled = boo

  def set_tone_state(self,boo):
   self.tone_enabled = boo
  
  def set_down_state(self,boo):
   self.shutDown = boo

  def set_screen_state(self,boo):
   self.print_messages = boo

  def set_main_path(self,path):
   self.main_path =  os.path.normpath(path) + os.sep

  def set_pop_server(self,pop):
    self.pop_server= pop
 
  def set_user_pass(self,passw):
    self.user_pass = passw
 
  def set_user_name(self,name):
   self.user_name = name



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
  value+="\n"
  
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
























class command_list:

 def __init__(self,name=''):
  self.name = name
  self.func_dict = {}
  self.num_dict = {}
  self.opt_dict = {}
  self.command_list = []
 def get_command_list(self):
  return self.command_list

 def add_command(self,func,num,string,option = 0):
   self.num_dict[string] = num
   self.func_dict[string] = func
   self.opt_dict[string] = option
   self.command_list.append(string)
 def get_command_num(self,string):
  return self.num_dict[string]
 def get_command_opt(self,string):
  return self.opt_dict[string]

 def get_func_command(self,string):
  return self.func_dict[string]




 def parse_string(self,string):
  input_list=filter(lambda s: s != "",string.split())
  out_list=[]

  x = 0
  while x <= len(input_list)-1:
  
   if input_list[x] in self.get_command_list():
    opt= (self.get_command_opt(input_list[x]) if (len(input_list) - x ) - 1 >= self.get_command_num(input_list[x])+self.get_command_opt(input_list[x]) else 0) # This will be refactored later ;_;
    if (len(input_list) - x ) - 1 >= self.get_command_num(input_list[x]):
     to_func=[]
     for num in range(x+1,x+self.get_command_num(input_list[x])+1+opt):
     
      to_func.append(input_list[num])
     out_list.append(self.get_func_command(input_list[x])(to_func))
  
     x+= self.get_command_num(input_list[x])+1+opt
  
    else:
   
     out_list.append(input_list[x] + " expects " + str(self.get_command_num(input_list[x])) + " inputs ")
     x+= 1
   else:
    out_list.append(self.name +' unknown command "' +input_list[x]+'"!')
    x+= 1
  return out_list


 





# Primary command functions===================================



def reply(pop):
 try:
  person = mail_table.getAdd(int(pop[0]))
  if person != pop[0]:
 
   send_mail(person)
   return ""
  else:
   return "mail number does not exist!"
 except:
  with open(state.get_main_path()+"addBook","r") as fp:
   contacts = fp.readlines()
  for i in contacts:
   if pop[0].upper() in i[i.index(":")+1:-1].upper(): 
    send_mail( i[:i.index(":")])
    return ""
  send_mail(pop[0])
  return ""




def dele(pop):
 try:
   
  return mail_table.del_num(int(pop[0]))
 except: 
  return mail_table.del_person(pop[0])
   

def kill(pop):
 state.set_down_state(True)
 get_it.killMail()
 sys.exit()
 return "killing auto_mail"

def refresh(pop):
 get_it.reFresh()

def voice_toggle(pop):
 if pop[0] == "1":
  state.set_speech_state(True)
  return "text to speech enabled"
 else:
  state.set_speech_state(False)
  return "text to speech disabled"

def tone_toggle(pop):
 if pop[0] == "1":
  state.tone_enabled = True
  return "Tone alerts enabled"
 else:
  state.tone_enabled = False
  return "Tone alerts disabled"

def m_screen_hide(pop):
  set_terminal_color()
  state.set_screen_state(False)
  return ""

def del_mailbox(pop):
 ok = raw_input("Do you want to delete all messages hosted on pop server?(y/n): ")
 if ok.upper() == "Y":
  
  return "well it's not going to happen because this hasn't been implemented yet."
 elif  ok.upper() == "N":
  return "No messages were deleted"
 else:
  return "Invaild option."
def m_screen_show(pop):

  state.set_screen_state(True)
  return ""


def clear(pop):
 set_terminal_color()
 return ""



#  Configuartion menu functions==========================



def one(pop):
 ok = ""
 while ok != "back":
  os.system("clear")
  print """
  Enter new email user address, or type back to return previous menu.
  Note that the previouse entry will be over written.
  """
  ok = raw_input("$: ")
  if ok == "back":
   break
  print "Save " + ok + " as user address?"
  k = raw_input("$: ")
  if k.upper() == "Y":
   config.save_token("user_name",ok)
   return "User addressed updated."
 return ""

def two(pop):
 ok = ""
 while ok != "back":
  os.system("clear")
  print """
  Enter new pop server address, or type back to return previous menu.
  Note that the previouse entry will be over written.
  """
  ok = raw_input("$: ")
  if ok == "back":
   break
  print "Save " + ok + " as pop server?"
  k = raw_input("$: ")
  if k.upper() == "Y":
   config.save_token("pop_srv",ok)
   return "pop server updated."
 return ""

def three(pop):
 message =""
 ok = ""
 while ok != "back":
  os.system("clear")
  print """
  Enter new main directory, or type back to return previous menu.
  Note that the previouse entry will be over written.
  """ 
  print message
  ok = raw_input("$: ")
  if ok == "back":
   break
  if ok != "back":
   print "Save " + ok + " as main directory?"
   k = raw_input("$: ")
   if k.upper() == "Y":
    if os.path.isdir(ok) == True:
     config.save_token("mail_dir",ok)
     return "Main directory updated."
    else:
     message = "The directory doesn't appear to vaild."
 return ""

def four(pop):
 ok = ""
 message = ""
 while ok != "back":
  os.system("clear")
  print """
  Enter voice default('0' for off or '1' for on), or type 'back' to return previous menu.
  Note that the previouse entry will be over written.
  """
  print message
  ok = raw_input("$: ")
  if ok == "back":
   break
  if ok == "1" or ok == "0":
   config.save_token("voice_state",ok)
   return "voice default saved"
  else:
   message = "Invaild setting. Choose either '0' for off or '1' for on."
   
 return ""






def five(pop):
 ok = ""
 message = ""
 while ok != "back":
  os.system("clear")
  print """
  Enter tone default('0' for off or '1' for on), or type back to return previous menu.
  Note that the previouse entry will be over written.
  """
  print message
  ok = raw_input("$: ")
  if ok == "back":
   break
  if ok == "1" or ok == "0":
   config.save_token("tone_state",ok)
   return "tone default saved"
  else:
   message = "Invaild setting. Choose either '0' for off or '1' for on."
   
 return ""



def six(pop):
 

 return "Not implemented as of yet"









def seven(pop):
 os.system("rest")
 ok = ''
 message =""
 while ok != "back":
  os.system("clear")
  warning_txt = """
 ****************Notice!****************
 Saving your password is insecure. 
 Do so at your own risk.
 Type 'back' to return to previous menu or 'delete' to remove saved passwords
 otherwise type password at prompt.

 """
 
  print warning_txt
  print message
  os.system("stty -echo")
  ok = raw_input("$: ")
  if ok == "back":
   break
  if ok.upper() == "DELETE":
   config.delete_token("pass_wrd")
   os.remove(state.get_main_path()+ "kttk")
   os.system("stty echo")
   return "Password deleted"
  elif ok != "back":
   print "Retype password"
   k = raw_input("$: ")
   os.system("stty echo")
   if ok == k:
  
     
    if config.get_token("pass_wrd") == "":
     with open(".auto_mail.config", "a") as fp:
      config.save_token("pass_wrd", state.get_main_path()+ "kttk") 
    
    try:
     with open(state.get_main_path()+ "kttk", 'w') as fp:
      fp.write(bz2.compress(k))
    except:
     print "error saving password"
    return "Password updated " 
   else:
    message = "Passwords did not match."
 os.system("stty echo")
 return ''
 
# =========================================================
def homer(pop):
 os.system("clear")
 print homer_simpson
 raw_input("   ")
 return ""
def am_config(pop):

 if pop[0] == "-set":
   setop = command_list()
   setop.add_command(one,0,"1")
   setop.add_command(two,0,"2")
   setop.add_command(three,0,"3")
   setop.add_command(four,0,"4")
   setop.add_command(five,0,"5")
   setop.add_command(six,0,"6")
   setop.add_command(seven,0,"7")
   
   ok = []
   ran=''
   while ''.join(ok) != "back":
    os.system("clear")
    print config_menu_string
    print ran
    ok = raw_input("$: ").split(" ")[0]
    ran = ''.join(setop.parse_string(ok))
   return ''
 elif pop[0] == "-info":
  return "No information yet"
 else:
  return "Unknown option "+pop[0]


def gm_srv(pop):
 ok = raw_input("Enter smpt server: ")
 print ok
 if raw_input("Save server?: ").upper() == "Y":
  git_config.save_token("smtp_srv",ok) 
  return "Smtp server saved"
 else:
  return "Server not saved"


def gm_port(pop):
 ok = raw_input("Enter smpt server's port: ")
 print ok
 if raw_input("Save por?: ").upper() == "Y":
  git_config.save_token("smtp_port",ok)
  return "Port saved"
 else:
  return "Port not saved"



def gm_config(pop):
 gm_config_menu_string = """*********\n1. Set smtp server. \n2. Set server port.\n*********"""
  

 if pop[0] == "-set":
   setop = command_list()
   setop.add_command(gm_srv,0,"1")
   setop.add_command(gm_port,0,"2")
  
   
   ok = []
   ran=''
   while ''.join(ok) != "back":
    os.system("clear")
    print gm_config_menu_string
    print """Type 'back' to return to previous menu.""" 
    print ran
    ok = raw_input("$: ").split(" ")[0]
    ran = ''.join(setop.parse_string(ok))
   return ''
 elif pop[0] == "-info":
  return "No information yet"
 else:
  return "Unknown option "+pop[0]










def ab_del(pop):
 try:
  option = int(pop[0])
 except:
  return "Invaild option!"
 new_book = []
 with open(state.get_main_path()+"addBook","r") as fp:
   ad_txt =fp.readlines()
 if option > len(ad_txt):
  return "Option out of range!"
 z = 1
 for i in ad_txt:
  if z != option:
   new_book.append(i)
  z+=1
 
 with open(state.get_main_path()+"addBook","w") as fp:
  fp.write(''.join(new_book))
 return "message deleted"


def ab_edit(pop):
 os.system("clear")
 try:
  option = int(pop[0])
 except:
  return "Invaild option"
 with open(state.get_main_path()+"addBook","r") as fp:
  ad_txt =fp.readlines()
 z = 1
 for i in ad_txt:
  if z == option:
   edit = i
   break
  z+=1
 
 print "Enter contact name or press enter to keep current name."
 ok = raw_input(edit[edit.index(":")+1:-1]+": ")
 print "Enter contact email or press enter to keep current name."
 k = raw_input(edit[:edit.index(":")]+": ")
 if k == "": k = edit[:edit.index(":")]
 if ok == "": ok = edit[edit.index(":")+1:-1]
 edit = k +":" + ok
 
 print  """Save edit(y/n?)"""
 print ok
 print k
 if raw_input("$: ").upper() == "Y":
  if ab_del(pop[0]) == "Invaild option!":
   return "Couldn't save contact an error occured"
  with open(state.get_main_path()+"addBook","a") as fp:
   fp.write(edit+"\n")
  
  return "Edit saved"
 else:
  return "Edit not saved"


def ab_add(pop):
 print """  ****************Add New Contact****************   
                                                                                      
"""
 print "Enter contact name."
 ok = raw_input("$: ")
 print "Enter contact email."
 k = raw_input("$: ")
 new_contact = k + ":" + ok +"\n"
 print "**New Contact**"
 print ok
 print k
 
 if raw_input("Save new contact?(y/n): ").upper() == "Y":
  with open(state.get_main_path()+"addBook","r") as fp:
   if new_contact in fp.read():
    return "Contact already exists"
   with open(state.get_main_path()+"addBook","a") as fp:
    fp.write(new_contact)
    return "New contact saved!"
 else:
  return "Contact not saved"
 

def addbook(pop):
 ok =""
 message =""
 abop = command_list()
 abop.add_command(ab_del,1,"delete")
 abop.add_command(ab_add,0,"new")
 abop.add_command(ab_edit,1,"edit")

 while ok !="back":
 
  os.system("clear")
  print """  ****************Address Book****************   
                                                                                      
"""
  
  with open(state.get_main_path()+"addBook") as fp:
   ad_txt =fp.readlines()
  z = 1
  for i in ad_txt:
   print str(z) +". "+ i[i.index(":")+1:-1] + " " +    i[:i.index(":")]
   z+=1
  print"""  
             Type 'delete' followed by address number to remove address. 
             Type 'edit' followed number to edit address
             Type new to access 'new' address menu          
             Type 'back' to return to previous menu."""
  for i in message:
   print i
  ok = raw_input("$: ")
  message = abop.parse_string(ok)
 return ""


def set_wait(pop):

 if pop[0] == "max":

  try:
   get_it.setWaitMax(int(pop[1]))
   return "wait max set"
  except:
   
   return "Non vaild option(must be integer)"
 elif pop[0] == "min":
  try:
   get_it.setWaitMin(int(pop[1]))
   return "wait min set"
  except:
   return "Non vaild option(must be integer)"
 elif pop[0] == "-info":
  return """              
            	'The wait' command is used to set wait times in seconds 
             between mail checks on pop server. There are two time 
             settings one for idle state (mail wasn't found during last check)
             and one for the active state(mail was found during last check) these options are set 
             with "min" and "max" respectively.
             
             Example: "wait max 30 wait min 10" 
             would set auto_mail to check for new mail every 30 seconds
             if no mail had been found in previous check, and every 10 seconds after an email had been found.
           """
 else:
  return 'Invaild usage. "wait" takes either "min" or "max" followed by integer or "-info" for help'
def link_commands():
  ins = command_list()
  ins.add_command(reply,1,"reply")
  ins.add_command(reply,1,"r",)
  ins.add_command(dele,1,"delete")
  ins.add_command(dele,1,"d")
  ins.add_command(kill,0,"kill")
  ins.add_command(refresh,0,"refresh")
  ins.add_command(clear,0,"clear")
  ins.add_command(tone_toggle,1,"tone")
  ins.add_command(voice_toggle,1,"voc")
  ins.add_command(m_screen_hide,1,"hide")
  ins.add_command(m_screen_show,1,"show")
  ins.add_command(del_mailbox,0,"nukeit")
  ins.add_command(am_config,1,"am_config")
  ins.add_command(gm_config,1,"gm_config")
  ins.add_command(set_wait,1,"wait",1)
  ins.add_command(addbook,0,"addbook")
  ins.add_command(homer,0,"homer")
  return ins

# =======================================================

def send_mail(to):
 if to not in subprocess.check_output("ps aux|grep gitmsg.py", shell=True): subprocess.Popen(state.get_main_path()+("./gitmsg.py -a " + to +" -u "+ state.get_user_name()+" -p " + state.get_user_pass() +" -m "+state.get_main_path()), shell=True) 
 

def speaK(sayString):
 if state.get_speech_state():
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


def set_terminal_color():
 os.system("reset")
 print '\x1b[1m'
 print '\x1b[37m'
 print '\x1b[40m'
 os.system("clear")


def reset_color():
 os.system("reset")
 print '\x1b[0m'
 print '\x1b[39m'
 print '\x1b[49m'
 os.system("clear")


set_terminal_color()



















def play_tone(tone,step,mod):
 if state.get_tone_state():
  t = 0 
  while(t != step):
 
   os.system('play --no-show-progress --null --channels 1 synth %s square %f' % ( .02, tone))
   tone=tone/mod
   t+=1
  return tone

 return 0







def getIn():
 sys_msg=""
 ins = link_commands()
 while(state.get_down_state()!=True):  # monitor for "kill signal" issued (either by command in getIn() or by death_daemon() in "kill" thread)
   
  
   chk =  ins.parse_string(raw_input("$: "))
   if chk != "no refresh":
    os.system("clear")
    print longtxt
    if state.print_messages == True:  
     print mail_table.list_directory()   
    for k in chk:
     print k
   
     








# ==========================Entry point============================
state=app_state()
#START UP HELL ++++++++++++++++++++++++++++++++++++++++++++++++++++
con_txt = """
  # auto_mail configuration settings
  # It's highly suggested you configure this file through auto_mail
  # The configuration menu can be accessed through auto_mail command interface by typing "am_config -set
  # help on configuration settings and addtional info can likewise be obtained by typing "am_config -info

"""


config = config_man(".auto_mail.config",con_txt)
state.set_main_path(config.get_token("mail_dir"))
state.set_pop_server(config.get_token("pop_srv"))
state.set_user_name(config.get_token("user_name"))
pass_w = config.get_token("pass_wrd")





if config.get_token("mail_dir") == "":
 print (" auto_mail did not find a main directory setting in configuartion\n This is required before auto_mail can function \n Enter main directory(or kill to exit)")
 ok = raw_input("\n : ")
 while not os.path.isdir(ok):
  if ok.upper() == "KILL":
   sys.exit()
  print "That's not a vaild directory"
  ok = raw_input("\n : ")
 ok+= ("/" if ok[-1:] != "/" else "")
 state.set_main_path(ok)

 k = raw_input("Would you like to save mail path?(y/n). \nYou can still choose to do this later by typing am_config -set\n$: ")
 if k.upper() == "Y":
  config.save_token("mail_dir",ok)
 else:
  print "main directory not saved"

git_config= config_man(state.get_main_path()+".gitmsg.config","#gitmsg.py settings")

 
if config.get_token("pop_srv") == "":
 ok = raw_input(" Please enter your pop mail server: ")
 while (os.system("ping -c 1 " + ok+ "> /dev/null")):
  ok = raw_input(" Error: Server invaild please enter a vaild pop server: ")
 state.set_pop_server(ok)
 k = raw_input(" Would you like to save pop server?(y/n). \nYou can still choose to do this later by typing am_config -set \n$: ")
 if k.upper() == "Y":
  config.save_token("pop_srv",ok)
  print " pop server saved"
 else:
  print " pop server not saved"
 

if config.get_token("user_name") == "":

 ok = raw_input(" Please enter email user name: ")
 state.set_user_name(ok)
 k = raw_input(" Would you like to save you user name?(y/n). \n You can still choose to do this later by typing am_config -set \n$: ")
 if k.upper() == "Y":
  config.save_token("user_name",ok)
  print " user saved"
 else:
  print " user not saved"


if config.get_token("pass_wrd") == "":
 os.system("stty -echo")
 ok = raw_input(" Please enter password: ")
 os.system("stty echo")
 state.set_user_pass(ok)
else:
 try:
  with open(config.get_token("pass_wrd"), "r") as fp:
   state.set_user_pass(bz2.decompress(fp.read()))
 except:
  print "Error getting login info"
  sys.exit()



# ======================================================================================================================================
































try:
 import pyttsx
 print "Succesfully imported pyttsx"
 print "Speech enabled!"
 speaK("Succesfully imported text to speech!")
 speaK("Speech enabled!")
except:

 state.tone_enabled = True
 print "Unable to import pyttsx"
 print "Text to speech won't be enabled"




t1 = threading.Thread(target=getIn) # function containing contiously running input loop
mail_table=autoMail.mail_table(state.get_main_path())
get_it=autoMail.autoMail(state.get_pop_server(),state.get_user_name(),state.get_user_pass(),state.get_main_path())
get_it.setWaitMax(30)
get_it.setWaitMin(10)
get_it.startMail()
print longtxt
print mail_table.list_directory() # start input loop

t1.start()                              

speaK("you have "+  str(mail_table.num_Ofmail()) +" " + ("messages" if mail_table.num_Ofmail() > 1 else "message" ) + " in your message directory!")
while (not state.get_down_state()):
 sender_list={}
 newMsg = get_it.newMsgs()
 if newMsg > 0:

  for i in get_it.whoMail():
   sender_list[i]=((sender_list[i]+1) if i in sender_list else 1)
  
  play_tone(play_tone(2000,2,.05)**2/2,1,2)
  speaK("you have" + str(newMsg) + "new" + ("emails" if newMsg > 1 else "email"))
  
  
  for i in sender_list:
   speaK(str(sender_list[i]) + "new " + ("messages" if sender_list[i] > 1 else "message" )+ " from" +mail_table.getName(str(i)))
   
   send_mail(i)
  os.system("clear")
  print longtxt
  if state.print_messages == True: 
   print mail_table.list_directory()
 time.sleep(5)



speaK("Auto mail shutting down, good bye")
os.system("clear")
reset_color()
print "shutting down"
sys.exit()

# ===============================================================








