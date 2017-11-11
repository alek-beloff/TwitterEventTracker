import tweepy
from pymongo import MongoClient
import time
# Get a cursor object

CONSUMER_KEY = 'cwuOhOSiMHaqSjUsyfYRVltuE'
CONSUMER_SECRET = 'JBZWaPi3ldDHgMo6NPr8MbRKEU2iHBW7xVzL094HjsoX33K4eJ'
OAUTH_TOKEN = '842632842207203328-cNbwTaG4eW4rbQJwaG4RxtZkHJ51SoO'
OAUTH_TOKEN_SECRET = 'IhypdlKWPYtpKJ8aWevWTPTyeTbtmffVRGsFcF9hXkQQg'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)


client = MongoClient()
db = client.twitter_data
def search_tweets():
    for tweet in tweepy.Cursor(api.search, geocode="55.86515,-4.25763,10km", lang="en", include_entities=True).items():
        #no geo info
        if(tweet.user.geo_enabled == False):

            print(tweet._json)
            a = tweet._json
            try:
                db.test_objectid.insert_one(a).inserted_id
            except:
                print("duplicated!")





global t
t = 0
while(True):

    ##run the program for 200 times
    if t >= 200:
        break

    try:
        search_tweets()
    except:
        print(t)
        ## sleep for 15mins if error
        time.sleep(60 * 15)
        t += 1

