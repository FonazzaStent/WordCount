"""WordCount 1.2.1 console - Count occurrences of single words and
clusters of 2 and 3 words in a text file.
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

occ_list=[]
occ_row=[]
counter=0

print ("Processing file...")
outfile=open("wordcount.txt",'w')
for n in range (0,number_words):
    count=wordlist.count(wordlist[n])
    occ_row.append(wordlist[n])
    occ_row.append(count)
    occ_list.append(occ_row)
    occ_row=[]
    if counter==progress_bar:
       print ("o",end="")
       counter=0
    counter=counter+1
onelist=dict([(t[0],t[1:]) for t in occ_list])
onelist=dict(sorted(onelist.items(), reverse=True, key=lambda item: item[1]))
outfile.write("---ooO Word occurrences count Ooo---"+"\n"+"\n")

for key,value in onelist.items():
    value=value[0]
    if value>=oneword:
        occ_string=str(key)+": "+str(value)+'\n'
        outfile.write(occ_string)

outfile.write("-----oooOOOooo-----"+"\n"+"\n")

occ_list=[]
occ_row=[]
twocluster=[]
counter=0
for word in range (1,number_words-1):
    cluster=wordlist[word]+" "+wordlist[word+1]
    twocluster.append(cluster)
number_words=len(twocluster)
for n in range (0,number_words):
    count=twocluster.count(twocluster[n])
    occ_row.append(twocluster[n])
    occ_row.append(count)
    occ_list.append(occ_row)
    occ_row=[]
    if counter==progress_bar:
       print ("o",end="")
       counter=0
    counter=counter+1
twolist=dict([(t[0],t[1:]) for t in occ_list])
twolist=dict(sorted(twolist.items(), reverse=True, key=lambda item: item[1]))
outfile.write("---ooO Two-word cluster occurrences count Ooo---"+"\n"+"\n")

for key,value in twolist.items():
    value=value[0]
    if value>=twowords:
        occ_string=str(key)+": "+str(value)+'\n'
        outfile.write(occ_string)

outfile.write("-----oooOOOooo-----"+"\n"+"\n")

occ_list=[]
occ_row=[]
threecluster=[]
counter=0
number_words=len(wordlist)
for word in range (1,number_words-2):
    cluster=wordlist[word]+" "+wordlist[word+1]+" "+wordlist[word+2]
    threecluster.append(cluster)
number_words=len(threecluster)
for n in range (0,number_words):
    count=threecluster.count(threecluster[n])
    occ_row.append(threecluster[n])
    occ_row.append(count)
    occ_list.append(occ_row)
    occ_row=[]
    if counter==progress_bar:
       print ("o",end="")
       counter=0
    counter=counter+1
threelist=dict([(t[0],t[1:]) for t in occ_list])
threelist=dict(sorted(threelist.items(), reverse=True, key=lambda item: item[1]))
outfile.write("---ooO Three-word cluster occurrences count Ooo---"+"\n"+"\n")
#print (threelist)
for key,value in threelist.items():
    value=value[0]
    if value>=threewords:
        occ_string=str(key)+": "+str(value)+'\n'
        outfile.write(occ_string)

outfile.write("-----oooOOOooo-----"+"\n"+"\n")

outfile.close()
os.system("wordcount.txt")
print ("\nOK")

        
    

