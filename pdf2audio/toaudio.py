#author : ash_ishh_

import pyttsx3
from gtts import gTTS
import sys,os

engine = pyttsx3.init()
if(len(sys.argv) < 2):
    print("Usage : python toaudio.py dirname")
    exit(0)

dirname = sys.argv[1]
fname = dirname + ".pdf"
pages = int(open(dirname+"//"+fname+"_pages.txt","r",encoding="utf-8").read())

print(dirname)
print(fname)
print(pages)


files = []
fileobjs = []


for i in range(1,pages+1):
    files.append(fname+str(i)+".txt")

#opening files
for filename in files:
    fileobjs.append(open(dirname+"/"+filename,"r"))

for fileobj in fileobjs:
    print("..")
    if(os.path.isfile(fileobj.name+".mp3")):
        print(fileobj.name+" skipped!")
        continue
    try:
        tts = gTTS(text=fileobj.read().replace('\n',' ').encode('ascii','ignore').decode('ascii'),lang="en")
        tts.save(fileobj.name+".mp3")
    except Exception as e:
        print("error :(" + str(e))
    print(fileobj.name + " Done!")

#closing files
for fileobj in fileobjs:
    fileobj.close()
