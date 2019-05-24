#!/usr/bin/python3

# this script is meant to be pasted into a jupyter notebook

import fbutil, json
import pandas as pd
import numpy as np
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')

print("imported deps")

msgs = fbutil.getAllMessages()

print("imported all messages")

days = {}

for msg in msgs:
    dt = fbutil.timestampMsToDate(msg['timestamp_ms'])
    newdt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    daymsgs = days.get(newdt, 0)
    daymsgs += 1
    days[newdt] = daymsgs

days_tab = [k for k in days]
msgs_tab = [days[k] for k in days]

zip_it = zip(days_tab, msgs_tab)

data = []
for i in zip_it:
    data.append(i)

weeks = fbutil.datapointsDayToWeek(data)

hv.Points(weeks).options(width=900, height=600)