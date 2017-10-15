import tweepy
from pymongo import MongoClient
import re
import json

auth = tweepy.OAuthHandler('q4utaFepGhE5OjujyoruBOoQg', 'D5K3P5URNUTxKnoVnggiUFsNapuNLOSx5cB7Zh6Y4HhpBhhtNy')
auth.set_access_token('438291047-AWXl0LpNxZzjhdFA3FH7AJHtmLRK52QDJiKzq5Wz', 'o3kZKFF2s9ctgVpfDVRRpMbg6BMsGUIFWlJm9wSysKyyY')

api = tweepy.API(auth)

client = MongoClient("mongodb://TeamProject:JoemonJoseForever@twitterdb-shard-00-00-qc9br.mongodb.net:27017,twitterdb-shard-00-01-qc9br.mongodb.net:27017,twitterdb-shard-00-02-qc9br.mongodb.net:27017/test?ssl=true&replicaSet=TwitterDB-shard-0&authSource=admin")
db = client.twitterdb

class MyStreamListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        json_data = json.loads(raw_data)
        post_id = db.twitter_data.insert_one(json_data).inserted_id
        print(post_id)
    #def on_status(self, status):
        #print(status.text)
        #insert = {
        #    "Title" : status.text
        #}
        #post_id = db.col.insert_one(insert).inserted_id
        #print(post_id)
    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

myStream.filter(locations=[-4.50,55.79,-3.97,55.93], async=True)

#print(db.col.count())
filter = "Scotland"
regx = re.compile(".*"+filter+".*", re.IGNORECASE)
posts = db.col.find({"Title": regx})
for post in posts:
    print(post)
#print(posts.count())