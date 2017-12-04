import sys
from pymongo import MongoClient
import numpy as np
import tqdm

def averageWorldDistribution ():
	client = MongoClient()
	unloc = client.twitterdb.stream_nongeo_coordinates
	
	tweets = unloc.find({},{'created_at': 1})

	for i in np.arange(1000) {
   		printjson(tweets.next());
	}

averageWorldDistribution()