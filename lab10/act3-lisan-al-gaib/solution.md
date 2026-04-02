# Lab 10 — Activity 3: Lisan-Al-Gaib / K-Means (`spice.py`)

## Problem Summary

Implement K-means clustering from scratch in `spice.py`. **No loops allowed** (except the `while True:` in the provided `kmeans()` function). All TODOs must use vectorized NumPy operations.

Grading: 17 marks across 10 testcases + 1 loop-check (penalty: -2 per extra loop).

---

## Key Insight: No Loops — Use Broadcasting

Every function that might seem to need a loop can be vectorized:

- **Distances**: `data[:, np.newaxis, :] - centers[np.newaxis, :, :]` gives an (N, K, 2) diff tensor in one shot
- **update_centers**: build a boolean mask `(labels[:, np.newaxis] == np.arange(K))` of shape (N, K), then `mask.T @ data` gives cluster sums in one matrix multiply

**Loop penalty**: The autograder counts every `for` and `while` in `spice.py`. The existing `while True:` in `kmeans()` accounts for 1. Any additional loop costs -2 marks each.

---

## Function Implementations

### `load_data(data_path)`
```python
return np.loadtxt(data_path, delimiter=',')  # → (N, 2)
```

### `initialise_centers(data, K, init_centers=None)`
```python
if init_centers is None:
    idx = np.random.choice(len(data), K, replace=False)
    return data[idx]
return init_centers
```
Note: must return **rows from `data`**, not random values. Autograder checks `center in data_sample`.

### `initialise_labels(data)`
```python
return np.zeros(len(data), dtype=int)  # all zeros (NOT ones — description is wrong, autograder checks 0)
```

### `calculate_distances(data, centers)` → shape (N, K)
```python
diff = data[:, np.newaxis, :] - centers[np.newaxis, :, :]  # (N, K, 2)
return np.sqrt(np.sum(diff ** 2, axis=2))
```

### `update_labels(distances)` → shape (N,)
```python
return np.argmin(distances, axis=1)
```

### `update_centers(data, labels, K)` → shape (K, 2)
```python
mask = (labels[:, np.newaxis] == np.arange(K)[np.newaxis, :])  # (N, K)
return (mask.T @ data) / mask.sum(axis=0)[:, np.newaxis]
```

### `check_termination(labels1, labels2)` → bool
```python
return np.array_equal(labels1, labels2)
```

### `visualise(data_path, labels, centers)` → plt
```python
data = load_data(data_path)
plt.scatter(data[:, 0], data[:, 1], c=labels, s=50, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
plt.title('K-means clustering')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('kmeans.png')
return plt
```

---

## Testcase Breakdown

| Testid | Function | Marks | Notes |
|--------|----------|-------|-------|
| 1 | load_data (sample1, 60 pts) | 1 | shape (60,2) |
| 2 | load_data (sample2, 120 pts) | 1 | shape (120,2) |
| 3 | initialise_centers (random) | 1 | centers must be from data |
| 4 | initialise_centers (provided) | 1 | exact match |
| 5 | initialise_labels | 1 | all zeros |
| 6 | calculate_distances | 2 | exact match within 1e-5 |
| 7 | update_labels | 2 | exact match |
| 8 | update_centers | 2 | exact match within 1e-5 |
| 9 | check_termination | 2 | True for equal, False for unequal |
| 10 | visualise (title/xlabel/ylabel/file) | 4 | exact strings, file must exist |
| 11 | Loop check | 0 (or -2n) | penalty if extra loops |

**Total: 17 marks**

---

## Common Student Mistakes

| Symptom | Likely Cause |
|---------|-------------|
| initialise_centers fails | Using `np.random.rand` instead of sampling from `data` |
| initialise_labels fails | Returning ones instead of zeros (description is wrong!) |
| calculate_distances wrong shape | Using `np.linalg.norm` with wrong axis |
| update_centers crashes | Division by zero if empty cluster (not tested but worth noting) |
| visualise fails title/label | Typo: `'K-Means'` vs `'K-means clustering'` (case sensitive) |
| visualise fails file check | Saving as `'plot.png'` instead of `'kmeans.png'` |
| Loop penalty | Using list comprehension with `for`, or explicit loop in update_centers |
