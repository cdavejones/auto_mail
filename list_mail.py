#!/usr/bin/env python
import os
import sys



class listMail:
 def __init__(self,directory):
  self.directory = directory
  
  fp = open(self.directory+"mail_log.log","r")
  self.log_file = fp.readlines()
  fp.close()
  self.menu_dictionary = {}

 def reload_data(self):
  
  fp = open(self.directory+"mail_log.log","r")
  self.log_file = fp.readlines()
  fp.close()
  self.menu_dictionary = {}

 def getAdd(self,index):
  try:
   return self.menu_dictionary[index].split("|")[2][len("From: "):]
  except:
   print "fail"
 def list_directory(self):
  self.reload_data()
  menu_print = ""
 
  lines = self.log_file
  for i in range(0,len(lines)):
    
   
    self.menu_dictionary[i] = lines[i]
    item = lines[i].split("|")
    num_string = str(i)+"    "
    menu_print+=" ".join([num_string[0:len(num_string)-len(str(i))],item[0],item[2],item[4]])
    menu_print+="\n"
  
  return menu_print



 def del_num(self,index):
  try:
   sender = self.menu_dictionary[index].split("|")[2][len("From: "):]
   msg_id = self.menu_dictionary[index].split("|")[3]
  
   self.del_mail(sender,msg_id)
   return "Deleted message " + str(index)
  except:
   return "Option out of range!(message does not exist)"
         



    
      
 def del_mail(self,sender,msg_id):
  path=self.directory+sender+".mail"
  fp=open(path,"r")
  t = fp.read()
  fp.close()
  exitLoop = False
  itemized=t.split("************MESSAGE**************")
  for i in range(0,len(itemized)):
   if msg_id in itemized[i]:
    del itemized[i]
    break


  t="************MESSAGE**************".join(itemized)
  fp=open(path,"w")
  fp.write(t)
  fp.close()
  for i in range(0,len(self.log_file)):
   if self.log_file[i].find(msg_id) >-1:
    del self.log_file[i]
    break
  fp=open(self.directory+"mail_log.log","w")

  fp.write("".join(self.log_file))
  fp.close()
  self.reload_data
  self.list_directory














