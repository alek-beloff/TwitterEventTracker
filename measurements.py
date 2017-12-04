import sys
from pymongo import MongoClient
import numpy as np
from tqdm import tqdm
from dateutil import parser

def averageWorldDistribution ():
	client = MongoClient()
	unloc = client.twitterdb.stream_nongeo_coordinates
	
	cursor = unloc.find({})#,{'time_zone': 1})
	tweets = []
	times = []

	print("getting tweets from database")
	for tweet in tqdm(cursor):
		print (json.dumps(json.loads(tweet), indent=4, sort_keys=True))
		tweets.append(tweet['time_zone'])
   		
   	tzone_dict = {w: 0 for w in tweets}

   	print('made a dictionary. Now counting tweets by time zones')
   	for tweet in tqdm(tweets):
   		tzone_dict[tweet['time_zone']] += 1

   	for zone in tzone_dict:
   		print(zone)





averageWorldDistribution()