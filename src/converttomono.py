from pydub import AudioSegment
from pathlib import Path

def convert_stereo_to_mono(input_file, output_file):
    # Charger le fichier audio
    audio = AudioSegment.from_file(input_file)
    
    # Vérifier si le fichier est déjà mono
    if audio.channels == 1:
        print(f"{input_file} est déjà en mono.")
        return
    
    # Convertir en mono
    mono_audio = audio.set_channels(1)
    
    # Exporter le fichier converti
    mono_audio.export(output_file, format="wav")
    print(f"Fichier converti sauvegardé sous {output_file}")

# Exemple d'utilisation
org_dir = "./data/sounds/convert"
for pth in sorted(Path(org_dir).rglob('*.wav')):                        
                if pth.is_file(): 
                    convert_stereo_to_mono(pth, pth)
