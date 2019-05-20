#!/usr/bin/python3
import json
import sys
import os
from whaaaaat import prompt
import fbutil

name = ("".join(sys.argv[1:])).lower()

convo = fbutil.promptConvo(name)

messages = fbutil.getMessagesOfConvo(convo)

fbutil.printMessages(messages)