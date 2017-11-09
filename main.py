import tweepy
import numpy as np
from pymongo import MongoClient
import re
import json
import math
import folium

auth = tweepy.OAuthHandler('q4utaFepGhE5OjujyoruBOoQg', 'D5K3P5URNUTxKnoVnggiUFsNapuNLOSx5cB7Zh6Y4HhpBhhtNy')
auth.set_access_token('438291047-AWXl0LpNxZzjhdFA3FH7AJHtmLRK52QDJiKzq5Wz', 'o3kZKFF2s9ctgVpfDVRRpMbg6BMsGUIFWlJm9wSysKyyY')

api = tweepy.API(auth)

try:
    client = MongoClient("mongodb://TeamProject:JoemonJoseForever@twitterdb-shard-00-00-qc9br.mongodb.net:27017,twitterdb-shard-00-01-qc9br.mongodb.net:27017,twitterdb-shard-00-02-qc9br.mongodb.net:27017/test?ssl=true&replicaSet=TwitterDB-shard-0&authSource=admin")
except ValueError:
    print(ValueError)
db = client.twitterdb

class MyStreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        json_data = json.loads(raw_data)
        post_id = db.twitter_data.insert_one(json_data).inserted_id
        print(post_id)
    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

#myStream.filter(locations=[-4.50,55.79,-3.97,55.93], async=True)

#localized_tweets = list(tweepy.Cursor(api.search,
#    q="university",
##    geocode="55.85,-4.25,10km",
#    #since="2017-10-13",
#    #until="2017-10-21",
#    lang="en").items())
#print(len(localized_tweets))

print(db.twitter_data.count())
filter = "is"
regx = re.compile(".*"+filter+".*", re.IGNORECASE)
posts = db.twitter_data.find({"text": regx})
for post in posts:
    print(post["place"]["bounding_box"]["type"])
print(posts.count())


def startMap(sender):
    m = folium.Map(location=[(55.79+55.93)/2, (-4.50-3.97)/2])
    filter = "is"
    regx = re.compile(".*"+filter+".*", re.IGNORECASE)
    posts = db.twitter_data.find({"text": regx})
    for post in posts:
            x0 = post["place"]["bounding_box"]["coordinates"][0][0][0]
            x1 = post["place"]["bounding_box"]["coordinates"][0][1][0]
            x2 = post["place"]["bounding_box"]["coordinates"][0][2][0]
            y0 = post["place"]["bounding_box"]["coordinates"][0][0][1]
            y1 = post["place"]["bounding_box"]["coordinates"][0][1][1]
            y2 = post["place"]["bounding_box"]["coordinates"][0][2][1]
            sq = np.square([x1-x0, y1-y0, x2-x1, y2-y1])
            sqrts = np.sqrt([sq[0]+sq[1], sq[2]+sq[3]])
            L1 = sqrts[0]
            L2 = sqrts[1]
            R = math.sqrt(L1**2 + L2**2)
            centre=[(y2+y0)/2, (x2+x0)/2]
            text = ''.join(e for e in post["text"] if e.isalnum() or e==' ')[:40]
            text = '<i>' + text + '</i>'
            if (R>1.0):
                folium.CircleMarker(centre, radius=R, popup=text,
                                color='#3186cc', fill_color='#3186cc').add_to(m)
            else:
                folium.Marker(centre, popup=text,
                             icon=folium.Icon(color='green',icon='info-sign')).add_to(m)
    display(m)