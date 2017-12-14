from localisation_core import *
import sys

if len(sys.argv) > 1 and sys.argv[1].lower() not in ['testbb', 'testgeo', 'minimizebb'] :
    exit('argument is incorrect')

nonloc_values = []
if len(sys.argv) == 1:
    nonloc_values = getUnloc()
print("Data loaded. Number of nonloc is %d" % len(nonloc_values))
bbox_values = getBbox()
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

if len(sys.argv) > 2 and sys.argv[1].lower() == 'testbb':
    qualityTesting(bbox_values, sys.argv[2], threshold=threshold, alpha = 0.5, conjunction_matrix=conjunction_matrix, d=d)
    exit('testing is completed')

exact_values = getGeo()

new_col = []
if len(sys.argv) == 1:
    new_col = localise_to_bbox(nonloc_values[:100], bbox_values, threshold, conjunction_matrix, d)
    print("We could recognize %f per cent tweets" % (len(new_col) * 100.0 / len(nonloc_values)))

#join recognised values to bbox
bbox_values += new_col

exact = [value.text for value in exact_values + bbox_values]
# flatten the list of lists to 1d array
exact_flatten = [item for sublist in exact for item in sublist]
# remove duplicates
exact_dict = {w: '' for w in exact_flatten}
# enumerate without duplicates
exact_enum = {w: idx for idx, w in enumerate(exact_dict)}

exact_matrix = np.zeros((len(exact_values + bbox_values), len(exact_enum)), dtype=int)
d = dict()
for idx, tweet in enumerate(exact_values + bbox_values):
    d[tweet.id] = idx
    for w in tweet.text:
        exact_matrix[idx, exact_enum[w]] += 1

if len(sys.argv) > 2 and sys.argv[1].lower() == 'testgeo':
    geoTesting(exact_values, sys.argv[2], threshold=threshold, conjunction_matrix=exact_matrix, d=d)
    exit('testing is completed')

exacts = localise_to_geo(bbox_values, exact_values, threshold, exact_matrix, d)
print(len(exacts))