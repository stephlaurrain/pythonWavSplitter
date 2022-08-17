# PythonWavSplitter
splitting waves with Python

extract sounds from drumkits like KVLT or EZDrummer

usage :

use Mulab to generate base sounds (see / mulab / drumkitexploder)

extract tracks

copy tracks into sounds/org

run with menu.sh

you'll find your splitted drumkit into data/sounds/result

change parameters in data/default.json (or your own json file as a parameter for python3 run.py split [json parameter file name without .json] )

enjoy !

## Parameters


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
normalization :
https://stackoverflow.com/questions/42492246/how-to-normalize-the-volume-of-an-audio-file-in-python
