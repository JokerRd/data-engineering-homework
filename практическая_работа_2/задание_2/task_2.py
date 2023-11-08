import numpy as np
import os

data = np.load('task_2_matrix_51_2.npy')

data_size = len(data)
number_variant = 51
compare_value = 500 + number_variant

x = []
y = []
z = []

for i in range(0, data_size):
    for j in range(0, data_size):
        element = data[i][j]
        if element > compare_value:
            x.append(i)
            y.append(j)
            z.append(element)

np.savez('answer.npz', x=x, y=y, z=z)
np.savez_compressed('answer_compressed.npz', x=x, y=y, z=z)

answer_size = os.path.getsize('answer.npz')
answer_compressed_size = os.path.getsize('answer_compressed.npz')
print(answer_size)
print(answer_compressed_size)
