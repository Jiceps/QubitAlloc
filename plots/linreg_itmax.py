import matplotlib.pyplot as plt
import numpy as np


Metrics_names = ["mean",
                 "mean nonzero",
                 "median",
                 "sd",
                 "sd nonzero",
                 "coeff of variation",
                 "coeff of variation nonzero",
                 "gini coeff",
                 "sparsity",
                 "entropy",
                 "frobenius norm",
                 "conditioning number"]


input_file_path = "../genMatrices/data.txt"

Metrics = np.loadtxt(input_file_path, delimiter=' ')

n = np.size(Metrics, axis=1)

'''
mean     = Metrics[:,0]
mean_nnz = Metrics[:,1]
median   = Metrics[:,2]
sd       = Metrics[:,0]
sd_nnz   = Metrics[:,0]
cv       = Metrics[:,6]
cv_nnz   = Metrics[:,7]
gini     = Metrics[:,8]
sparsity = Metrics[:,9]
frob     = Metrics[:,10]
cond_num = Metrics[:,11]
'''

itmax_values = [4,
                5,
                5,
                2,
                4,
                5,
                6,
                2,
                4,
                3,
                5,
                5,
                1,
                5,
                5,
                4,
                5,
                4,
                1,
                11]


for i in range(n):

    plt.figure()
    plt.scatter(Metrics[:,i], itmax_values)
    plt.title(Metrics_names[i])


fig = plt.figure()
ax = fig.add_subplot(projection="3d")

ax.scatter(Metrics[:,0], Metrics[:,9], itmax_values)


plt.show()