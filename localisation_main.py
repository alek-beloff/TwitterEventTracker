from localisation_core import *
import sys

if len(sys.argv) > 1 and sys.argv[1] != 'testBB':
    exit('argument is incorrect')

if len(sys.argv) > 1 and sys.argv[1] == 'testBB':
    bbox_values = getBbox()
    print("and number of bbox is %d" % len(bbox_values))

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

if len(sys.argv) > 1 and sys.argv[1] == 'testBB':
    if len(sys.argv) > 2:
        qualityTesting(bbox_values, sys.argv[2], threshold=threshold, conjunction_matrix=conjunction_matrix, d=d)
    else:
        #default parameter
        qualityTesting(bbox_values, 10, threshold=threshold, conjunction_matrix=conjunction_matrix, d=d)

if len(sys.argv) == 1:
    new_col = localise_to_bbox(nonloc_values, bbox_values, threshold, conjunction_matrix, d)
    print("We could recognize %f per cent tweets" % (len(new_col) * 100.0 / len(nonloc_values)))