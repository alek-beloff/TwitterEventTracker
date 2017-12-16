from scipy.optimize import minimize
from localisation_core import *

def newQualityTesting (x0):
    print(x0)
    threshold = x0[0]
    alpha = x0[1]
    bbox_values = getBbox()
    tweet_content = [value.text for value in tqdm(bbox_values)]
    # flatten the list of lists to 1d array
    flatten_content = [item for sublist in tweet_content for item in sublist]
    # remove duplicates
    content_dict = {w: '' for w in flatten_content}
    # enumerate without duplicates
    content_enum = {w: idx for idx, w in enumerate(content_dict)}
    print("Dictionary is generated. Number of words %d" % len(content_enum))

    conjunction_matrix = np.zeros((len(bbox_values), len(content_enum)), dtype=int)
    d = dict()
    for idx, tweet in enumerate(tqdm(bbox_values)):
        d[tweet.id] = idx
        for w in tweet.text:
            conjunction_matrix[idx, content_enum[w]] += 1.
    return -qualityTesting(bbox_values=bbox_values, number=15,
                           threshold=threshold, alpha=alpha,
                           conjunction_matrix=conjunction_matrix, d=d)

x0 = np.array([0.9,0.5])
res = minimize(newQualityTesting, x0, method='BFGS', options={'maxiter':10,'eps':0.2})#,
              # options={'xtol': 0.1, 'disp': True})
print(res.x)
#res1= minimize(geoTesting, x0, method='nelder-mead',
 #              options={'xtol': 1e-8, 'disp': True})