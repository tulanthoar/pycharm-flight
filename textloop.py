from time import sleep

from bs4 import BeautifulSoup
from requests import Session
from requests.exceptions import ( HTTPError, MissingSchema, InvalidURL)

def nc(tagl,t):
    return(tagl.find_next(class_=t))

def soup_t(soup_text):
    b_tag = soup_text.body
    t_tag = nc(nc(b_tag,"track-panel-actualtime"),"track-panel-actualtime")
    a_tags = nc(b_tag,"track-panel-arrival").a
    arrival = a_tags.text
    t = t_tag.text
    panel = nc(b_tag,"track-panel-inner")
    status = nc(panel,'smallrow1')
    print('Arriving in ' + arrival + ' at ' + t)
    print(status.text)
    print('')
    if "En Route" in status.text and arrival is 'KSLC':
        return t
    else:
        return None


inbound = ('http://flightaware.com/live/flight/SOO597', '597')
nightBoi = ('http://flightaware.com/live/flight/AMF1062', '1062')
nightMhr = ('http://flightaware.com/live/flight/SOO197', '197')
nightRno = ('http://flightaware.com/live/flight/SOO594', '594')

flights = (inbound, nightBoi, nightMhr, nightRno)
with Session() as ses:
    print('session has begun')
    while True:
        try:
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
                print(fNum)
                arr = soup_t(soupIn)
                if arr is not None:
                    print(fNum + ' arrives at ' + arr)
            sleep(300)
        except KeyboardInterrupt:
            print('breaking..,')
            break

