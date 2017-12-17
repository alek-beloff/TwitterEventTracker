from tqdm import tqdm
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from datetime import timedelta
import numpy as np
from dateutil import parser
import re
import json
from nltk.corpus import stopwords
from lshash import lshash
from scipy.optimize import minimize

def RemoveStopWords(stopWords, text):
    stopWords.add('https')
    return [w for w in text if w not in stopWords and len(w)>2]

class Tweet:
    def __init__(self, id, text, time, stopWords, user = None, bounding_box = None, coordinates = None, place = None):
        self.id = id
        self.text = RemoveStopWords(stopWords,
                                    list(filter(None,re.split('[^a-z]',text.lower()))))
        self.time = parser.parse(str(time))
        if bounding_box == None:
            self.bounding_box = []
        else:
            self.bounding_box = bounding_box
        self.coordinates = coordinates
        self.place = place
        self.user = user

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
                         bounding_box=json.loads(line)["place"]["bounding_box"]["coordinates"][0],
                         place=json.loads(line)["place"]["name"])
                   for line
                   in tqdm(open("actual_data/bbox.json",encoding="utf-8"))
                   if json.loads(line)["lang"] == "en"
                   and json.loads(line)["in_reply_to_user_id"] == None
                   and json.loads(line)["in_reply_to_status_id"] == None
                   and json.loads(line)["retweeted"] == False]
def getGeo():
    stopWords = set(stopwords.words('english'))

    print('Read geo tweets')
    return [Tweet(json.loads(line)["_id"]["$numberLong"],
                         json.loads(line)["text"],
                         json.loads(line)["created_at"],
                         stopWords,
                         json.loads(line)["user"]["name"],
                         bounding_box=json.loads(line)["place"]["bounding_box"]["coordinates"][0],
                         coordinates=json.loads(line)["coordinates"]["coordinates"],
                         place=json.loads(line)["place"]["name"])
                   for line
                   in tqdm(open("actual_data/exact.json"))
                   if json.loads(line)["lang"] == "en"
                   and json.loads(line)["in_reply_to_user_id"] == None
                   and json.loads(line)["in_reply_to_status_id"] == None
                   and json.loads(line)["retweeted"] == False]

def qualityTesting(bbox_values, number, threshold, alpha, conjunction_matrix, d):
    amount_of_localized = 0
    amount_of_correct = 0
    print("Quality test is running currently...")
    for test in tqdm(bbox_values[50:int(number)+50]):
        old_bbox = test.bounding_box
        result = localise_to_bbox([test], [x for x in bbox_values if x != test], threshold, alpha, conjunction_matrix, d)
        if (len(result) > 0):
            amount_of_localized+=1
            if list(old_bbox) == list(result[0].bounding_box):
                amount_of_correct+=1
    l = amount_of_localized*100.0/float(number)
    print (amount_of_correct)
    return amount_of_correct
    #c = amount_of_correct*100.0/amount_of_localized
    print("Amount of localized tweets is %f percent of the number given"%l)
    print("Amount of correctly localized tweets is %f percent of those which are localized"%c)

def distanceKm(p1,p2):
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(p1[0])
    lon1 = radians(p1[1])
    lat2 = radians(p2[0])
    lon2 = radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def geoTesting(exact_values, number, threshold, alpha, conjunction_matrix, d):
    amount_of_localized = 0
    amount_of_correct = 0
    print("Quality test is running currently...")
    for test in tqdm(exact_values[:int(number)]):
        a = [x for x in exact_values if x != test]

        old_coord = test.coordinates

        result = localise_to_geo([test], a, threshold, alpha, conjunction_matrix, d)
        if (len(result) > 0):
            amount_of_localized+=1
            dist = distanceKm (old_coord, result[0].coordinates)
            if dist < 0.1:
                amount_of_correct+=1
    l = amount_of_localized*100.0/float(number)
    c = amount_of_correct*100.0/amount_of_localized
    print("Amount of localized tweets is %f percent of the number given"%l)
    print("Amount of correctly localized tweets (within 100 meters) is %f percent of those which are localized"%c)

def localise_to_bbox(unloc, loc, threshold, alpha, conj_m, d):

    new_col = []

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
            boxes.append(bbox.bounding_box)
        x0 = np.sum([x[0][0] * (alpha / x[1] + (1 - alpha) / x[2]) for x in points])
        y0 = np.sum([x[0][1] * (alpha / x[1] + (1 - alpha) / x[2]) for x in points])
        m0 = np.sum([alpha / x[1] + (1 - alpha) / x[2] for x in points])
        coord_res = Point([x0 / m0, y0 / m0])
        for box in boxes:
            pol = Polygon(box)
            if pol.contains(coord_res):
                tweet.bounding_box = box
                new_col.append(tweet)
                break
    return new_col

def localise_to_geo(bbox_values,exact_values,threshold,alpha,conj_m,d):

    places_dict = {exact.place: [] for exact in exact_values + bbox_values}
    print("created dictionary of places")

    result = []

    geo_dict = places_dict.copy()
    bbox_dict = places_dict.copy()

    print("now put tweets into place buckets")
    for value in tqdm(exact_values):
        geo_dict[value.place].append(value)
    for value in tqdm(bbox_values):
        bbox_dict[value.place].append(value)
    print("tweets have been allocated")

    coord_dict = {}

    print("creating indexes...")
    for place in tqdm(places_dict):
        print("work with place %s"%place)
        lsh = lshash.LSHash(6, conj_m.shape[1])
        for tweet in geo_dict[place]:
            lsh.index(conj_m[d[tweet.id]], extra_data=tweet.id)
            coord_dict[tweet.id] = tweet
        print("index for %s is ready. Starting localisation"%place)
        for bbox in tqdm(bbox_dict[place]):
            inside_tweets = places_dict[bbox.place]
            if len(inside_tweets) < 3: continue
            cs = lsh.query(conj_m[d[bbox.id]], num_results=10, distance_func='cosine')

            cs2 = []
            for m in cs:
                if m[1] < threshold:
                    cs2.append([m[0][1], m[1]])

            points = []
            for idx in cs2:
                exact = coord_dict[idx[0]]

                tdelta = (exact.time - bbox.time).total_seconds() / timedelta(minutes=1).total_seconds()
                # another threshold by time. Not more than a week
                if tdelta > 60 * 24 * 7: continue

                points.append((exact.coordinates, tdelta + 0.0001, idx[1] + 0.0001))
            if len(points) < 3: continue
            x0 = np.sum([x[0][0] * (alpha / x[1] + (1 - alpha) / x[2]) for x in points])
            y0 = np.sum([x[0][1] * (alpha / x[1] + (1 - alpha) / x[2]) for x in points])
            m0 = np.sum([alpha / x[1] + (1 - alpha) / x[2] for x in points])
            bbox.coordinates = [x0 / m0, y0 / m0]
            result.append(bbox)

    return result