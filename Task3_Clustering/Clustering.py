import pandas as pd
import csv
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import random


def distance(x, y, x1, y1):
    dist = sqrt((y - y1) ** 2 + (x - x1) ** 2)
    return dist


data = pd.read_csv("test3.csv", index_col=0, delimiter=',')
n_clusters = 2


def get(v, st):
    while st[v] != -1:
        v = st[v]
    return v


def merge(v1, v2, st):
    v1 = get(v1, st)
    v2 = get(v2, st)
    if v1 != v2:
        st[v1] = v2
        return True
    return False


def simplify(v, st):
    vertices = []
    while st[v] != -1 and st[v] != v:
        vertices.append(v)
        v = st[v]
    for vertex in vertices:
        st[vertex] = v
    st[v] = v


def hierarchy_cluster(data, n_clusters):
    distances = []
    for j in range(len(data)):
        for k in range(j + 1, len(data)):
            distances.append([distance(data[j][0], data[j][1], data[k][0], data[k][1]), j, k])
    distances.sort()

    n = len(data)
    clusters = [-1 for i in range(n)]
    hist = []
    for element in distances:
        root_1 = get(element[1], clusters)
        root_2 = get(element[2], clusters)
        if merge(root_1, root_2, clusters):
            hist.append((root_1, root_2))

    for i in range(n_clusters - 1):
        v1, v2 = hist[-1 - i]
        clusters[v1] = -1

    for i in range(n):
        simplify(i, clusters)
    indixes = dict()
    i = 0
    for el in set(clusters):
        indixes[el] = i
        i += 1
    for i in range(len(clusters)):
        clusters[i] = indixes[clusters[i]]

    return clusters


def kmeans_cluster(data, centers, epochs=15):
    clusters = np.zeros(len(data))
    cnt_of_element = np.zeros(n_clusters)
    sum_of_element = [[0, 0] for i in range(n_clusters)]
    for m in range(epochs):
        for i in range(len(data)):
            for j in range(len(centers)):
                if j == 0:
                    min_dist = distance(data[i][0], data[i][1], centers[j][0], centers[j][1])
                    index_min_dist = 0

                if distance(data[i][0], data[i][1], centers[j][0], centers[j][1]) < min_dist:
                    index_min_dist = j
                    min_dist = distance(data[i][0], data[i][1], centers[j][0], centers[j][1])

            clusters[i] = index_min_dist
            sum_of_element[index_min_dist][0] += data[i][0]
            sum_of_element[index_min_dist][1] += data[i][1]
            cnt_of_element[index_min_dist] += 1
            if i % 100000 == 0:
                print("K-Means epoch", m, ":", i+1)
        for t in range(n_clusters):
            centers[t][0] = sum_of_element[t][0] / cnt_of_element[t]
            centers[t][1] = sum_of_element[t][1] / cnt_of_element[t]

    return clusters, centers


def get_centers(data, clusters):
    cnt = [0] * n_clusters
    centers = []
    for i in range(n_clusters):
        centers.append([0, 0])

    for i in range(len(clusters)):
        cnt[clusters[i]] += 1
        centers[clusters[i]][0] += data[i][0]
        centers[clusters[i]][1] += data[i][1]
    print(cnt)

    for i in range(n_clusters):
        centers[i][0] /= cnt[i]
        centers[i][1] /= cnt[i]
    return centers


eps = 5000
collisions = 0
n_test = 10
all_centers_of = []
for test in range(n_test):
    sample = data.sample(frac=0.0001).to_numpy()
    count_element_clusters = [0] * n_clusters
    clusters = hierarchy_cluster(sample, n_clusters)
    for i in range(len(sample)):
       scatter1 = plt.scatter(sample[i][0], sample[i][1], c='red' if clusters[i] == 0 else 'orange')
       if clusters[i] == 0:
           count_element_clusters[0] += 1
       else: count_element_clusters[1] += 1

    centers = get_centers(sample, clusters)
    scatter1 = plt.scatter(centers[0][0], centers[0][1], c='blue', label = u'Центр 1-ого кластера')
    scatter1 = plt.scatter(centers[1][0], centers[1][1], c='magenta', label = u'Центр 2-ого кластера')
    for elem in centers:
        all_centers_of.append(elem)
    close = False
    for j in range(len(centers)):
        for k in range(j + 1, len(centers)):
            print(distance(centers[j][0],centers[j][1],centers[k][0],centers[k][1]))
            if distance(centers[j][0], centers[j][1], centers[k][0], centers[k][1]) < eps:
                close = True

    if count_element_clusters[1]/len(clusters) > 0.8 or count_element_clusters[0]/len(clusters) > 0.8: close = True
    if close:
        collisions += 1
        print(collisions)
    print("#test", test, "passed")
    plt.legend()
    plt.show()

if collisions > 0.6 * n_test:
    print("Не разделяются")
    exit(0)

centers_centers = []
for i in range(n_clusters):
    centers_centers.append(all_centers_of[i+n_clusters*random.randint(0, n_test-1)])
big_eps = 1000
dist_of_centers = []
clusters, centers = kmeans_cluster(all_centers_of, centers_centers)
for i in range(len(centers)):
    for k in range(i+1,len(centers)):
        dist_of_centers.append(distance(centers[i][0],centers[i][1],centers[k][0],centers[k][1]))
while min(dist_of_centers) <= big_eps:
    centers_centers = []
    dist_of_centers = []
    for i in range(n_clusters):
        centers_centers.append(all_centers_of[i + n_clusters * random.randint(0, n_test - 1)])
    clusters, centers = kmeans_cluster(all_centers_of, centers_centers)
    for i in range(len(centers)):
        for k in range(i + 1, len(centers)):
            dist_of_centers.append(distance(centers[i][0], centers[i][1], centers[k][0], centers[k][1]))



#for i in range(len(all_centers_of)):
    #if clusters[i] == 0:
      #  scatter1 = plt.scatter(all_centers_of[i][0],all_centers_of[i][1], c='red')
    #elif clusters[i] == 1:
     #   scatter1 = plt.scatter(all_centers_of[i][0], all_centers_of[i][1], c='green')
    #else:
      #  scatter1 = plt.scatter(all_centers_of[i][0], all_centers_of[i][1], c='blue')
#plt.show()
vectors = data.to_numpy()

clusters = pd.DataFrame(kmeans_cluster(vectors, centers)[0])
data['cluster'] = clusters
data.to_csv('clusters2.csv', index=True, quoting=csv.QUOTE_ALL)
