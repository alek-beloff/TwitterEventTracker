import tweepy
from pymongo import MongoClient
import time
import sys
import datetime as d

CONSUMER_KEY = 'cwuOhOSiMHaqSjUsyfYRVltuE', 'q4utaFepGhE5OjujyoruBOoQg', '8ZHXLlxEfLQm90U19fRC08NBx', 'r8dh3IsvxNOMH2UjSIoM00gnN', 'y5UTqSuap75HuKye2NPcr7rfI'
CONSUMER_SECRET = 'JBZWaPi3ldDHgMo6NPr8MbRKEU2iHBW7xVzL094HjsoX33K4eJ', 'D5K3P5URNUTxKnoVnggiUFsNapuNLOSx5cB7Zh6Y4HhpBhhtNy', 'OjxPXXR4lDc666H2HUWtbQBtG2J5d2wDZY1B6XirQHpyZqGEbY', '0SqGVySPhZ8ngMYnQ05W8KPctMp8jbXGSdCo0qKxMYKwcewIrZ', 'blLk28TL9jEye1DH6CKDrlu4liu1kFssRMHglPXELUlzHzuhaP'
OAUTH_TOKEN = '842632842207203328-cNbwTaG4eW4rbQJwaG4RxtZkHJ51SoO', '438291047-AWXl0LpNxZzjhdFA3FH7AJHtmLRK52QDJiKzq5Wz', '916331671372353536-lVwpfVwieRCuLmyP14j0lbXGuNcitcD', '917416602634768385-pXPkTeyW9vaysd4vZflYm2pZckkIeDn', '917723257217998848-uld992dlGdvz71FpxosLs7gjAUCuIbI'
OAUTH_TOKEN_SECRET = 'IhypdlKWPYtpKJ8aWevWTPTyeTbtmffVRGsFcF9hXkQQg', 'o3kZKFF2s9ctgVpfDVRRpMbg6BMsGUIFWlJm9wSysKyyY', 'gdpRf9Qf2cU01yGPem2aJaP6sljaEah1lDdPRtyt2b75b', 'HweGKohJFWSMPDj1LwjoNExGIj1K2e7ApHdHpA7fcwl7F', 'bkDjxKNVddeDwBUIJo1mL5ENz3JTMD2Ka2jyJvAyGxsfC'

idx = 0
if len(sys.argv) == 1:
    exit('use terminal to run it')
elif sys.argv[1] == 'nonloc':
    idx = 0
elif sys.argv[1] == 'loc' and sys.argv[2].lower() == 'ny':
    idx = 1
elif sys.argv[1] == 'loc' and sys.argv[2].lower() == 'lo':
    idx = 2
elif sys.argv[1] == 'loc' and sys.argv[2].lower() == 'gla':
    idx = 3
elif sys.argv[1] == 'loc' and sys.argv[2].lower() == 'chi':
    idx = 4
else:
    exit('wrong terminal variables')

auth = tweepy.OAuthHandler(CONSUMER_KEY[idx], CONSUMER_SECRET[idx])
auth.set_access_token(OAUTH_TOKEN[idx], OAUTH_TOKEN_SECRET[idx])

# auth = tweepy.OAuthHandler('q4utaFepGhE5OjujyoruBOoQg', 'D5K3P5URNUTxKnoVnggiUFsNapuNLOSx5cB7Zh6Y4HhpBhhtNy')
# auth.set_access_token('438291047-AWXl0LpNxZzjhdFA3FH7AJHtmLRK52QDJiKzq5Wz',
#                       'o3kZKFF2s9ctgVpfDVRRpMbg6BMsGUIFWlJm9wSysKyyY')

api = tweepy.API(auth)

##connect to local mongodb
client = MongoClient()
db = client.twitterdb
i = 0
j = 0
k = 0


