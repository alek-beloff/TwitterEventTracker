from localisation_core import *
import sys
from pymongo import MongoClient

def getGeoFromDatabase(place):
    stopWords = set(stopwords.words('english'))

    client = MongoClient()
    db = client.twitterdb
    source = db.final_stream_geo_coordinatesNY
    if place.lower() == "gla":
        source = db.final_stream_geo_coordinatesGLA
    if place.lower() == "lo":
        source = db.final_stream_geo_coordinatesLO
    if place.lower() == "chi":
        source = db.final_stream_geo_coordinatesCHI

    return [Tweet(line["_id"],
                         line["text"],
                         line["created_at"],
                         stopWords,
                         coordinates=line["coordinates"]["coordinates"],
                         bounding_box=line["place"]["bounding_box"]["coordinates"][0],
                         place=line["place"]["name"])
                   for line
                   in tqdm(source.find())
                   if line["lang"] == "en"
                   and line["in_reply_to_user_id"] == None
                   and line["in_reply_to_status_id"] == None
                   and line["retweeted"] == False]

def getBboxFromDatabase(place):
    stopWords = set(stopwords.words('english'))

    client = MongoClient()
    db = client.twitterdb
    source = db.final_stream_boundingBoxNY
    if place.lower() == "gla":
        source = db.final_stream_boundingBoxGLA
    if place.lower() == "lo":
        source = db.final_stream_boundingBoxLO
    if place.lower() == "chi":
        source = db.final_stream_boundingBoxCHI

    return [Tweet(line["_id"],
                         line["text"],
                         line["created_at"],
                         stopWords,
                         bounding_box=line["place"]["bounding_box"]["coordinates"][0],
                         place=line["place"]["name"])
                   for line
                   in tqdm(source.find())
                   if line["lang"] == "en"
                   and line["in_reply_to_user_id"] == None
                   and line["in_reply_to_status_id"] == None
                   and line["retweeted"] == False]

if len(sys.argv) != 2:
    exit('use terminal to specify the city')

if sys.argv[1].lower() not in ['ny', 'lo', 'chi', 'gla'] :
    exit('argument is incorrect')

print("reading bbox tweets...")
bbox_values = getBboxFromDatabase(sys.argv[1])

print("reading geo tweets...")
exact_values = getGeoFromDatabase(sys.argv[1])

print("we have %d bbox tweets to be localised using %d geo tweets"%(len(bbox_values), len(exact_values)))

exact = [value.text for value in exact_values + bbox_values]
# flatten the list of lists to 1d array
exact_flatten = [item for sublist in exact for item in sublist]
# remove duplicates
exact_dict = {w: '' for w in exact_flatten}
# enumerate without duplicates
exact_enum = {w: idx for idx, w in enumerate(exact_dict)}

exact_matrix = np.zeros((len(exact_values + bbox_values), len(exact_enum)), dtype=bool)
d = dict()
for idx, tweet in enumerate(exact_values + bbox_values):
    d[tweet.id] = idx
    for w in tweet.text:
        exact_matrix[idx, exact_enum[w]] = True

print("matrix is created. size is %d on %d"%(exact_matrix.shape))

exacts = localise_to_geo(bbox_values, exact_values, threshold=10.0, alpha=0.5, conj_m=exact_matrix, d=d)
print("inserting values into documents...")

client = MongoClient()
db = client.twitterdb


source = db.localised_geo_tweetsNY
if sys.argv[1].lower() == "lo":
    source = db.localised_geo_tweetsLO
if sys.argv[1].lower() == "gla":
    source = db.localised_geo_tweetsGLA
if sys.argv[1].lower() == "chi":
    source = db.localised_geo_tweetsCHI

for tweet in tqdm(exacts + exact_values):
    raw = {
        "_id": tweet.id,
        "coordinates": {
            "coordinates": tweet.coordinates
        },
        "place": {
            "name": tweet.place,
            "bounding_box": {
                "coordinates": [tweet.bounding_box]
            }
        },
        "lang": "en",
        "in_reply_to_user_id": None,
        "in_reply_to_status_id": None,
        "retweeted": False,
        "created_at": tweet.time,
        "text": tweet.text
    }

    source.insert(raw)

print(len(exacts))