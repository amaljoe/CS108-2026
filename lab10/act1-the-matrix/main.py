'''
    NumPy and The Matrix
'''

import numpy as np

def task1(matrix):
    '''return the upper diagonal matrix in column-wise fashion'''
    return np.triu(matrix).T

def task2(matrix):
    '''return mean, median, std (precision 2), all along x, determinant, inverse, pseudo-inverse'''
    mean = np.mean(matrix, axis=0)
    median = np.median(matrix, axis=0)
    std = np.std(matrix, axis=0)
    det = np.around(np.linalg.det(matrix), 2)
    pseudoinv = np.around(np.linalg.pinv(matrix), 2)
    if det != 0:
        inv = np.around(np.linalg.inv(matrix), 2)
    else:
        inv = pseudoinv
    return mean, median, std, det, inv, pseudoinv

def task3(matrix, num=0, padding=3):
    '''return the padded matrix'''
    return np.pad(matrix, padding, constant_values=num)

if __name__ == '__main__':
    matrix = np.array([
        [5,5,84,3,9],
        [6,11,1,55,58],
        [1,20,48,12,36],
        [8,4,41,93,98],
        [6,17,64,0,13]
    ])
    print(task1(matrix))
    mean, median, std, det, inv, pseudoinv = task2(matrix)
    print("Mean: ", mean)
    print("Median: ", median)
    print("Std: ", std)
    print("Det: ", det)
    print("Inv: ", inv)
    print("Task3:", task3(matrix))
