# pythonWavSplitter
splitting waves with python


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

# Sauvegarder paquets

pip freeze > requirements.txt

# Références

https://github.com/jiaaro/pydub/blob/master/pydub/silence.py

# sox !
sox -V3 input.wav out.wav silence -l 1 0.0 -40d 1 1.0 -40d  : newfile : restart

# marche avec tempo 40
 res = silence.split_on_silence(myaudio, min_silence_len=70, silence_thresh=-40, keep_silence=False)