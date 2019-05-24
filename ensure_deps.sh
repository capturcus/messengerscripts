#!/bin/bash

python3 -c "import pip"
if [ $? != 0 ]; then
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
fi

sudo apt-get install -y python3-dev

sudo python3 -m pip install inquirer pytz