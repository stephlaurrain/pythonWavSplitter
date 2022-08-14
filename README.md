# PythonWavSplitter
splitting waves with python

extract sounds from drumkits like KVLT or EZDrummer

usage :

use Mulab to generate base sounds (see / mulab / drumkitexploder)
extract tracks
copy tracks into sounds/org

PythonWavSplitter finds the best parameters for split_threshold, split_time, seek_step and process time
then splits the files
run with run.sh

you'll find your splitted drumkit into data/sounds/result

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

