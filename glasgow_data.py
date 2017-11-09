import tweepy
from pymongo import MongoClient

# Get a cursor object

CONSUMER_KEY = 'cwuOhOSiMHaqSjUsyfYRVltuE'
CONSUMER_SECRET = 'JBZWaPi3ldDHgMo6NPr8MbRKEU2iHBW7xVzL094HjsoX33K4eJ'
OAUTH_TOKEN = '842632842207203328-cNbwTaG4eW4rbQJwaG4RxtZkHJ51SoO'
OAUTH_TOKEN_SECRET = 'IhypdlKWPYtpKJ8aWevWTPTyeTbtmffVRGsFcF9hXkQQg'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth)


client = MongoClient()
db = client.twitterdb
def search_tweets():
    for tweet in tweepy.Cursor(api.search,geocode="55.86515,-4.25763,10km",lang= "en",include_entities=True).items():
        if(tweet.user.geo_enabled == False):

            print(tweet._json)
            insert = {
                tweet._json
            }
            db.hist_glasgow_nogeolocation.insert_one(insert).inserted_id

        if (tweet.user.geo_enabled == True and tweet.coordinates != None):
            print(tweet._json)
            insert = {
                tweet._json
            }
            db.hist_glasgow_geo_coordinates.insert_one(insert).inserted_id
       # if (tweet.user.geo_enabled == True and tweet.bounding_box != None and tweet.coordinates == None):
        #    print(tweet._json)
         #   insert = {
          #      tweet._json
           # }
           # db.hist_glasgow_bounding_box.insert_one(insert).inserted_id

search_tweets()


