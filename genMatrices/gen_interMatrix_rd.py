import numpy as np
from utils import * # type: ignore

n_min = 4
n_max = 27

val_min = 1
val_max = 1000
prob_0 = 0.5

sizes = [20]# range(n_min, n_max + 1)


def RandomMatrix (n, val_min, val_max, prob_0):

    F = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i+1, n):

            r = np.random.rand()

            if (r > prob_0):

                v = np.random.randint(val_min, val_max + 1)

                F[i,j] = v
                F[j,i] = v

    return F


for n in sizes:

    output_file_name = "rd_" + str(n) + ".csv"
    output_file_path = "../inter/" + output_file_name

    SaveMatrix_csv(RandomMatrix(n, val_min, val_max, prob_0), output_file_path)

    print("Generated", output_file_path)
