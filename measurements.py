import sys
from pymongo import MongoClient
import numpy as np
from tqdm import tqdm

def averageWorldDistribution ():
	client = MongoClient()
	unloc = client.twitterdb.stream_nongeo_coordinates
	
	cursor = unloc.find({},{'created_at': 1})
	tweets = []

	for i in tqdm(np.arange(100000)):
   		tweets.append(cursor.next())

averageWorldDistribution()