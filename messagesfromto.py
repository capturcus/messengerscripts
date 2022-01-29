#!/usr/bin/python3

import fbutil, sys, datetime, pytz

warsaw_tz = pytz.timezone('Europe/Warsaw')

START = sys.argv[1]
END = sys.argv[2]

val = fbutil.validateDate(START)
if val is not True:
    print(val)
    print(START)
    sys.exit(1)

val = fbutil.validateDate(END)
if val is not True:
    print(val)
    print(END)
    sys.exit(1)

l = list(map(int, START.split(".")))
start = datetime.datetime(l[2], l[1], l[0], tzinfo=warsaw_tz)

l = list(map(int, END.split(".")))
end = datetime.datetime(l[2], l[1], l[0], tzinfo=warsaw_tz)

messages = fbutil.getAllMessages()

msgsInRange = []
for msg in messages:
    dt = fbutil.timestampMsToDate(msg["timestamp_ms"])
    if start < dt and dt <= end:
        msgsInRange.append(msg)

fbutil.printMessages(msgsInRange)
