# -*- encoding: utf-8 -*-
import caldav, datetime, time, pytz
from savoirs import configuration

def evenements():
    rc = []

    client = caldav.DAVClient(configuration['calendrier'])
    cal = caldav.Calendar(client, url = configuration['calendrier'])
    start = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%z")
    events = cal.date_search(start)

    for e in events:
        rc.append(e.instance.vevent)

    rc.sort(lambda x,y: cmp(time.mktime(x.dtstart.value.timetuple()), 
                            time.mktime(y.dtstart.value.timetuple())))

    return rc



def evenement_info(uid):
    client = caldav.DAVClient(configuration['calendrier'])
    cal = caldav.Calendar(client, url = configuration['calendrier'])
    return cal.event(uid)

def evenement_publie(event):
    client = caldav.DAVClient(configuration['calendrier'])
    cal = caldav.Calendar(client, url = configuration['calendrier'])
    e = caldav.Event(client, parent = cal, data = event.serialize()).save()

def combine(when, tz):
    r = datetime.datetime(when.year, when.month, when.day, 
                          when.hour, when.minute, tzinfo = pytz.timezone(tz))
    #r = r.replace(tzinfo = pytz.timezone("UTC"))
    t = r.utctimetuple()
    r = datetime.datetime(*(t[0:6]), tzinfo = pytz.timezone("UTC"))
    return r
