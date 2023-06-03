"""WordCount 1.1.1 - Count occurrencies of single words and clusters of 2
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
import io
import os

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



filename=sys.argv[1]
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
except FileNotFoundError:
    message="Not found: " +filename
    print(message)
else:
    wordlist=contents.split()
    number_words=len(wordlist)
    print("Total words of " + filename ,"is" , str(number_words))
progress_bar=int((number_words*3)/100)
word_occ=wordlist[0]
occurrencies=[]
word=[]
word.append (word_occ)
occurrencies.append(1)
index=0
occ_check=0
counter=0
print ("Processing file...")
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
    if counter==progress_bar:
       print ("o",end="")
       counter=0
    counter=counter+1
items=len(word)
rows=[[]]
for z in range (0,items):
    wordz=(word[z])
    occurrenciesz=(occurrencies[z])
    if occurrenciesz>=oneword:
       rows.append([occurrenciesz,wordz])
rows.sort(reverse=True)
outfile=open("wordcount.txt",'w')
outfile.write("---ooO Word occurrencies count Ooo---"+"\n"+"\n")
items=len(rows)
for z in range (0,items-1):
   occurrencies=str(rows[z][0])
   word=str(rows[z][1])
   outfile.write(word+": "+occurrencies+ '\n')
outfile.write("-----oooOOOooo-----"+"\n"+"\n")

word_occ1=wordlist[0]
word_occ2=wordlist[2]
occurrencies=[]
word=[]
word.append (word_occ1+" "+word_occ2)
occurrencies.append(1)
index=0
occ_check=0
counter=0
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
    if counter==progress_bar:
       print ("o",end="")
       counter=0
    counter=counter+1
items=len(word)
rows=[[]]
for z in range (0,items):
    wordz=(word[z])
    occurrenciesz=(occurrencies[z])
    if occurrenciesz>=twowords:
       rows.append([occurrenciesz,wordz])
rows.sort(reverse=True)
outfile.write("---ooO Two words cluster occurrencies count Ooo---"+"\n"+"\n")
items=len(rows)
for z in range (0,items-1):
   word=str(rows[z][0])
   occurrencies=str(rows[z][1])
   outfile.write(occurrencies+": "+word+ '\n')
outfile.write("-----oooOOOooo-----"+"\n"+"\n")

word_occ1=wordlist[0]
word_occ2=wordlist[2]
word_occ3=wordlist[3]
occurrencies=[]
word=[]
word.append (word_occ1+" "+word_occ2+" "+word_occ3)
occurrencies.append(1)
index=0
occ_check=0
counter=0
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
    if counter==progress_bar:
       print ("o",end="")
       counter=0
    counter=counter+1
items=len(word)
rows=[[]]
for z in range (0,items):
    wordz=(word[z])
    occurrenciesz=(occurrencies[z])
    if occurrenciesz>=threewords:
       rows.append([occurrenciesz,wordz])
rows.sort(reverse=True)
outfile.write("---ooO Three words cluster occurrencies count Ooo---"+"\n"+"\n")
items=len(rows)
for z in range (0,items-1):
   word=str(rows[z][0])
   occurrencies=str(rows[z][1])
   outfile.write(occurrencies+": "+word+ '\n')
outfile.close()
os.system("wordcount.txt")
print ("\nOK")

        
    

