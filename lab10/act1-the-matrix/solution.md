# Lab 10 — Activity 1: The Matrix (`main.py`)

## Problem Summary

Implement three NumPy functions on a given 5×5 matrix.

| Task | Function | What it does |
|------|----------|-------------|
| 1 | `task1(matrix)` | Transpose of upper triangular matrix (incl. diagonal) |
| 2 | `task2(matrix)` | Mean, median, std (axis=0), determinant, inverse, pseudo-inverse |
| 3 | `task3(matrix, num, padding)` | Pad matrix with value `num`, border size `padding` |

---

## Task 1 — Upper Triangular Transpose

```python
return np.triu(matrix).T
```

`np.triu` zeroes out everything below the diagonal. `.T` transposes it.

**Common mistake:** Taking `np.tril(matrix).T` (lower triangular) instead.

---

## Task 2 — Stats + Linear Algebra

```python
mean    = np.mean(matrix, axis=0)
median  = np.median(matrix, axis=0)
std     = np.std(matrix, axis=0)
det     = np.around(np.linalg.det(matrix), 2)
pseudoinv = np.around(np.linalg.pinv(matrix), 2)
inv     = np.around(np.linalg.inv(matrix), 2) if det != 0 else pseudoinv
```

- All stats use `axis=0` (column-wise / along x-axis)
- Autograder checks mean/median with `np.array_equal` (exact) — do NOT round these
- std, det, inv, pinv are checked with `np.round(..., 2)` tolerance — safe to return raw values
- If `det == 0`: return pseudo-inverse for both `inv` and `pseudoinv`

**Common mistakes:**
- Using `axis=1` instead of `axis=0`
- Rounding mean/median (breaks exact equality check)
- Not handling the zero-determinant case

---

## Task 3 — Padding

```python
return np.pad(matrix, padding, constant_values=num)
```

`np.pad(arr, n, constant_values=v)` adds `n` rows/cols of value `v` on all 4 sides.

**Common mistakes:**
- Confusing argument order: it's `(matrix, padding, num)` in the call but `num` is the pad value
- Using `np.zeros` and manual slicing instead of `np.pad`

---

## Testcase Table

| Testid | What's checked | Pass condition |
|--------|---------------|----------------|
| 1 | task1 result | `np.array_equal` with expected |
| 2 | mean | exact `np.array_equal` |
| 3 | median | exact `np.array_equal` |
| 4 | std | `norm(round(std,2) - expected) < 1e-4` |
| 5 | det | `abs(round(det,2) - expected) < 1e-4` |
| 6 | inv | `norm(round(inv,2) - expected) < 1e-4` |
| 7 | pinv | `norm(round(pinv,2) - expected) < 1e-4` |
| 8 | task3(num=1, padding=2) | `np.array_equal` |

Total: **8 marks**

---

## Quick Debugging

| Symptom | Likely Cause |
|---------|-------------|
| Task 1 wrong shape | Using `.T` on wrong matrix, or forgetting `.T` |
| Mean/median fail despite correct values | Rounding output before returning |
| Det/inv precision errors | Not using `np.around(..., 2)` |
| Task 3 wrong border | Swapping `num` and `padding` arguments |
| Crash on singular matrix | Not checking `det != 0` before `np.linalg.inv` |
