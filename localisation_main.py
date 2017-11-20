from localisation_core import *

import json
from nltk.corpus import stopwords

stopWords = set(stopwords.words('english'))
print('Read unlocalised tweets')
nonloc_values = [Tweet(json.loads(line)["_id"]["$numberLong"],
                       json.loads(line)["text"],
                       json.loads(line)["created_at"],
                       stopWords)
                 for line
                 in tqdm(open("actual_data/nogeo.json"))
                 if json.loads(line)["lang"] == "en"
                 and json.loads(line)["in_reply_to_user_id"] == None
                 and json.loads(line)["in_reply_to_status_id"] == None
                 and json.loads(line)["retweeted"] == False]

print('Read bbox tweets')
bbox_values = [Tweet(json.loads(line)["_id"]["$numberLong"],
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

print("Data loaded. Number of nonloc is %d" % len(nonloc_values))
print("and number of bbox is %d" % len(bbox_values))

tweet_content = [value.text for value in tqdm(bbox_values + nonloc_values)]
# flatten the list of lists to 1d array
flatten_content = [item for sublist in tweet_content for item in sublist]
# remove duplicates
content_dict = {w: '' for w in flatten_content}
# enumerate without duplicates
content_enum = {w: idx for idx, w in enumerate(content_dict)}

print("Dictionary is generated. Number of words %d" % len(content_enum))

conjunction_matrix = np.zeros((len(bbox_values + nonloc_values), len(content_enum)), dtype=int)
d = dict()
for idx, tweet in enumerate(tqdm(bbox_values + nonloc_values)):
    d[tweet.id] = idx
    for w in tweet.text:
        conjunction_matrix[idx, content_enum[w]] += 1.

print("Matrix is calculated. Shape is", conjunction_matrix.shape)

#make a threshold for similarity
threshold = 0.9

new_col = localise_to_bbox(nonloc_values, bbox_values, threshold, conjunction_matrix, d)

print("We could recognize %f per cent tweets"%(len(new_col)*100.0/len(nonloc_values)))
