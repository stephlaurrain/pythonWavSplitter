#!/bin/bash

input_file="./data/sounds/org/org.wav"
silence_threshold=-30dB
silence_duration=0.5
res_dir="./data/sounds/result"
res_filename=$res_dir/"ulysse1-"

rm -rf $res_dir/*
# exit

# Détecter les silences et enregistrer les informations dans silence_info.txt
ffmpeg -i "$input_file" -af silencedetect=noise=$silence_threshold:d=$silence_duration -f null - 2> silence_info.txt

# Initialiser les variables
start_time=0
segment_index=0

# Lire le fichier silence_info.txt et extraire les informations de silence
while read -r line; do
    if [[ $line == *"silence_start"* ]]; then
        silence_start=$(echo $line | grep -oP 'silence_start: \K[\d\.]+')
        ffmpeg -i "$input_file" -ss $start_time -to $silence_start -c copy "${res_filename}${segment_index}.wav"
        start_time=$silence_start
        segment_index=$((segment_index+1))
    elif [[ $line == *"silence_end"* ]]; then
        silence_end=$(echo $line | grep -oP 'silence_end: \K[\d\.]+')
        start_time=$silence_end
    fi
done < silence_info.txt

# Extraire le dernier segment
ffmpeg -i "$input_file" -ss $start_time -c copy "${res_filename}${segment_index}.wav"

