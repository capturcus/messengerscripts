#!/usr/bin/python3
# -*- coding: utf-8 -*-

import functools, datetime, pytz, sys, os, json, re
# from whaaaaat import prompt

warsaw_tz = pytz.timezone('Europe/Warsaw')

JA = "Marcin Parafiniuk"
FOREIGN_MESSAGE_COLOR = "\033[48;5;86m\033[38;5;0m"
MY_MESSAGE_COLOR = "\033[48;5;4m\033[38;5;7m"
CLEAR_COLOR = "\033[0m"

def validateDate(d):
    if re.match(r"[0-9]{2}\.[0-9]{2}\.[0-9]{4}", d) is None:
        return "gib date like: 25.03.1997"
    l = map(int, d.split("."))
    k = []
    for x in l:
        k.append(x)
    try:
        dt = datetime.datetime(k[2], k[1], k[0])
    except Exception as e:
        return str(e)
    return True

def promptDate(msg):
    questions = [
        {
            'type': 'input',
            'name': 'date',
            'message': msg,
            'validate': validateDate
        }
    ]
    answers = prompt(questions)
    finaldate = answers['date']
    l = list(map(int, finaldate.split(".")))
    return datetime.datetime(l[2], l[1], l[0])

def promptConvo(name):
    dirs = os.listdir("..")
    names = []
    for d in dirs:
        if d.lower().startswith(name):
            names.append(d)

    if len(names) > 1:
        questions = [
            {
                'type': 'list',
                'name': 'first_name',
                'message': 'which one?',
                'choices': names
            }
        ]
        answers = prompt(questions)
        finalname = answers['first_name']
        return finalname
    elif len(names) == 0:
        print("not found")
        return None
    else:
        finalname = names[0]
    return finalname

def getMessagesOfConvo(messages_path):
    if messages_path is None:
        return None
    relPath = "../"+messages_path+"/message.json"
    if not os.path.isfile(relPath):
        return []
    with open(relPath) as f:
        j = json.loads(f.read())
        l = j['messages']
        for m in l:
            m['source_convo'] = messages_path
        return l

def getAllMessages():
    allMessages = []
    for folder in os.listdir(".."):
        if folder == "messengerscripts":
            continue
        allMessages += getMessagesOfConvo(folder)
    return allMessages

def messageSort(x, y):
    if x[0] != y[0]:
        return x[0]-y[0]
    else:
        return 1

def timestampMsToDate(ts):
    return datetime.datetime.fromtimestamp(ts/1000.0, warsaw_tz)

def getTermSize():
    try:
        return os.get_terminal_size(0)
    except OSError:
        try:
            return os.get_terminal_size(1)
        except OSError:
            return os.get_terminal_size(2)

def splitOnSpace(text, maxLen):
    if len(text) <= maxLen:
        return [text]
    i = maxLen
    while text[i] != " " and text[i] != "\n" and i != 0:
        i -= 1
    if i == 0:
        return [text[:maxLen]] + splitOnSpace(text[maxLen+1:], maxLen)
    return [text[:i]] + splitOnSpace(text[i+1:], maxLen)


def printMessages(msgs):

    if msgs is None or len(msgs) == 0:
        print("<NO MESSAGES>")
        return

    participants = set()
    convos = set()

    # first pass
    for msg in msgs:
        convos.add(msg['source_convo'].split("_")[0])
        if "sender_name" not in msg:
            participants.add("<unknown sender>")
            continue
        participant = msg["sender_name"]
        if participant != JA:
            participants.add(participant)

    maxConvLen = max(map(lambda x: len(x), convos))
    maxParLen = 0 if len(participants) == 0 else max(map(lambda x: len(x), participants))

    prefixLen = maxParLen+len("03.01.2018 21:32")+3
    if len(convos) > 1:
        prefixLen += maxConvLen+3

    # second pass
    for msg in sorted([(m['timestamp_ms'], m) for m in msgs], key=functools.cmp_to_key(messageSort)):
        m = msg[1]
        if "sender_name" not in m:
            sender = "<unknown sender>"
        else:
            if m["sender_name"] == JA:
                senderName = "<ja>"
                sender = (maxParLen - len(senderName))*" " + senderName + ":"
            else:
                senderName = m["sender_name"].encode('latin1').decode('utf8')
                sender = (maxParLen - len(senderName))*" " + senderName + ":"
        if "content" not in m:
            m['content'] = "<no content>"
        convostamp = m['source_convo'].split("_")[0]
        dt = timestampMsToDate(m['timestamp_ms'])
        time = "{:02d}.{:02d}.{} {:02d}:{:02d}".format(dt.day, dt.month, dt.year, dt.hour, dt.minute)
        message = m["content"].encode('latin1').decode('utf8')
        columns = getTermSize().columns
        startColor = MY_MESSAGE_COLOR if sender.strip() == "<ja>:" else FOREIGN_MESSAGE_COLOR
        if prefixLen < columns - 10:
            # otherwise it makes no sense

            messageLines = []
            maxLineLen = columns - prefixLen
            for line in message.split("\n"):
                if len(line) > maxLineLen:
                    lines = splitOnSpace(line, maxLineLen)
                    messageLines += lines
                else:
                    messageLines.append(line)
            
            finalMessage = startColor + messageLines[0] + CLEAR_COLOR
            for line in messageLines[1:]:
                finalMessage += "\n" + " "*prefixLen + startColor + line + CLEAR_COLOR
            
            message = finalMessage


        line = "{} {} {}".format(time, sender, message)

        if len(convos) > 1:
            line = ("[{}] "+" "*(maxConvLen - len(convostamp))).format(convostamp) + line
        sys.stdout.write(line+"\n")