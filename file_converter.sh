#!/bin/bash
folder="/home1/srallaba/data/VCTK-Corpus/wav48"
new_folder="/home1/srallaba/data/VCTK-Corpus/wav16"

cd $folder

for spk in *;
do
    echo $spk
#    mkdir $new_folder/$spk
    cd $folder/$spk
    for file in *;
    do
          echo $spk/$file
               
          sox $file -r 16000 -c 1 $new_folder/$spk/$file
    done

done
