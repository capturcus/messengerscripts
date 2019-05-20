#!/usr/bin/python3


import fbutil, json
import pandas as pd
import numpy as np
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')

print("imported deps")
"""
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

"""
def avg(l):
    return sum(l)/len(l)

def moving_avg(l, N):
    half = round(N/2)+1
    cumavg = l[:half]
    ret = []
    for i in range(len(l)):
        print (l[i], cumavg)
        ret.append(avg(cumavg))
        if i+half < len(l):
            cumavg.append(l[i+half])
        if len(cumavg) > N or len(l)-i-1 < N:
            cumavg = cumavg[1:]
    return ret

x = [1,2,3,4,5,6,7,8]
N = 5

print(np.convolve(x, np.ones((N,))/N, mode='valid'))