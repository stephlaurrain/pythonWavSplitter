# pythonWavSplitter
splitting waves with python

extract sounds from drumkits like KVLT or EZDrummer

usage :
use Mulab to generate base sounds (see /mulab / drumkitexploder)
extract tracks
copy tracks into sounds/org
run splitter with run.sh

find best parameters for split_threshold, split_time and seek step by running :
calculate.sh

then see last default log

change parameters in data/default.json (or your own json file as a parameter for python3 run.py [command] [json parameter file name without .json] )

enjoy !

## Create virtual env

python3 -m venv env

## Activate virtual env 

source env/bin/activate

## Install dependencies

pip3 install -r requirements.txt

## env version

pipenv --version

## Virtual env location

pipenv --venv

## Destroy it

pipenv --rm

## Save dependencies

pip freeze > requirements.txt

# References

https://github.com/jiaaro/pydub/blob/master/pydub/silence.py

# sox (but we don't mind)
sox -V3 input.wav out.wav silence -l 1 0.0 -40d 1 1.0 -40d  : newfile : restart

# Configuration

## Work with tempo 40
 res = silence.split_on_silence(myaudio, min_silence_len=70, silence_thresh=-40, keep_silence=False)

# Confs
## not bad
    "split_time":70,
    "split_threshold":-40,
    "keep_silence":false,
    "seek_step":25

## Quasi perfect
    "split_time":500,
    "split_threshold":-40,
    "keep_silence":false,
    "seek_step":10

## Very good
    "split_time":100,
    "split_threshold":-50,
    "keep_silence":false,
    "seek_step":10,
    "relative_wait":2

    provoque juste décalage à partir de ridebell

    un seul decalage :
    "split_time":110,
    "split_threshold":-50,
    "keep_silence":false,
    "seek_step":5,
    "loop_wait":1

### Best
   "split_time":100,
    "split_threshold":-70,
    "keep_silence":false,
    "seek_step":2,
    "loop_wait":1
