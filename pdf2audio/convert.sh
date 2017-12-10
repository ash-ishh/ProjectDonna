#!/bin/bash


path=$1
title="$(basename $path .pdf)"
mkdir $title

#copy file to newly created dir and cd into it
cp $path $title
cd $title

fname=$title".pdf"

pages=$(pdftk $fname dump_data | grep NumberOfPages | grep -oP '\d+')
echo $pages > $fname"_pages.txt"
#it fetches number of pages of arg file and save it to file_pages.txt


for (( i=1; i<=$pages; i++ ))
do
    pdftk $fname cat $i output $fname"$i"".pdf" #pull out ith page and make pdf of it filename1.pdf filename2.pdf
    pdftotext $fname"$i"".pdf" $fname"$i"".txt" #make .txt of that single page filename.pdf1.txt
    rm $1"$i"".pdf" #remove pdf
done

#mv $fname .
