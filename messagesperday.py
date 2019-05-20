#!/usr/bin/python3

import datetime, json, os, pytz, fbutil

days={}

warsaw_tz = pytz.timezone('Europe/Warsaw')
for m in fbutil.getAllMessages():
    d = datetime.datetime.fromtimestamp(m["timestamp_ms"]/1000.0, warsaw_tz)
    daynum = d.day + d.month*100 + d.year*10000
    msgs = days.get(daynum, 0)
    days[daynum] = msgs + 1

dayspairs = []

for k in days:
    dayspairs.append((days[k], k))

for x in sorted(dayspairs):
    print(x[0], x[1])