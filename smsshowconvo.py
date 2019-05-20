#!/usr/bin/python3

from lxml import etree
import sys, fbutil

NUMBER=sys.argv[1]

el = etree.parse("SmsContactsBackup/sms/sms_20151016153421.xml")

msgs = []

for s in el.xpath("//allsms")[0]:
    if s.get("address") != NUMBER:
        continue
    isMine = s.get("type") == "2"
    msg = {
        "source_convo": NUMBER,
        "timestamp_ms": int(s.get("date")),
        "sender_name": "Marcin Parafiniuk" if isMine else s.get("name"),
        "content": s.get("body").encode("utf-8").decode("latin-1")
    }
    msgs.append(msg)

fbutil.printMessages(msgs)