import telebot
import config as cfg
import backend
import sys
modded_chat=None
try:
    bot = telebot.TeleBot(cfg.token)

except:
        print("Failed to connect to telegram ")
        sys.exit(1)

vote_event= ""
event_name=""
buf_dates = []
@bot.message_handler(commands=["new","list","dates","vote","help","chatid"])
def msg_handler(message):
    global  modded_chat
    if modded_chat==None and message.chat.type!="private":
        modded_chat=message.chat.id
    print("Hit msg handler")
    if "new" in message.text:
        new(message)
    elif "list" in message.text:
        list_events(message)
    elif "dates" in message.text:
        dates(message)
    elif "vote" in message.text:
        vote(message)
    elif "chatid" in message.text:
        getid(message)
    else:
        bot.reply_to(message,"An error occured at least this works")
        cli_help(message)

def getid(msg):
    global modded_chat
    bot.reply_to(msg,msg.chat.id)
    modded_chat = msg.chat.id



@bot.message_handler(func=lambda m: True)
def handle_all(message):
    #bot.reply_to(message,message.text)
    if message.chat.type == "private":
        text = message.text
        if len(text)<10:
            return
        print(text[:2])
        if "/e" == text[:2]:
            print("Parse message")
            text  = text[2:]
            name = ""
            p_dates = []
            for line in text.split("\n"):
                print(line)
                if line [:2]=="/n":
                    print("Name")
                    name = line[2:]
                elif line [:2]=="/d":
                    print("Date")
                    p_dates.append(line[2:])


            t_poll = backend.poll_template(p_dates, name)
            #chat_id = message.chat.id
            print(p_dates)
            print(*t_poll)
            poll_msg = bot.send_poll(modded_chat, *t_poll)  # hacky

            backend.new_event(name, buf_dates, poll_msg)

def cli_help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,"Ich kenne Folgende Befehle")
    bot.send_message(chat_id,"/new : erzeuge ein neuees Event")
    bot.send_message(chat_id,"/list : liste alle events")
    bot.send_message(chat_id,"/dates [Event name]  : zeige alle Termine des Events")
    bot.send_message(chat_id,"/vote [Event name] : vote für einen Bestimmten Termin eins events")
    bot.send_message(chat_id,"Bitte beachte case sENSiTIve")


def vote(message):
    print("Start vote")
    chat_id=message.chat.id
    event_name=message.text
    event_name = event_name.replace("/vote ","")
    print(f"Vote in {event_name}")
    events = backend.get_events()
    #get event
    for i in events:
        if i.name in event_name:
            break
    event = i
    bot.reply_to(event.poll,"Vote hier")

#currently not needed anymore
def get_vote(message):
    global vote_event
    chat_id = message.chat.id

    events  = backend.get_events()
    for i in events:
        if i.name in vote_event:
            break
    event = i
    ev_index = events.index(event)
    try:
        events[ev_index].dates[message.text]+=1
        backend.write_events(events)
    except IndexError:
        bot.send_message(chat_id,"Termin wurde nicht gefunden strange??")
    bot.send_message(chat_id,"Vielen DAnk für ihre Stimme")
    vote_event=""


def new(message):
    if message.chat.type != "private":
        bot.reply_to(message,"New events are created in Private chats moving conversation")

    #bot.reply_to(message,"you will be helped soon")
    #m=bot.send_message(message.chat.id,"Wie heißt des event???")
    #bot.register_next_step_handler(m,event_get_name)

def list_events(message):
    print("Start listing")
    chat_id = message.chat.id
    events = backend.get_events()
    bot.send_message(chat_id,"Momentan kenne ich folgende Events:")
    for event in events:
        bot.send_message(chat_id,event.name)

def dates(message):#TODO Better interface for this porcess
    print("get dates for an event")
    event_name =  message.text
    chat_id = message.chat.id
    event_name = event_name.replace("/dates ","")
    print(event_name)
    events = backend.get_events()
    for i in events:
        if i.name in event_name:
            for j in i.dates.keys():
                bot.send_message(chat_id,f"{j} :: {i.dates[j]}")
def event_get_name(message):
        text = message.text
        global name
        name = text
        m = bot.send_message(message.chat.id,"Wann soll's los gehen?")
        print(f"Name: {text}")
        bot.register_next_step_handler(m,event_get_date)


def event_get_date(message):
    global dates

    text = message.text
    if text == "x":
        global name,buf_dates
        t_poll= backend.poll_template(buf_dates,name)
        chat_id = message.chat.id
        poll_msg=bot.send_poll(chat_id,*t_poll)# hacky


        backend.new_event(name,buf_dates,poll_msg)
        name = ""
        buf_dates = []
        bot.send_message(message.chat.id,"Vielen Dank ihr event wurde gespeichert")

        print("Entry finished Cleaned vars")
        return
    print(f"New Date: {text}")
    buf_dates.append(text)
    m = bot.send_message(message.chat.id,"Was ist der Alternativ Termin?[x to quit]")
    bot.register_next_step_handler(m,event_get_date)





bot.polling()