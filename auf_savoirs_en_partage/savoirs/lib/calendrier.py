# -*- encoding: utf-8 -*-
import caldav, datetime, time, pytz
from savoirs.globals import configuration
from settings import CALENDRIER_URL

def evenements():
    rc = []

    client = caldav.DAVClient(CALENDRIER_URL)
    cal = caldav.Calendar(client, url = CALENDRIER_URL)
    start = datetime.datetime.now()
    events = cal.date_search(start)

    for e in events:
        rc.append(e.instance.vevent)

    rc.sort(lambda x,y: cmp(time.mktime(x.dtstart.value.timetuple()), 
                            time.mktime(y.dtstart.value.timetuple())))

    return rc

def evenement_info(uid):
    client = caldav.DAVClient(CALENDRIER_URL)
    cal = caldav.Calendar(client, url = CALENDRIER_URL)
    return cal.event(uid)


def combine(when, tz):
    r = datetime.datetime(when.year, when.month, when.day, 
                          when.hour, when.minute, tzinfo = pytz.timezone(unicode(tz)))
    #r = r.replace(tzinfo = pytz.timezone("UTC"))
    t = r.utctimetuple()
    r = datetime.datetime(t[0],t[1],t[2],t[3],t[4],t[5], 
                          tzinfo = pytz.timezone("UTC"))
    return r
