import numpy as np
import json

data = np.load('task_1_matrix_51.npy')

total_sum = np.sum(data)
total_avr = data.mean()
main_diagonal_sum = sum(np.diagonal(data))
main_diagonal_avr = np.diagonal(data).mean()
side_diagonal_sum = sum(np.fliplr(data).diagonal())
side_diagonal_avr = np.fliplr(data).diagonal().mean()
min_value = data.min()
max_value = data.max()

with open('task_1_answer.json', 'w') as f:
    json.dump({
        'sum': int(total_sum),
        'avr': total_avr,
        'sumMD': int(main_diagonal_sum),
        'avrMD': main_diagonal_avr,
        'sumSD': int(side_diagonal_sum),
        'avrSD': side_diagonal_avr,
        'max': int(max_value),
        'min': int(min_value)
    }, f)

normalized_data = data / total_sum

np.save('task_1_normalized_matrix.npy', normalized_data)

