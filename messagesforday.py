#!/usr/bin/python3

import datetime, json, os, pytz, sys, fbutil

DAY=int(sys.argv[1])

dayMsgs = []

msgs = fbutil.getAllMessages()
for msg in msgs:
    d = fbutil.timestampMsToDate(msg["timestamp_ms"])
    daynum = d.day + d.month*100 + d.year*10000
    if daynum == DAY:
        dayMsgs.append(msg)

fbutil.printMessages(dayMsgs)