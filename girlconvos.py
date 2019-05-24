#!/usr/bin/python3

# this script is meant to be pasted into a jupyter notebook

from collections import OrderedDict
import fbutil, json, os
import pandas as pd
import numpy as np
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')

print("imported deps")

girlMessages = []

for folder in os.listdir(".."):
    if folder == "messengerscripts":
        continue
    convoMessages = fbutil.getMessagesOfConvo(folder)
    participants = set()
    for msg in convoMessages:
        if "sender_name" not in msg:
            participants.add("<unknown sender>")
            continue
        participant = msg["sender_name"]
        
        if participant != fbutil.JA:
            participants.add(participant)
    
    if len(participants) == 1:
        if list(participants)[0].split(" ")[0][-1] == "a":
            girlMessages += convoMessages


print("imported all messages")

days = OrderedDict()

for msg in girlMessages:
    dt = fbutil.timestampMsToDate(msg['timestamp_ms'])
    daydt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    dayconvos = days.get(daydt, set())
    dayconvos.add(msg['source_convo'])
    days[daydt] = dayconvos

data = []

for k in sorted(days.items()):
    data.append((k[0], len(k[1])))
N = 5

# weeks = fbutil.datapointsDayToWeek(data)

hv.Points(data).options(width=900, height=600)