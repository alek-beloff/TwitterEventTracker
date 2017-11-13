import tweepy
from pymongo import MongoClient
import time


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

            print('boundingBox', status.place.bounding_box.coordinates)
            a = status._json
            a["_id"] = a["id"]
            try:
                db.stream_NYC_boundingBox.insert_one(a).inserted_id
            except:
                print("duplicated!")
        if (status.coordinates != None):


            print('coordinates', status._json)
            a = status._json
            a["_id"] = a["id"]
            try:
                db.stream_NYC_geo_coordinates.insert_one(a).inserted_id
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

global t
t = 0
while(True):

    ##run the program for 20 times
    if t >= 20:
        break

    try:
        myStream.filter(locations=[-74.284596, 40.502686, -72.474598, 41.336975], async=True)
    except:
        print(t)
        ## sleep for 15mins if error
        time.sleep(60 * 15)
        t += 1