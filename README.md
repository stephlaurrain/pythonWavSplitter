# pythonWavSplitter
splitting waves with python

extract sounds from drumkits like KVLT or EZDrummer

usage :
use Mulab to generate base sounds (see /mulab / drumkitexploder)
extract tracks
copy tracks into sounds/org
run pythonWavSplitter with run.sh

enjoy !

install : pip3 install -r requirements.txt

## créer environnement virtuel :

python3 -m venv env

## activer

source env/bin/activate

## installer les dépendances

pip3 install -r requirements.txt

## version

pipenv --version

## connaître où est l'env virtuel

pipenv --venv

## le détruire

pipenv --rm

## Sauvegarder paquets

pip freeze > requirements.txt

# Références

https://github.com/jiaaro/pydub/blob/master/pydub/silence.py

# sox !
sox -V3 input.wav out.wav silence -l 1 0.0 -40d 1 1.0 -40d  : newfile : restart

# Configuration
# marche avec tempo 40
 res = silence.split_on_silence(myaudio, min_silence_len=70, silence_thresh=-40, keep_silence=False)

# confs
## pas mal  
    "split_time":70,
    "split_treshold":-40,
    "keep_silence":false,
    "seek_step":25

## quasi parfait
    split_time":500,
    "split_treshold":-40,
    "keep_silence":false,
    "seek_step":10
}

## TRES BIEN
    "split_time":100,
    "split_treshold":-50,
    "keep_silence":false,
    "seek_step":10,
    "relative_wait":2

    provoque juste décalage à partir de ridebell

    un seul decalage :
    "split_time":110,
    "split_treshold":-50,
    "keep_silence":false,
    "seek_step":5,
    "loop_wait":1

### Bons paramètres
   "split_time":100,
    "split_treshold":-70,
    "keep_silence":false,
    "seek_step":2,
    "loop_wait":1
