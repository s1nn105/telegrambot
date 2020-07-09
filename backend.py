#import sqlite3
#why using databases if you could implement your own
#broken buggy system for storing stuff in one big text File ?????
#There is absolutly no reason to not do that
import os.path
import sys
import pickle
SAFE_FILE="events"

if os.path.isfile(SAFE_FILE):
        pass
elif os.path.isdir(SAFE_FILE):
    print("Idiot")
    sys.exit(1)
elif not os.path.exists(SAFE_FILE):
    f=open(SAFE_FILE,"wb")
    pickle.dump([],f)
    f.close()

def get_handle(mode): #useless function
    return open(SAFE_FILE,mode)

def get_events():
    fi = get_handle("rb")
    events = pickle.load(fi)
    fi.close()
    return events
class user_chat:
    name = None
    chat_id = None
    dates = None

def write_events(events):
    fi = get_handle("wb")
    pickle.dump(events,fi)
    fi.close()
def poll_template(dates,e_name):
    question = f"Wann soll {e_name} stattfinden??"
    return [question,dates]
def add_event(event):
    events = get_events()
    events.append(event)
    write_events(events)

def new_event(name,dates,poll_msg):
    e = Event()
    e.name = name
    e.poll = poll_msg
    for i in dates:
        e.add_date(i)

    add_event(e)

class Event:
    def __init__(self):
        self.name = ""
        self.dates = {}
        self.poll = None
    def add_date(self,da):
        self.dates[da]=0

    def vote_for_date(self,dat):
        self.dates[dat]+=1
    #TODO add an nice string __str__ representation
