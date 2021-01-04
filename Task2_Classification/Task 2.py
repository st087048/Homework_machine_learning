from sklearn.neighbors import NearestNeighbors
import numpy as np
import random
from sklearn.neighbors import KDTree
schools = []
side = 30
n_schools = 3
for i in range(n_schools):
    schools.append([random.randint(0, 3*side), random.randint(0, 3*side)])
body = [3,1]
y = np.array([[100,8]])

schools = np.array(schools).reshape(-1,1)
X = np.array([[20, 5], [15, 7], [3, 21], [10, 1], [100, 7], [3, 2]])
kdt = KDTree(X, leaf_size=30, metric='manhattan')
print(kdt.query(y, k=1, return_distance=False))