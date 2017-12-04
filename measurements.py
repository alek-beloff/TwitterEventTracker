import sys
from pymongo import MongoClient
import numpy as np
from tqdm import tqdm
from dateutil import parser
import json
from datetime import timedelta, datetime

def timeZoneDistribution ():
	client = MongoClient()
	unloc = client.twitterdb.stream_nongeo_coordinates
	
	cursor = unloc.find({},{ 'user.utc_offset': 1, 'user.time_zone': 1 })
	tweets = []
	times = []

	print("getting tweets from database")
	for tweet in tqdm(cursor):
		#print (json.dumps(tweet, indent=4, sort_keys=True))
		tweets.append((tweet['user']['utc_offset'], tweet['user']['time_zone']))
   		
	tzone2_dict = {w:tz for w,tz in tweets}
	tzone_dict = {w:0 for w,tz in tweets}

	print('made a dictionary. Now counting tweets by time zones')
	for tweet, val in tqdm(tweets):
		tzone_dict[tweet] += 1

	for zone, value in tzone_dict.items():
		if zone == None: continue
		print(float(zone)/(60*60), value, tzone2_dict[zone])

def stamp(time):
	return (time - datetime(1970, 1, 1)).total_seconds()

def averageWordDistribution ():
	client = MongoClient()
	unloc = client.twitterdb.stream_nongeo_coordinates
	
	cursor = unloc.find({},{ 'user.utc_offset': 1, 'created_at': 1 })
	tweets = []
	i=0

	print("getting tweets from database")
	for tweet in tqdm(cursor):
		if tweet['user']['utc_offset'] == None: 
			print('have none!')
			continue
		tweets.append(stamp(parser.parse(str(tweet['created_at'])) + timedelta(seconds=tweet['user']['utc_offset']))/600) #10 minute intervals
	
	time_dict = {w: 0 for w in tweets}
	print('made a dictionary. Now counting tweets by time chops')
	for tweet in tqdm(tweets):
   		time_dict[tweet] += 1

	for chop, count in time_dict.items():
		if chop == None: continue
		print(datetime.fromtimestamp(chop), count, tzone2_dict[zone])














averageWordDistribution()









