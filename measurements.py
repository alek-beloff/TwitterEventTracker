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
	j = 0

	print("getting tweets from database")
	for tweet in tqdm(cursor):
   		tweets.append(tweet)
   		#time = parser.parse(str(tweet['created_at']))
   		if str(tweet['created_at'])[20:25] == '+0000':
   			i+=1
   		else:
   			j+=1
   		print(i, j)





averageWorldDistribution()