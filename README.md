# PythonWavSplitter
splitting waves with Python

extract sounds from drumkits like KVLT or EZDrummer

usage :

use Mulab to generate base sounds (see / mulab / drumkitexploder)

extract tracks

copy tracks into sounds/org

PythonWavSplitter finds the best parameters for split_threshold, split_time, seek_step and process time

then splits the files

run with run.sh

you'll find your splitted drumkit into data/sounds/result

change parameters in data/default.json (or your own json file as a parameter for python3 run.py split [json parameter file name without .json] )

enjoy !

## Parameters

stop_at_good_score_found : if this value = 0, then it wont stop until the testing is complete
else, this parameter is the threshold for process_time will stop the loop and beging the split
example : stop_at_good_score_found : 1.6
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