def checkLO(status):
    global i
    global j
    global k
    locations = ['Royal Albert Hall', 'Brent', 'Lambeth', 'London', 'Islington', 'Kensington', 'Enfield', 'Eltham',
                 'Walthamstow', 'Merton', 'Paddington', 'Camden Town', 'Wandsworth', 'Crayford', 'Hackney', 'Richmond',
                 'Greenwich', 'Barnet',
                 'East Ham', 'West Ham', 'Hillingdon', 'Staines-upon-Thames', 'Hammersmith', 'South East', 'Water Rats',
                 'Poplar', 'Sutton', 'Stratford',
                 'Wembley Stadium', 'Hackney', 'Camberwell', 'Bexley', 'Ealing', 'Romford', 'Kingston upon Thames',
                 'East', 'Harrow', 'The O2']
    if (status.coordinates == None and status.place != None):
        if (status.place.name not in locations): return True
        print(status.place.name, status.place.bounding_box.coordinates[0][::2])
        a = status._json
        a["_id"] = a["id"]
        try:
            db.stream_boundingBoxLO.insert_one(a)
            i = db.count_check_boundingBoxLO.count()
            i=i+1
            db.count_check_boundingBoxLO.insert_one(
                {"tweet_count": i, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                 "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                 "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                 "tweet_weekday": d.datetime.now().isoweekday()})
            try:
                db.full_data.insert_one(a).inserted_id
            except:
                db.duplicate_data.insert_one(a)
                k = db.count_check_duplicate_data.count()
                k=k+1
                db.count_check_duplicate_data.insert_one(
                    {"tweet_count": k, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                     "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                     "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                     "tweet_weekday": d.datetime.now().isoweekday()})

        except:
            print("duplicated!")

    elif (status.coordinates != None):
        if (status.place.name not in locations): return True
        a = status._json
        a["_id"] = a["id"]
        try:
            db.stream_geo_coordinatesLO.insert_one(a)
            j=db.count_check_geo_coordinatesLO.count()
            j = j + 1
            db.count_check_geo_coordinatesLO.insert_one(
                {"tweet_count": j, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                 "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                 "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                 "tweet_weekday": d.datetime.now().isoweekday()})
            try:
                db.full_data.insert_one(a).inserted_id
            except:
                db.duplicate_data.insert_one(a)
                k=db.count_check_duplicate_data.count()
                k = k + 1
                db.count_check_duplicate_data.insert_one(
                    {"tweet_count": k, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                     "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                     "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                     "tweet_weekday": d.datetime.now().isoweekday()})

        except:
            print("duplicated!")


def checkNY(status):
    global i
    global j
    global k
    locations = ['Manhattan', 'Staten Island', 'Queens', 'Floral Park', 'Yaphank', 'Brooklyn',
                 'Dobbs Ferry', 'North Massapequa', 'Bronx', 'New York']
    if (status.coordinates == None and status.place != None):
        if (status.place.name not in locations): return True
        print(status.place.name, status.place.bounding_box.coordinates[0][::2])
        a = status._json
        a["_id"] = a["id"]
        try:
            db.stream_boundingBoxNY.insert_one(a)
            i=db.count_check_boundingBoxNY.count()
            i = i + 1
            db.count_check_boundingBoxNY.insert_one(
                {"tweet_count": i, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                 "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                 "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                 "tweet_weekday": d.datetime.now().isoweekday()})

            try:
                db.full_data.insert_one(a)
            except:
                db.duplicate_data.insert_one(a)
                k=db.count_check_duplicate_data.count()
                k = k + 1
                db.count_check_duplicate_data.insert_one(
                    {"tweet_count": k, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                     "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                     "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                     "tweet_weekday": d.datetime.now().isoweekday()})

        except:
            print("duplicated!")
    elif (status.coordinates != None):
        if (status.place.name not in locations): return True
        a = status._json
        a["_id"] = a["id"]
        try:
            db.stream_geo_coordinatesNY.insert_one(a)
            j=db.count_check_geo_coordinatesNY.count()
            j = j + 1
            db.count_check_geo_coordinatesNY.insert_one(
                {"tweet_count": j, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                 "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                 "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                 "tweet_weekday": d.datetime.now().isoweekday()})
            try:
                db.full_data.insert_one(a)
            except:
                db.duplicate_data.insert_one(a)
                k=db.count_check_duplicate_data.count()
                k = k + 1
                db.count_check_duplicate_data.insert_one(
                    {"tweet_count": k, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                     "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                     "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                     "tweet_weekday": d.datetime.now().isoweekday()})

        except:
            print("duplicated!")


