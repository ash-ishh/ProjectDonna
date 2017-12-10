#author : ash_ishh_

import PyPDF2

pdffile = open("files/lastch.pdf","rb")
pdfreader = PyPDF2.PdfFileReader(pdffile)
textList = []
textFile = open("text.txt","wb")

for n in range(pdfreader.numPages):
    pageObj = pdfreader.getPage(n)
    textList.append(pageObj.extractText())
    textFile.write(pageObj.extractText().encode('utf-8'))
textFile.close()


