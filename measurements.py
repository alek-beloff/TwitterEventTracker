import sys
from pymongo import MongoClient
import numpy as np
from tqdm import tqdm
from dateutil import parser

def averageWorldDistribution ():
	client = MongoClient()
	unloc = client.twitterdb.stream_nongeo_coordinates
	
	cursor = unloc.find({},{'created_at': 1})
	tweets = []
	times = []

	i = 0

	print("getting tweets from database")
	for tweet in tqdm(cursor):
   		tweets.append(tweet)
   		time = parser.parse(str(tweet['created_at']))
   		print (tweet['created_at'], time)
   		i += 1
   		if i==1000:
   			return





averageWorldDistribution()