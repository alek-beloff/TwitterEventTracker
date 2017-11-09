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
        #no geo info
        if(tweet.user.geo_enabled == False):

            print(tweet._json)
            insert = {
                tweet._json
            }
            db.hist_glasgow_nogeolocation.insert_one(insert).inserted_id

        #exact coord
        if (tweet.user.geo_enabled == True and tweet.coordinates != None):
            print(tweet._json)
            insert = {
                tweet._json
            }
            db.hist_glasgow_geo_coordinates.insert_one(insert).inserted_id

        ##bounding box
        if (tweet.user.geo_enabled == True and tweet.place != None and tweet.coordinates == None):
            # print(decodeData(tweet))
            print(tweet.place.bounding_box.coordinates)
            insert = {
                tweet._json
            }
            db.hist_glasgow_bounding_box.insert_one(insert).inserted_id



def decodeData(status):
    return {
        "retweet_count": status.retweet_count,
        "favorited": status.favorited,
        "in_reply_to_user_id": status.in_reply_to_user_id,
        "created_at": status.created_at,
        "coordinates": status.coordinates,
        "user": {
            "created_at": status.user.created_at,
            "geo_enabled": status.user.geo_enabled,
            "lang": status.user.lang,
            "url": status.user.url,
            "description": status.user.description,
            "time_zone": status.user.time_zone,
            "location": status.user.location,
            "screen_name": status.user.screen_name,
            "protected": status.user.protected,
            "statuses_count": status.user.statuses_count,
            "profile_image_url_https": status.user.profile_image_url_https,
            "utc_offset": status.user.utc_offset,
            "followers_count": status.user.followers_count,
            "id": status.user.id,
            "id_str": status.user.id_str,
            "name": status.user.name,
            "friends_count": status.user.friends_count,
        },
        "retweeted": status.retweeted,
        "place": {
            "country_code": status.place.country_code,
            "country": status.place.country,
            "name": status.place.name,
            "full_name": status.place.full_name,
            "id": status.place.id,
            "bounding_box": {
                "type": status.place.bounding_box.type,
                "coordinates": status.place.bounding_box.coordinates
            }
        },
        "geo": status.geo,
        "_id": status.id,
        "text": status.text,
        "lang": status.lang,
        "in_reply_to_user_id_str": status.in_reply_to_user_id_str,
        "id_str": status.id_str
    }

search_tweets()


