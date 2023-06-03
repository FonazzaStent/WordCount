"""WordCount 1.2.0 - Count occurrences of single words and clusters of 2
and 3 words in a text file.
Copyright (C) 2022  Fonazza-Stent

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""


import sys
from unidecode import unidecode
import io
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
import time
import shutil


try:
    import pyi_splash
    pyi_splash.close()
except:
    True

#Configuration
def init():
    global oneword
    global twowords
    global threewords
    parameters=[]
    if os.path.isfile('config.ini'):
      configfile=open("config.ini",'r')
    else:
      parameterstring='5\n5\n5'
      configfile=open("config.ini",'w')
      configfile.write(parameterstring)
      configfile.close()
      configfile=open("config.ini",'r')
    for n in range (0,3):
       line=configfile.readline()
       line=line.rstrip('\n')
       if not line.isdigit():
          line='5'
       parameters.append(line)
    configfile.close()
    oneword=int(parameters[0])
    twowords=int(parameters[1])
    threewords=int(parameters[2])    

#Create app window
def create_app_window():
        global top
        global root
        img=b'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LjEvIgogICAgeG1sbnM6R0lNUD0iaHR0cDovL3d3dy5naW1wLm9yZy94bXAvIgogICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iCiAgIHhtcE1NOkRvY3VtZW50SUQ9ImdpbXA6ZG9jaWQ6Z2ltcDo1M2ZmOTYxOS05ZGI5LTRlNzMtODdkMi0xNmIwZTE5NDhlZDAiCiAgIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6NDY5M2JhMTktZmE5ZS00MmQ2LThjN2EtZDg5OGU4OWJkMWUxIgogICB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ODhjZmYxNjctMDQ4MC00NDI3LWI1ZGYtZmI2YjcyMGVjNDRiIgogICBkYzpGb3JtYXQ9ImltYWdlL3BuZyIKICAgR0lNUDpBUEk9IjIuMCIKICAgR0lNUDpQbGF0Zm9ybT0iV2luZG93cyIKICAgR0lNUDpUaW1lU3RhbXA9IjE2NzEwMTYzMTAzMTg1MDAiCiAgIEdJTVA6VmVyc2lvbj0iMi4xMC4zMiIKICAgdGlmZjpPcmllbnRhdGlvbj0iMSIKICAgeG1wOkNyZWF0b3JUb29sPSJHSU1QIDIuMTAiCiAgIHhtcDpNZXRhZGF0YURhdGU9IjIwMjI6MTI6MTRUMTI6MTE6NDgrMDE6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDIyOjEyOjE0VDEyOjExOjQ4KzAxOjAwIj4KICAgPHhtcE1NOkhpc3Rvcnk+CiAgICA8cmRmOlNlcT4KICAgICA8cmRmOmxpCiAgICAgIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiCiAgICAgIHN0RXZ0OmNoYW5nZWQ9Ii8iCiAgICAgIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6ZmI5NTFlYjItOTViZC00YjkwLTkwMDItNjg2NTY3OWEyMWJiIgogICAgICBzdEV2dDpzb2Z0d2FyZUFnZW50PSJHaW1wIDIuMTAgKFdpbmRvd3MpIgogICAgICBzdEV2dDp3aGVuPSIyMDIyLTEwLTI4VDE2OjM1OjM2Ii8+CiAgICAgPHJkZjpsaQogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmJiNjYzNjRhLTRkNmYtNDI3Zi05Yjg4LWRmNzRkOGMyYWZlNSIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChXaW5kb3dzKSIKICAgICAgc3RFdnQ6d2hlbj0iMjAyMi0xMi0xNFQxMjoxMTo1MCIvPgogICAgPC9yZGY6U2VxPgogICA8L3htcE1NOkhpc3Rvcnk+CiAgPC9yZGY6RGVzY3JpcHRpb24+CiA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgCjw/eHBhY2tldCBlbmQ9InciPz6QqEjbAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5gwOCwsyDpCvpwAACb1JREFUSMd9VnlwFFUa/17360nmnkkymSSTSSYXCUuGQKIRSuT0oJQVcF3xogAvLJTVBe8Dd1fDigdQKIjItSV4ALohuCvkwgiZEFys7AYkTEIYEghJ5p7MdM/R7739YyAguvurrq7q7vre+32//r7v91BDY0NxcXFeXh4AJBKJYCDgdns8Hg9llBDC87wyVZmeke4edjcfbj7b21tgK9BqtbFYDGPMcYjjeADgea64qNhgMOTn52dnZwHA2nXrVvxxBQOGESBgEAqGLly8wChDCBmNhoICm1KpBABRlFpbWx1tbY62tjtuvy0tLa2+obHtX8fhF0hRKB5ZuKiwsCDPmldcXIQxlmUZYx4DAsaYXq/T63/DABhjoWBoYOCS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'
        root= tk.Tk()
        top= root
        top.geometry("600x450+468+138")
        top.resizable(1,1)
        top.title("WordCount")
        favicon=tk.PhotoImage(data=img) 
        root.wm_iconphoto(True, favicon)

#Textbox
def create_textbox():
        global textbox
        global progress
        global label1
        textbox = Text(top)
        textbox.place(relx=0.033, rely=0.022, relheight=0.820, relwidth=0.933)
        scroll_1=Scrollbar (top)
        scroll_1.pack(side=RIGHT, fill=Y)
        textbox.configure(yscrollcommand=scroll_1.set)
        scroll_1.configure(command=textbox.yview)
        textbox.configure(state=DISABLED)
        progress = Progressbar(top, orient = HORIZONTAL, length = 100, mode = 'determinate')
        progress.place(relx=0.075, rely=0.860,relwidth=0.850)
        label1=Label(top,text=' ')
        label1.place(relx=0.40,rely=0.93,relwidth=0.70,height=20)

#menu
def create_menu():
    menubar=tk.Menu(top, tearoff=0)
    top.configure(menu=menubar)
    sub_menu=tk.Menu(top, tearoff=0)
    menubar.add_cascade(menu=sub_menu,compound="left", label="File")
    sub_menu.add_command(compound="left", label="Open", command=open_file, accelerator="Alt+O")
    sub_menu.add_command(compound="left",label="Save", command=Save_to_file,accelerator="Alt+S")
    sub_menu.add_command(compound="left",label="Quit", command=QuitApp, accelerator="Alt+Q")
    top.bind_all("<Alt-o>",open_file_hotkey)
    top.bind_all("<Alt-s>",Save_hotkey)
    top.bind_all("<Alt-q>",Quit_hotkey)
    menubar.bind_all("<Alt-f>",menubar.invoke(1))

def open_file_hotkey(event):
    open_file()

def Save_hotkey(event):
    Save_to_file()

def Quit_hotkey (event):
    QuitApp()

#Open File
def open_file():
    global filename
    data=[('TXT', '*.txt')]
    filename=askopenfilename(filetypes=data)
    textbox.delete(1.0,END)
    count()

#Save to file
def Save_to_file():
        counttxt=textbox.get(1.0,END)
        data=[('Text','*.txt')]
        countfilename=asksaveasfilename(filetypes=data, defaultextension=data)
        if str(countfilename)!='':
            countfile =open(countfilename,'w')
            countfile.write(counttxt)
            countfile.close()
       

#Quit
def QuitApp():
    okcancel= messagebox.askokcancel("Quit?","Do you want to quit the app?",default="ok")
    if okcancel== True:
        top.destroy()

def count():
   filesize=os.path.getsize(filename)
   counter=1
   step=0
   textbox.configure(state=NORMAL)
   try:
      with io.open(filename, 'r', encoding='utf-8') as file_object:
           contents=''
           eof=False
           while eof==False:
               try:
                   char=file_object.read(1)
               except:
                   char="?"
               contents=contents+char
               if char=='':
                   eof=True
               if step<200:
                   step= step+1
               else:
                   progress['value']=int((counter/filesize)*100)+((200/filesize)*100)
                   root.update_idletasks()
                   step=0
               counter=counter+1
   except FileNotFoundError:
       message="Not found: " +filename
       print(message)
   else:
       wordlist=contents.split()
       number_words=len(wordlist)
       #print("Total words of " + filename ,"is" , str(number_words))
   word_occ=wordlist[0]
   occurrencies=[]
   word=[]
   word.append (word_occ)
   occurrencies.append(1)
   index=0
   occ_check=0
   totalcompute=len(wordlist)
   counter=1
   label1.configure(text="Counting single words")
   for n in range (0,number_words):
       word_occ=wordlist[n]
       items=len(word)
       for x in range (0,items):
           if word_occ==word[x]:
               count=int(occurrencies[x])
               occurrencies[x]=count+1
               occ_check=1
       if occ_check==0:    
           word.append(word_occ)
           occurrencies.append(1)
       occ_check=0
       progress['value']=int((counter/number_words)*100)
       root.update_idletasks()
       counter=counter+1       
   items=len(word)
   rows=[[]]
   for z in range (0,items):
       wordz=(word[z])
       occurrenciesz=(occurrencies[z])
       if occurrenciesz>=oneword:
           rows.append([occurrenciesz,wordz])
   rows.sort(reverse=True)
   textbox.insert(INSERT,"---ooO Word occurrencies count Ooo---"+"\n"+"\n")
   items=len(rows)
   for z in range (0,items-1):
      occurrencies=str(rows[z][0])
      word=str(rows[z][1])
      try:
          textbox.insert(INSERT,word+": "+occurrencies+ '\n')
      except:
          error=True
   textbox.insert(INSERT,"-----oooOOOooo-----"+"\n"+"\n")

   word_occ1=wordlist[0]
   word_occ2=wordlist[2]
   occurrencies=[]
   word=[]
   word.append (word_occ1+" "+word_occ2)
   occurrencies.append(1)
   index=0
   occ_check=0
   counter=1
   label1.configure(text="Counting 2 word clusters")
   for n in range (0,number_words-1):
       word_occ1=wordlist[n]
       word_occ2=wordlist[n+1]
       items=len(word)
       for x in range (0,items):
           word_occ=word_occ1+" "+word_occ2
           if word_occ==word[x]:
               count=int(occurrencies[x])
               occurrencies[x]=count+1
               occ_check=1
       if occ_check==0:    
           word.append(word_occ)
           occurrencies.append(1)
       occ_check=0
       progress['value']=int((counter/number_words)*100)
       root.update_idletasks()
       counter=counter+1
   items=len(word)
   rows=[[]]
   for z in range (0,items):
       wordz=(word[z])
       occurrenciesz=(occurrencies[z])
       if occurrenciesz>=twowords:
           rows.append([occurrenciesz,wordz])
   rows.sort(reverse=True)
   #outfile.write("---ooO Two words cluster occurrencies count Ooo---"+"\n"+"\n")
   textbox.insert(INSERT,"---ooO Two words cluster occurrencies count Ooo---"+"\n"+"\n")
   items=len(rows)
   for z in range (0,items-1):
      word=str(rows[z][0])
      occurrencies=str(rows[z][1])
      try:
          #outfile.write(occurrencies+": "+word+ '\n')
          textbox.insert(INSERT,occurrencies+": "+word+ '\n')
      except:
          error=True
   #outfile.write("-----oooOOOooo-----"+"\n"+"\n")
   textbox.insert(INSERT,"-----oooOOOooo-----"+"\n"+"\n")

   word_occ1=wordlist[0]
   word_occ2=wordlist[2]
   word_occ3=wordlist[3]
   occurrencies=[]
   word=[]
   word.append (word_occ1+" "+word_occ2+" "+word_occ3)
   occurrencies.append(1)
   index=0
   occ_check=0
   counter=1
   label1.configure(text="Counting 3 word clusters")
   for n in range (0,number_words-2):
       word_occ1=wordlist[n]
       word_occ2=wordlist[n+1]
       word_occ3=wordlist[n+2]
       items=len(word)
       for x in range (0,items):
           word_occ=word_occ1+" "+word_occ2+" "+word_occ3
           if word_occ==word[x]:
               count=int(occurrencies[x])
               occurrencies[x]=count+1
               occ_check=1
       if occ_check==0:    
           word.append(word_occ)
           occurrencies.append(1)
       occ_check=0
       progress['value']=int((counter/number_words)*100)
       root.update_idletasks()
       counter=counter+1
   items=len(word)
   rows=[[]]
   for z in range (0,items):
       wordz=(word[z])
       occurrenciesz=(occurrencies[z])
       if occurrenciesz>=threewords:
           rows.append([occurrenciesz,wordz])
   rows.sort(reverse=True)
   #outfile.write("---ooO Three words cluster occurrencies count Ooo---"+"\n"+"\n")
   textbox.insert(INSERT,"---ooO Three words cluster occurrencies count Ooo---"+"\n"+"\n")
   items=len(rows)
   for z in range (0,items-1):
      word=str(rows[z][0])
      occurrencies=str(rows[z][1])
      try:
          #outfile.write(occurrencies+": "+word+ '\n')
          textbox.insert(INSERT,occurrencies+": "+word+ '\n')
      except:
          error=True
   #outfile.close()
   #os.system("wordcount.txt")
   #print ("OK")
   progress['value']=100
   root.update_idletasks()
   label1.configure(text="Counting complete")
def main():
   init()
   create_app_window()
   create_textbox()
   create_menu()

main()
root.mainloop()

