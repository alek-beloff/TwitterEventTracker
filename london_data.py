import tweepy
from pymongo import MongoClient
import time
# Get a cursor object

# CONSUMER_KEY = 'cwuOhOSiMHaqSjUsyfYRVltuE'
# CONSUMER_SECRET = 'JBZWaPi3ldDHgMo6NPr8MbRKEU2iHBW7xVzL094HjsoX33K4eJ'
# OAUTH_TOKEN = '842632842207203328-cNbwTaG4eW4rbQJwaG4RxtZkHJ51SoO'
# OAUTH_TOKEN_SECRET = 'IhypdlKWPYtpKJ8aWevWTPTyeTbtmffVRGsFcF9hXkQQg'

CONSUMER_KEY = 'cwuOhOSiMHaqSjUsyfYRVltuE', 'q4utaFepGhE5OjujyoruBOoQg', '8ZHXLlxEfLQm90U19fRC08NBx', 'r8dh3IsvxNOMH2UjSIoM00gnN', 'y5UTqSuap75HuKye2NPcr7rfI', 'tA56qfLnFMdUNHMMhrs5XtFUE'
CONSUMER_SECRET = 'JBZWaPi3ldDHgMo6NPr8MbRKEU2iHBW7xVzL094HjsoX33K4eJ', 'D5K3P5URNUTxKnoVnggiUFsNapuNLOSx5cB7Zh6Y4HhpBhhtNy', 'OjxPXXR4lDc666H2HUWtbQBtG2J5d2wDZY1B6XirQHpyZqGEbY', '0SqGVySPhZ8ngMYnQ05W8KPctMp8jbXGSdCo0qKxMYKwcewIrZ', 'blLk28TL9jEye1DH6CKDrlu4liu1kFssRMHglPXELUlzHzuhaP', 'mcyFIkViAEs2HgYAi5n9toH1rYnPKYMblYvUhz0rh7CL5mEG72'
OAUTH_TOKEN = '842632842207203328-cNbwTaG4eW4rbQJwaG4RxtZkHJ51SoO', '438291047-AWXl0LpNxZzjhdFA3FH7AJHtmLRK52QDJiKzq5Wz', '916331671372353536-lVwpfVwieRCuLmyP14j0lbXGuNcitcD', '917416602634768385-pXPkTeyW9vaysd4vZflYm2pZckkIeDn', '917723257217998848-uld992dlGdvz71FpxosLs7gjAUCuIbI', '915531741795962880-NFqV6fvMwNahmd4PWcxS9Yw2UEWhcks'
OAUTH_TOKEN_SECRET = 'IhypdlKWPYtpKJ8aWevWTPTyeTbtmffVRGsFcF9hXkQQg', 'o3kZKFF2s9ctgVpfDVRRpMbg6BMsGUIFWlJm9wSysKyyY', 'gdpRf9Qf2cU01yGPem2aJaP6sljaEah1lDdPRtyt2b75b', 'HweGKohJFWSMPDj1LwjoNExGIj1K2e7ApHdHpA7fcwl7F', 'bkDjxKNVddeDwBUIJo1mL5ENz3JTMD2Ka2jyJvAyGxsfC', 'J1p0QEWwbz6L9zjRXRsPqsRLcvzRG43UTL0mfrkj3wTs9'

t_id = 942071339216789504 - 1
end = False

def changeAPI(id):
    a = tweepy.OAuthHandler(CONSUMER_KEY[id], CONSUMER_SECRET[id])
    a.set_access_token(OAUTH_TOKEN[id], OAUTH_TOKEN_SECRET[id])
    return tweepy.API(a)

def search_tweets():
    global t_id
    global end
    max_id = t_id
    for tweet in tweepy.Cursor(api.search, geocode="40.7127,-87.62979,10km", lang="en", include_entities=True,  max_id=str(max_id-1)).items():
        date = str(tweet.created_at)[8:10]
        t_id = tweet.id
        requiredDate = ['10','11', '12', '13', '14','15', '16']
        print(tweet.created_at)
        if date not in requiredDate:
            print(tweet.text)
            end = True
            print('end', end)
            break

        #no geo info
        if(tweet.user.geo_enabled == False):

            print(tweet._json)
            a = tweet._json
            a["_id"] = a["id"]
            try:
                db.MonToWed_hist_newyork_nogeolocation.insert_one(a).inserted_id
            except:
                print("duplicated!")

        #exact coord
        if (tweet.user.geo_enabled == True and tweet.coordinates != None):
            print(tweet._json)
            a = tweet._json
            a["_id"] = a["id"]
            try:
                db.MonToWed_hist_newyork_geo_coordinates.insert_one(a).inserted_id
            except:
                print("duplicated!")

        ##bounding box
        if (tweet.user.geo_enabled == True and tweet.place != None and tweet.coordinates == None):
            # print(decodeData(tweet))
            print(tweet.place.bounding_box.coordinates)
            a = tweet._json
            a["_id"] = a["id"]
            try:
                db.MonToWed_hist_newyork_bounding_box.insert_one(tweet._json).inserted_id
            except:
                print("duplicated!")



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

auth = tweepy.OAuthHandler(CONSUMER_KEY[0], CONSUMER_SECRET[0])
auth.set_access_token(OAUTH_TOKEN[0], OAUTH_TOKEN_SECRET[0])

api = changeAPI(0)


client = MongoClient()
db = client.twitterdb


global t
t = 0
global i
i = 0
while(True):

    ##run the program for 200 times
    if t >= 2000:
        break

    try:
        api = changeAPI(i)
        search_tweets()
        if end == True:
            break
    except Exception as e:
        print('time: ', t)
        print('id: ', i)
        i = i + 1
        print(str(e))
        if i == 6:
        ## sleep for 15mins if error
            time.sleep(60 * 5)
            t += 1
            i = 0


