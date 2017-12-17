from localisation_core import *
import sys

exact_values = getGeo()

exact = [value.text for value in exact_values]
# flatten the list of lists to 1d array
exact_flatten = [item for sublist in exact for item in sublist]
# remove duplicates
exact_dict = {w: '' for w in exact_flatten}
# enumerate without duplicates
exact_enum = {w: idx for idx, w in enumerate(exact_dict)}

exact_matrix = np.zeros((len(exact_values), len(exact_enum)), dtype=int)
d = dict()
for idx, tweet in enumerate(exact_values):
    d[tweet.id] = idx
    for w in tweet.text:
        exact_matrix[idx, exact_enum[w]] += 1

geoTesting(exact_values, sys.argv[1], threshold=0.9, alpha=0.5, conjunction_matrix=exact_matrix, d=d)
exit('testing is completed')