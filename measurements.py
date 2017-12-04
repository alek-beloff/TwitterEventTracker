import sys
from pymongo import MongoClient
import numpy as np
import tqdm

def averageWorldDistribution ():
	client = MongoClient()
	unloc = client.twitterdb.stream_nongeo_coordinates
	
	tweets = unloc.find({},{'created_at': 1})

	print(len(tweets))
	print(tweets[0])

averageWorldDistribution()