def checkGLA(status):
    global i
    global j
    global k

    locations = ['Glasgow', 'Scotland', 'Paisley']
    if (status.coordinates == None and status.place != None):
        if (status.place.name not in locations): return True
        print(status.place.name, status.place.bounding_box.coordinates[0][::2])
        a = status._json
        a["_id"] = a["id"]
        try:
            db.stream_boundingBoxGLA.insert_one(a)
            i=db.count_check_boundingBoxGLA.count()
            i=i+1
            db.count_check_boundingBoxGLA.insert_one(
                {"tweet_count": i, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                 "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                 "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                 "tweet_weekday": d.datetime.now().isoweekday()})

            try:
                db.full_data.insert_one(a).inserted_id
            except:
                db.duplicate_data.insert_one(a)
                k=db.count_check_duplicate_data.count()
                k = k + 1
                db.count_check_duplicate_data.insert_one(
                    {"tweet_count": k, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                     "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                     "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                     "tweet_weekday": d.datetime.now().isoweekday()})

        except:
            print("duplicated!")
    elif (status.coordinates != None):
        if (status.place.name not in locations): return True
        a = status._json
        a["_id"] = a["id"]
        try:
            db.stream_geo_coordinatesGLA.insert_one(a)
            j=db.count_check_geo_coordinatesGLA.count()
            j = j + 1
            db.count_check_geo_coordinatesGLA.insert_one(
                {"tweet_count": j, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                 "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                 "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                 "tweet_weekday": d.datetime.now().isoweekday()})
            try:
                db.full_data.insert_one(a).inserted_id
            except:
                db.duplicate_data.insert_one(a)
                k=db.count_check_duplicate_data.count()
                k = k + 1
                db.count_check_duplicate_data.insert_one(
                    {"tweet_count": k, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                     "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                     "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                     "tweet_weekday": d.datetime.now().isoweekday()})

        except:
            print("duplicated!")


def checkCHI(status):
    global i
    global j
    global k
    locations = ['Chicago', 'Illinois', 'Indiana', 'Michigan']
    if (status.coordinates == None and status.place != None):
        if (status.place.name not in locations): return True
        print(status.place.name, status.place.bounding_box.coordinates[0][::2])
        a = status._json
        a["_id"] = a["id"]
        try:
            db.stream_boundingBoxCHI.insert_one(a)
            i=db.count_check_boundingBoxCHI.count()
            i = i + 1
            db.count_check_boundingBoxCHI.insert_one(
                {"tweet_count": i, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                 "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                 "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                 "tweet_weekday": d.datetime.now().isoweekday()})
            try:
                db.full_data.insert_one(a).inserted_id
            except:
                db.duplicate_data.insert_one(a)
                k=db.count_check_duplicate_data.count()
                k = k + 1
                db.count_check_duplicate_data.insert_one(
                    {"tweet_count": k, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                     "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                     "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                     "tweet_weekday": d.datetime.now().isoweekday()})

        except:
            print("duplicated!")
    elif (status.coordinates != None):
        if (status.place.name not in locations): return True
        a = status._json
        a["_id"] = a["id"]
        try:
            db.stream_geo_coordinatesCHI.insert_one(a)
            j=db.count_check_geo_coordinatesCHI.count()
            j = j + 1
            db.count_check_geo_coordinatesCHI.insert_one(
                {"tweet_count": j, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                 "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                 "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                 "tweet_weekday": d.datetime.now().isoweekday()})
            try:
                db.full_data.insert_one(a).inserted_id
            except:
                db.duplicate_data.insert_one(a)
                k=db.count_check_duplicate_data.count()
                k = k + 1
                db.count_check_duplicate_data.insert_one(
                    {"tweet_count": k, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                     "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                     "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                     "tweet_weekday": d.datetime.now().isoweekday()})

        except:
            print("duplicated!")


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global i
        global k
        if (status.coordinates == None and status.place == None):
            a = status._json
            a["_id"] = a["id"]
            try:
                db.stream_nongeo_coordinates.insert_one(a)
                i=db.count_check_nongeo_coordinates.count()
                i = i + 1
                db.count_check_nongeo_coordinates.insert_one(
                    {"tweet_count": i, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                     "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                     "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                     "tweet_weekday": d.datetime.now().isoweekday()})
                try:
                    db.full_data.insert_one(a).inserted_id
                except:
                    db.duplicate_data.insert_one(a)
                    k=db.count_check_duplicate_data.count()
                    k = k + 1
                    db.count_check_duplicate_data.insert_one(
                        {"tweet_count": k, "tweet_created_at": a["created_at"], "tweet_time": d.datetime.now(),
                         "tweet_day": d.datetime.now().day, "tweet_month": d.datetime.now().month,
                         "tweet_hour": d.datetime.now().hour, "tweet_minute": d.datetime.now().minute,
                         "tweet_weekday": d.datetime.now().isoweekday()})

            except:
                print("duplicated!")
        elif sys.argv[1] == 'loc' and sys.argv[2].lower() == 'ny':
            checkNY(status)
        elif sys.argv[1] == 'loc' and sys.argv[2].lower() == 'lo':
            checkLO(status)
        elif sys.argv[1] == 'loc' and sys.argv[2].lower() == 'gla':
            checkGLA(status)
        elif sys.argv[1] == 'loc' and sys.argv[2].lower() == 'chi':
            checkCHI(status)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print('limit')
            return False


myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())


def Sample(myStream, lang):
    t = 0
    while (True):
        print("running sample", t)

        ##run the program for 20 times
        if t >= 20:
            break

        try:
            myStream.sample(languages=lang)
        except:
            print(t)
            ## sleep for 15mins if error
            time.sleep(60 * 15)
            t += 1


def FilterLO(myStream):
    t = 0
    while (True):
        print("running filter", t)

        ##run the program for 20 times
        if t >= 20:
            break
        try:
            myStream.filter(locations=[-0.510365, 51.286702, 0.334043, 51.691824])  # Greater London
        except:
            print(t)
            ## sleep for 15mins if error
            time.sleep(60 * 15)
            t += 1


def FilterNY(myStream):
    t = 0
    while (True):
        print("running filter", t)

        ##run the program for 20 times
        if t >= 20:
            break
        try:
            myStream.filter(locations=[-74.026675, 40.683935, -73.910408, 40.877483,  # Manhattan
                                       -74.255641, 40.495865, -74.052253, 40.648887,  # Staten Island
                                       -73.962582, 40.541722, -73.699793, 40.800037,  # Queens
                                       -73.722827, 40.712833, -73.687894, 40.73732,  # Floral Park (NY)
                                       -72.974376, 40.796768, -72.886039, 40.86706,  # Yaphank (Lond Island, NY)
                                       -74.041878, 40.570842, -73.855673, 40.739434,  # Brooklyn
                                       -73.883553, 40.998332, -73.845404, 41.02466,  # Dobbs Ferry (NY)
                                       -73.486593, 40.681111, -73.450056, 40.718254,  # North Massapequa
                                       -73.933612, 40.785365, -73.765271, 40.91533,  # Bronx
                                       ])
        except:
            print(t)
            ## sleep for 15mins if error
            time.sleep(60 * 15)
            t += 1


def FilterGLA(myStream):
    t = 0
    while (True):
        print("running filter", t)

        ##run the program for 20 times
        if t >= 20:
            break
        try:
            myStream.filter(locations=[-4.393285, 55.796184, -4.090218, 55.920421])  # Glasgow
        except:
            print(t)
            ## sleep for 15mins if error
            time.sleep(60 * 15)
            t += 1


def FilterCHI(myStream):
    t = 0
    while (True):
        print("running filter", t)

        ##run the program for 20 times
        if t >= 20:
            break
        try:
            myStream.filter(locations=[-87.940033, 41.644102, -87.523993, 42.023067])  # Chicago
        except:
            print(t)
            ## sleep for 15mins if error
            time.sleep(60 * 15)
            t += 1


if sys.argv[1] == 'nonloc':
    print("streaming nonloc")
    Sample(myStream, ["en"])
if sys.argv[1] == 'loc':
    if sys.argv[1] == 'loc' and sys.argv[2].lower() == 'ny':
        FilterNY(myStream)
    if sys.argv[1] == 'loc' and sys.argv[2].lower() == 'lo':
        FilterLO(myStream)
    if sys.argv[1] == 'loc' and sys.argv[2].lower() == 'gla':
        FilterGLA(myStream)
    if sys.argv[1] == 'loc' and sys.argv[2].lower() == 'chi':
        FilterCHI(myStream)
