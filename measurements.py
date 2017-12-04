import sys
from pymongo import MongoClient
import numpy as np
from tqdm import tqdm
from dateutil import parser
import json

def averageWorldDistribution ():
	client = MongoClient()
	unloc = client.twitterdb.stream_nongeo_coordinates
	
	cursor = unloc.find({},{ 'user.utc_offset': 1 })
	tweets = []
	times = []

	print("getting tweets from database")
	for tweet in tqdm(cursor):
		#print (json.dumps(tweet, indent=4, sort_keys=True))
		tweets.append(tweet['user']['utc_offset'])
   		
   	tzone_dict = {w: 0 for w in tweets}

   	print('made a dictionary. Now counting tweets by time zones')
   	for tweet in tqdm(tweets):
   		tzone_dict[tweet] += 1

   	for zone, value in tzone_dict.items():
   		print(float(zone)/(60*60), value)





averageWorldDistribution()