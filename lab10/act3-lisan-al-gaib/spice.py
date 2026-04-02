'''
Lab 7: ADVANCED PYTHON
Activity 1 : LISAN-AL-GAIB (Dune Reference)
Author : Sabyasachi Samantaray

Here we will be dealing only with 2D data to aid visualisation

In this activity, your aim will be the following.
1) Implement the kmeans algorithm completely and correctly.
2) Implement all TODOs without using any loops
'''

### TODO 1: Importing the necessary libraries - numpy, matplotlib and time
### This TODO is already done
import time # to time the execution
import numpy as np
import matplotlib.pyplot as plt
### TODO 1

### TODO 2
def load_data(data_path):
    return np.loadtxt(data_path, delimiter=',')

### TODO 3.1
def initialise_centers(data, K, init_centers=None):
    if init_centers is None:
        idx = np.random.choice(len(data), K, replace=False)
        return data[idx]
    return init_centers

### TODO 3.2
def initialise_labels(data):
    return np.zeros(len(data), dtype=int)

### TODO 4.1 : E step
def calculate_distances(data, centers):
    # (N,1,2) - (1,K,2) => (N,K,2) => (N,K)
    diff = data[:, np.newaxis, :] - centers[np.newaxis, :, :]
    return np.sqrt(np.sum(diff ** 2, axis=2))

### TODO 4.2 : E step
def update_labels(distances):
    return np.argmin(distances, axis=1)

### TODO 5 : M step
def update_centers(data, labels, K):
    mask = (labels[:, np.newaxis] == np.arange(K)[np.newaxis, :])  # (N,K)
    return (mask.T @ data) / mask.sum(axis=0)[:, np.newaxis]       # (K,2)

### TODO 6 : Check convergence
def check_termination(labels1, labels2):
    return np.array_equal(labels1, labels2)

### DON'T CHANGE ANYTHING IN THE FOLLOWING FUNCTION
def kmeans(data_path:str, K:int, init_centers):
    data = load_data(data_path)
    centers = initialise_centers(data, K, init_centers)
    labels = initialise_labels(data)
    start_time = time.time()
    while True:
        distances = calculate_distances(data, centers)
        labels_new = update_labels(distances)
        centers = update_centers(data, labels_new, K)
        if check_termination(labels, labels_new): break
        else: labels = labels_new
    end_time = time.time()
    return centers, labels, end_time - start_time

### FILL THE LINES BELOW THE TODO COMMENTS
def visualise(data_path, labels, centers):
    data = load_data(data_path)
    plt.scatter(data[:, 0], data[:, 1], c=labels, s=50, cmap='viridis')
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)

    ### TODO 7
    plt.title('K-means clustering')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig('kmeans.png')

    ## DO NOT CHANGE THE FOLLOWING LINE
    return plt
