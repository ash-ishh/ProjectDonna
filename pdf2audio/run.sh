filename=$1
withoutextension="${filename%.*}"
bash convert.sh $filename && python toaudio.py $withoutextension
