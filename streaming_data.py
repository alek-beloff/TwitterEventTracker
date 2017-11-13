import tweepy
from pymongo import MongoClient

auth = tweepy.OAuthHandler('q4utaFepGhE5OjujyoruBOoQg', 'D5K3P5URNUTxKnoVnggiUFsNapuNLOSx5cB7Zh6Y4HhpBhhtNy')
auth.set_access_token('438291047-AWXl0LpNxZzjhdFA3FH7AJHtmLRK52QDJiKzq5Wz',
                      'o3kZKFF2s9ctgVpfDVRRpMbg6BMsGUIFWlJm9wSysKyyY')

api = tweepy.API(auth)



class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global i, j
        #if (status.place != None and status.place.name in ['NY']):# and status.place.name in ['Glasgow', 'New York', 'Chicago', 'London']):
         #   print("PLACE IS NOT NULL", status.coordinates, status.place.bounding_box.coordinates)
        #print(status)
        #if (status.user.geo_enabled == False):print ("it is me!!")
        if (status.coordinates == None and status.place!=None):
            i=i+1
            print(status.place.bounding_box.coordinates, status.place.name, status.user.name)
        if (status.coordinates != None):
            j=j+1
            print("place and coords %d"%j)
        #print("printed %d"%i)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

i=0
j=0
myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
#myStream.filter(locations=[-74.284596, 40.502686, -72.474598, 41.336975], async=True)
myStream.filter(track=['syria%paris'])
#myStream.filter(locations=[-89.99,-89.99,89.99,89.99], async=True)
#myStream.sample()