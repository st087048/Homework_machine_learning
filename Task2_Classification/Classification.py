import matplotlib.pyplot as plt
import numpy as np
from random import randint
from sklearn.neighbors import KDTree
from math import fabs, sqrt


men = [randint(1,18) + 0.5, randint(1,18) + 0.5] # местоположение человека
scatter1 = plt.scatter(men[0], men[1], marker = '*', c = 'magenta', label = u'Жилище человека')
n_schools = int(input())
schools = []
for i in range(n_schools):
    schools.append([randint(1, 18) + 0.5, randint(1, 18) + 0.5])
    scatter1 = plt.scatter(schools[i][0], schools[i][1], c = 'green', marker = '.')
free_men = [[men[0] + 0.5, men[1] + 0.5]]
exit_schools = []
for i in range(n_schools):
    exit_schools.append([schools[i][0] + 0.5, schools[i][1] + 0.5]) # местоположение выходов
exit_schools = np.array(exit_schools)
free_men = np.array(free_men)

kdt = KDTree(exit_schools, leaf_size=30, metric='manhattan')
res = kdt.query(free_men, k=1, return_distance=False)
scatter1 = plt.scatter(schools[res[0][0]][0],schools[res[0][0]][1], marker = 's', c = 'blue', label = u'Подходящая школа')
plt.xticks(np.arange(0,21,1))
plt.yticks(np.arange(0,21,1))
exit_schools = exit_schools.tolist()
free_men = free_men.tolist()

dist = abs(exit_schools[res[0][0]][0] - free_men[0][0]) + abs(exit_schools[res[0][0]][1] - free_men[0][1]) + sqrt(2)
print(dist)
print(res[0][0])
plt.grid(alpha = 1)
plt.legend()
plt.show()
