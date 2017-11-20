from tqdm import tqdm
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from datetime import timedelta
import numpy as np
from dateutil import parser
import re
import json
from nltk.corpus import stopwords

def RemoveStopWords(stopWords, text):
    return [w for w in text if w not in stopWords and len(w)>2]

class Tweet:
    def __init__(self, id, text, time, stopWords, bounding_box = None, coordinates = None):
        self.id = id
        self.text = RemoveStopWords(stopWords,
                                    list(filter(None,re.split('[^a-z]',text.lower()))))
        self.time = parser.parse(str(time))
        if bounding_box == None:
            self.bounding_box = []
        else:
            self.bounding_box = bounding_box
        self.coordinates = coordinates

def getUnloc():
    stopWords = set(stopwords.words('english'))

    print('Read unlocalised tweets')
    return [Tweet(json.loads(line)["_id"]["$numberLong"],
                           json.loads(line)["text"],
                           json.loads(line)["created_at"],
                           stopWords)
                     for line
                     in tqdm(open("actual_data/nogeo.json"))
                     if json.loads(line)["lang"] == "en"
                     and json.loads(line)["in_reply_to_user_id"] == None
                     and json.loads(line)["in_reply_to_status_id"] == None
                     and json.loads(line)["retweeted"] == False]
def getBbox():
    stopWords = set(stopwords.words('english'))

    print('Read bbox tweets')
    return [Tweet(json.loads(line)["_id"]["$numberLong"],
                         json.loads(line)["text"],
                         json.loads(line)["created_at"],
                         stopWords,
                         bounding_box=json.loads(line)["place"]["bounding_box"]["coordinates"][0])
                   for line
                   in tqdm(open("actual_data/bbox.json"))
                   if json.loads(line)["lang"] == "en"
                   and json.loads(line)["in_reply_to_user_id"] == None
                   and json.loads(line)["in_reply_to_status_id"] == None
                   and json.loads(line)["retweeted"] == False]

def qualityTesting(bbox_values, number, threshold, conjunction_matrix, d):
    amount_of_localized = 0
    amount_of_correct = 0
    print("Quality test is running currently...")
    for test in tqdm(bbox_values[:int(number)]):
        result = localise_to_bbox([test], [x for x in bbox_values if x != test], threshold, conjunction_matrix, d)
        if (len(result) > 0):
            amount_of_localized+=1
            if list(test.bounding_box) == list(result[0].bounding_box):
                amount_of_correct+=1
    l = amount_of_localized*100.0/float(number)
    c = amount_of_correct*100.0/amount_of_localized
    print("Amount of localized tweets is %f percent of the number given"%l)
    print("Amount of correctly localized tweets is %f percent of those which are localized"%c)

def localise_to_bbox(unloc, loc, threshold, conj_m, d):

    new_col = []
    from lshash import lshash

    lsh = lshash.LSHash(6, conj_m.shape[1])

    bbox_dict = {}

    for bbox in loc:
        lsh.index(conj_m[d[bbox.id]], extra_data=bbox.id)
        bbox_dict[bbox.id] = bbox

    for tweet in tqdm(unloc):
        cs = lsh.query(conj_m[d[tweet.id]], num_results=10, distance_func='cosine')
        points = []
        boxes = []
        cs2 = []
        for m in cs:
            if m[1] < threshold:
                cs2.append([m[0][1], m[1]])
        for idx in cs2:
            bbox = bbox_dict[idx[0]]

            tdelta = (bbox.time - tweet.time).total_seconds() / timedelta(minutes=1).total_seconds()
            # another threshold by time. Not more than a week
            if tdelta > 60 * 24 * 7: continue

            points += [(x, tdelta + 0.0001, idx[1] + 0.0001)
                       for x in bbox.bounding_box]
            boxes.append(Polygon(bbox.bounding_box))
        x0 = np.sum([x[0][0] * (1 / x[1] + 1 / x[2]) for x in points])
        y0 = np.sum([x[0][1] * (1 / x[1] + 1 / x[2]) for x in points])
        m0 = np.sum([1 / x[1] + 1 / x[2] for x in points])
        coord_res = Point([x0 / m0, y0 / m0])
        for box in boxes:
            if box.contains(coord_res):
                tweet.bounding_box = box.exterior.coords
                new_col.append(tweet)
                break
    return new_col
