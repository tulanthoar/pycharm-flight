from time import sleep

from bs4 import BeautifulSoup
from requests import Session
from requests.exceptions import ( HTTPError, MissingSchema, InvalidURL)
from colorama import init
from termcolor import colored
from requests import post


def nc(tagl, t):
    return tagl.find_next(class_=t)


def soup_t(soup_text):
    b_tag = soup_text.body
    t_tag = nc(nc(b_tag, "track-panel-actualtime"), "track-panel-actualtime")
    a_tags = nc(b_tag, "track-panel-arrival").a
    arrival = a_tags.text
    t = t_tag.text
    panel = nc(b_tag, "track-panel-inner")
    status = nc(panel, 'smallrow1')
    print('Arriving in ' + arrival + ' at ' + t)
    print(status.text)
    if "En Route" in status.text and 'KSLC' in arrival:
        return t
    else:
        return None


init()
inboundRno = ('http://flightaware.com/live/flight/SOO594', '594')
inbound = ('http://flightaware.com/live/flight/SOO597', '597')
nightBoi = ('http://flightaware.com/live/flight/AMF1062', '1062')
nightMhr = ('http://flightaware.com/live/flight/SOO197', '197')
testf = ("http://flightaware.com/live/flight/SWA1844", '1844')
hipurl="https://tulanthoar.hipchat.com/v2/room/2672264/notification?auth_token=gqHibVexRWaqeAcQooOlaDm7kGniOyJLl6fglKBv"
npyurl="https://npy.hipchat.com/v2/room/2674348/notification"
npynottok="EkpHuaUe6GBYfXf9JFo32UqZ3GJ1AkHbiABr3r40"

flights = (inboundRno, inbound, nightBoi, nightMhr, testf)
with Session() as ses:
    print('session has begun')
    while True:
        try:
            print('------------------------')
            for f in flights:
                try:
                    p = ses.get(f[0])
                except InvalidURL:
                    print('invalid url, ' + f[0])
                    break
                except MissingSchema:
                    print('add http')
                    break
                except HTTPError:
                    print('http error')
                    break
                soupIn = BeautifulSoup(p.text, 'html.parser')
                parts = soupIn.title.string.split('#')
                fNum = parts[0] + f[1]
                print(colored(fNum,'yellow'))
                arr = soup_t(soupIn)
                if arr is not None:
                    print(colored(fNum + ' arrives at ' + arr,'green'))
                    msg = fNum + ' arrives at ' + arr
                    dat = {'notify':'false','message_format':'text','message':msg}
                    npydat = {'auth_token':npynottok,'notify':'false','message_format':'text','message':msg}
                    post(hipurl, data=dat)
                    post(npyurl, data=npydat)
                print('')
            sleep(300)
        except KeyboardInterrupt:
            print('breaking..,')
            break

