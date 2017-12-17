from localisation_core import *
import scipy.cluster.hierarchy as hcluster
from datetime import datetime
import matplotlib.pyplot as plt
import pytz
import folium
from folium.plugins import MarkerCluster

def totimestamp(dt, epoch=datetime(2017,9,9)):
    td = dt - epoch.replace(tzinfo=pytz.utc)
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / (2*10**11)

def getClusters(geo, place):
    tweet_content = [value.text for value in geo]
    # flatten the list of lists to 1d array
    flatten_content = [item for sublist in tweet_content for item in sublist]
    # remove duplicates
    content_dict = {w: '' for w in flatten_content}
    # enumerate without duplicates
    content_enum = {w: idx for idx, w in enumerate(content_dict)}

    conj_m = np.zeros((len(geo), len(content_enum)), dtype=int)
    d = dict()
    d_rev = dict()
    for idx, tweet in enumerate(geo):
        d[tweet.id] = idx
        d_rev[idx] = tweet.id
        for w in tweet.text:
            conj_m[idx, content_enum[w]] += 1.

    data = np.zeros((len(geo), 3), dtype=float)
    for idx, item in enumerate(geo):
        data[idx, :] = [item.coordinates[0], item.coordinates[1], totimestamp(item.time)]

    thresh = 0.005
    clusters = hcluster.fclusterdata(data, thresh, criterion="distance")

    clus = {}
    for idx,c in enumerate(clusters):
        if c not in clus:
            clus[c] = [idx]
        else:
            clus[c].append(idx)
    # detete clusters which have less than 3 items
    delQueue = []
    aliveQueue = []
    for c in clus:
        if len(clus[c]) < 3:
            delQueue.append(c)
        else:
            aliveQueue += clus[c]

    colours = []
    data2 = []
    for i in aliveQueue:
        colours.append(clusters[i])
        data2.append(data[i, 0:2])

    data2 = np.asarray(data2)
    if data2.shape == (0,):
        return

    for i in delQueue:
        del clus[i]

    # plotting
    plt.scatter(*np.transpose(data2[:, :]), c=colours)
    plt.axis("equal")
    title = "threshold: %f, number of clusters: %d, place: %s" % (thresh, len(set(colours)), geo[0].place)
    plt.title(title)
    plt.show()

    event_list = []

    for cluster in clus:
        lsh = lshash.LSHash(6, conj_m.shape[1])
        used_idx = []
        for item in clus[cluster]:
            lsh.index(conj_m[item], extra_data=d_rev[item])
        for item in clus[cluster]:
            event_candidate = []
            cs = lsh.query(conj_m[item], distance_func='cosine')
            for m in cs:
                if m[1]<0.3:
                    used_idx.append(m[0][1])
                    event_candidate.append(m[0][1])
            if len(event_candidate) > 2:
                event_list.append(event_candidate)

    uk = folium.Map(location=[geo[0].coordinates[1], geo[0].coordinates[0]], zoom_start=10, control_scale=True)


    for event in event_list:
        cluster = []
        cluster_title = []
        for messageId in event:
            for tweet in geo:
                if tweet.id == messageId:
                    cluster.append((tweet.text, tweet.time, tweet.user, [tweet.coordinates[1],tweet.coordinates[0]]))
        #for item in cluster:
        #    if len(cluster_title) == 0:
        #        cluster_title = set(item[0])
        #    else:
        #        cluster_title = cluster_title & set(item[0])
        #cluster_title = ','.join(list(cluster_title))
        marker_cluster = MarkerCluster().add_to(uk)
        for item in cluster:
            popup = ', '.join(item[0]) + str(item[1]) + str(item[2])
            folium.Marker(item[3], popup=popup).add_to(marker_cluster)

    uk.save("examples/"+place+"_event_clusters.html")




geo = getGeo()

geoCollection = {}

for item in geo:
    if item.place not in geoCollection:
        geoCollection[item.place] = [item]
    else:
        geoCollection[item.place].append(item)

for item in geoCollection:
    getClusters(geoCollection[item], geoCollection[item][0].place)


