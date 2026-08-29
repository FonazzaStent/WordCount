"""WordCount 1.3.0 - Count occurrences of single words and clusters of 2
and 3 words in a text file.
Copyright (C) 2022-2026  SymbolForm

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
import webbrowser
from collections import Counter
import re


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

    #About menu
    about=tk.Menu(top, tearoff=0)
    menubar.add_cascade(menu=about,compound="left", label="?")
    about.add_command(compound="left", label="Help", command=helpbox)
    about.add_command(compound="left", label="About", command=aboutbox)

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

def tokenize(text):
    # Lowercase and extract words (letters and numbers)
    return re.findall(r"\b\w+\b", text.lower())

def count_clusters(words, size):
    return Counter(tuple(words[i:i+size]) for i in range(len(words)-size+1))

def count():
    file_object=open(filename,'r',encoding='utf-8')
    text=file_object.read()
    words = tokenize(text)
    word_counts = Counter(words)
    bigram_counts = count_clusters(words, 2)
    trigram_counts = count_clusters(words, 3)
    textbox.configure(state=NORMAL)

  
    textbox.insert(INSERT,"---ooO Word occurrences count Ooo---"+"\n"+"\n")    
    for word, count in word_counts.most_common():
        if count<oneword:
            continue
        wordstring=(f"{word}: {count}")
        #print (wordstring)
        textbox.insert(INSERT,wordstring+"\n")
        progress['value']=int((count/len(word_counts))*100)
        root.update_idletasks()

    textbox.insert(INSERT,"\n---ooO Two word clusters occurrences count Ooo---"+"\n"+"\n")    
    for bigram, count in bigram_counts.most_common():
        if count<twowords:
            continue
        bigramstring=(f"{' '.join(bigram)}: {count}")
        textbox.insert(INSERT,bigramstring+"\n") 
        progress['value']=int((count/len(bigram_counts))*100)
        root.update_idletasks()
        
    textbox.insert(INSERT,"\n---ooO Three word clusters occurrences count Ooo---"+"\n"+"\n") 
    for trigram, count in trigram_counts.most_common():
        if count<threewords:
            continue
        trigramstring=(f"{' '.join(trigram)}: {count}")
        textbox.insert(INSERT,trigramstring+"\n")
        progress['value']=int((count/len(trigram_counts))*100)
        root.update_idletasks()



#About
def aboutbox():
    global aboutbox
    #print ('about')
    aboutbox=tk.Toplevel(top)
    aboutbox.geometry("500x240")
    aboutbox.resizable(0,0)
    aboutbox.title("About")
    about_label=Label(aboutbox)
    logo=b'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'
    logoimg=tk.PhotoImage(data=logo)
    about_label.place(x=35,y=40,height=102,width=430)
    about_label.configure(image=logoimg)
    about_label.image=logoimg
    about_label.bind("<Button-1>", lambda e: callback("https://symbolform.com/"))

    url_title=Label(aboutbox)
    url_title.place(x=35,y=10,height=40,width=430)
    url_title.configure(text="WordCount 1.3.0", font=("Arial",15), anchor='center')

    url_label=Label(aboutbox)
    url_label.place(x=35,y=152,height=30,width=430)
    url_label.configure(text="https://symbolform.com/", anchor='center')
    url_label.bind("<Button-1>", lambda e: callback("https://symbolform.com/"))

    url_label2=Label(aboutbox)
    url_label2.place(x=35,y=172,height=30,width=430)
    url_label2.configure(text="https://symbolform.com/count-word-clusters/", anchor='center')
    url_label2.bind("<Button-1>", lambda e: callback("https://symbolform.com/count-word-clusters/"))

    close_button=Button(aboutbox)
    close_button.place(x=220,y=200,height=30,width=40)
    close_button.configure(text="Close")
    close_button.bind("<Button-1>", close_aboutbox)
    
def close_aboutbox(event):
    aboutbox.destroy()

def callback(url):
    webbrowser.open_new_tab(url)

def helpbox():
    global helpbox
    helpbox=tk.Toplevel(top)
    helpbox.geometry("440x540")
    helpbox.resizable(0,0)
    helpbox.title("Help")
    
    textbox1 = Text(helpbox)
    textbox1.place(x=20, y=20, height=470, width=400)
    scroll_2=Scrollbar (helpbox)
    scroll_2.place(x=421, y=20, height=470, anchor='n')
    textbox1.configure(yscrollcommand=scroll_2.set, wrap=WORD)
    scroll_2.configure(command=textbox1.yview)
    textbox1.focus_set()
    readme="WordCount 1.3.0\n\
SymbolForm\n\
\n\
Description:\n\
The program can read a text file and count the occurrences of single \
words and clusters of 2 and 3 words. The resulting list will be sorted in \
descending order (highest frequency on top).\n\
\n\
Instructions:\n\
- Launch the program\n\
- File-Open (Alt-O) to open a text file\n\
- The program will automatically start counting word frequency\n\
- The progress bar will display single word, 2 word and 3 word cluster \
  count progress\n\
- Wait for the \"Counting complete\" message\n\
- The resulting list will be displayed in the main text window\n\
- File-Save (Alt-S) to save the list to a file\n\
- File-Quit (Alt-Q) to quit the program\n\
- Alt-F to open the file menu and navigate it with the keyboard\n\
\n\
Edit the config.ini file to set minimum occurrences number:\n\
\n\
Row n. 1: minimum occurrences of single words\n\
Row n. 2: minimum occurrences of two-word clusters\n\
Row n. 3: minimum occurrences of three-word clusters\n\
\n\
"
    textbox1.insert(INSERT,readme)
    textbox1.configure(state=DISABLED)
    close_button1=Button(helpbox)
    close_button1.place(x=200,y=500,height=30,width=40)
    close_button1.configure(text="Close")
    close_button1.bind("<Button-1>", close_helpbox)

def close_helpbox(event):
    helpbox.destroy()
     
def main():
   init()
   create_app_window()
   create_textbox()
   create_menu()

main()
root.mainloop()

