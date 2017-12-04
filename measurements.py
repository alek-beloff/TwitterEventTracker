import sys
from pymongo import MongoClient
import numpy as np
import tqdm

def averageWorldDistribution ():
	client = MongoClient()
	unloc = client.twitterdb.stream_nongeo_coordinates
	
	tweets = tqdm(unloc.find({},{'created_at': 1}))

	print(tweets[0])

averageWorldDistribution()