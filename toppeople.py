#!/usr/bin/env python3

import fbutil, pytz, datetime, sys

messages = fbutil.getAllMessages()

print("messages loaded")

people = {}

warsaw_tz = pytz.timezone('Europe/Warsaw')
for m in messages:
    d = datetime.datetime.fromtimestamp(m["timestamp_ms"]/1000.0, warsaw_tz)
    daynum = d.day + d.month*100 + d.year*10000
    person_msgs = people.get(m["sender_name"], {})
    msgs = person_msgs.get(daynum, 0)
    person_msgs[daynum] = msgs + 1
    people[m["sender_name"]] = person_msgs

people_pairs = []

for person, msgs in people.items():
    people_pairs.append((len(msgs), person))

for p in sorted(people_pairs):
    print(p[1], p[0])

# person = people[sys.argv[1]]

# for i in sorted([(day, nums) for day, nums in person.items()]):
#     print(i[0], i[1])
