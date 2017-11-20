import tweepy
from pymongo import MongoClient
import time
import sys


CONSUMER_KEY = 'cwuOhOSiMHaqSjUsyfYRVltuE'
CONSUMER_SECRET = 'JBZWaPi3ldDHgMo6NPr8MbRKEU2iHBW7xVzL094HjsoX33K4eJ'
OAUTH_TOKEN = '842632842207203328-cNbwTaG4eW4rbQJwaG4RxtZkHJ51SoO'
OAUTH_TOKEN_SECRET = 'IhypdlKWPYtpKJ8aWevWTPTyeTbtmffVRGsFcF9hXkQQg'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)

# auth = tweepy.OAuthHandler('q4utaFepGhE5OjujyoruBOoQg', 'D5K3P5URNUTxKnoVnggiUFsNapuNLOSx5cB7Zh6Y4HhpBhhtNy')
# auth.set_access_token('438291047-AWXl0LpNxZzjhdFA3FH7AJHtmLRK52QDJiKzq5Wz',
#                       'o3kZKFF2s9ctgVpfDVRRpMbg6BMsGUIFWlJm9wSysKyyY')

api = tweepy.API(auth)

##connect to local mongodb
client = MongoClient()
db = client.twitterdb


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):

        #if (status.place != None and status.place.name in ['NY']):# and status.place.name in ['Glasgow', 'New York', 'Chicago', 'London']):
         #   print("PLACE IS NOT NULL", status.coordinates, status.place.bounding_box.coordinates)
        #print(status)
        #if (status.user.geo_enabled == False):print ("it is me!!")

        ##bounding box data


        if (status.coordinates == None and status.place!=None):
            print(status.place.name, status.place.bounding_box.coordinates[0][::2])
            #print (status.place.name)
            a = status._json
            a["_id"] = a["id"]
            try:
                db.stream_boundingBox.insert_one(a).inserted_id
            except:
                print("duplicated!")
        elif (status.coordinates != None):

            #print('coordinates', status._json)
            a = status._json
            a["_id"] = a["id"]
            try:
                db.stream_geo_coordinates.insert_one(a).inserted_id
            except:
                print("duplicated!")
        else:
            a = status._json
            a["_id"] = a["id"]
            try:
                db.stream_nongeo_coordinates.insert_one(a).inserted_id
            except:
                print("duplicated!")
        return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print('limit')
            return False


myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())

##filter for tweets from NYC area
# myStream.filter(locations=[80.10,12.90,80.33,13.24], async=True)

# myStream.filter(track=['syria%paris'])
#myStream.filter(locations=[-89.99,-89.99,89.99,89.99], async=True)
# myStream.sample()

def Sample (myStream, lang):
    t = 0
    while (True):
        print("running sample", t)

        ##run the program for 20 times
        if t >= 20:
            break

        try:
            myStream.sample(languages = lang)
        except:
            print(t)
            ## sleep for 15mins if error
            time.sleep(60 * 15)
            t += 1

def Filter (myStream):
    t = 0
    while (True):
        print("running filter", t)

        ##run the program for 20 times
        if t >= 20:
            break
        try:
            myStream.filter(locations=[-4.393285, 55.796184, -4.090218, 55.920421,  # Glasgow
                                       -74.026675, 40.683935, -73.910408, 40.877483,  # Manhattan
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
if len(sys.argv) == 1:
    exit('use terminal to run it')
if sys.argv[1] == 'nonloc':
    print("streaming nonloc")
    Sample(myStream,["en"])
if sys.argv[1] == 'loc':
    print("streaming loc")
    Filter(myStream)


#myStream.filter(locations=[-74.284596, 40.502686, -72.474598, 41.336975, -4.3932845, 55.796184,-4.0902182,55.9204214], async=True)
