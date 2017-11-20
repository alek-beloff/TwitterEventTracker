from tqdm import tqdm
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from datetime import timedelta
import numpy as np
from dateutil import parser
import re

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

            tdelta = (bbox.time - tweet.time) / timedelta(minutes=1)
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