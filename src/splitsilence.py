import os
import re
import subprocess

input_file = "./data/sounds/org/org.wav"
silence_threshold = "-30dB"
silence_duration = "0.5"
res_dir = "./data/sounds/result"
res_filename = os.path.join(res_dir, "fsdgSnare1-")

# Supprimer le contenu du répertoire de résultats
if not os.path.exists(res_dir):
    os.makedirs(res_dir)
else:
    for file in os.listdir(res_dir):
        file_path = os.path.join(res_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier {file_path}: {e}")

# Détecter les silences et enregistrer les informations dans silence_info.txt
subprocess.run([
    "ffmpeg", "-i", input_file, "-af", f"silencedetect=noise={silence_threshold}:d={silence_duration}",
    "-f", "null", "-"
], stderr=open("silence_info.txt", "w"))

# Initialiser les variables
start_time = 0
segment_index = 0

# Lire le fichier silence_info.txt et extraire les informations de silence
with open("silence_info.txt", "r") as f:
    for line in f:
        if "silence_start" in line:
            silence_start = float(re.search(r'silence_start: ([\d\.]+)', line).group(1))
            subprocess.run([
                "ffmpeg", "-i", input_file, "-ss", str(start_time), "-to", str(silence_start), 
                "-c", "copy", f"{res_filename}{segment_index}.wav"
            ])
            start_time = silence_start
            segment_index += 1
        elif "silence_end" in line:
            silence_end = float(re.search(r'silence_end: ([\d\.]+)', line).group(1))
            start_time = silence_end

# Extraire le dernier segment
subprocess.run([
    "ffmpeg", "-i", input_file, "-ss", str(start_time), "-c", "copy", f"{res_filename}{segment_index}.wav"
])
