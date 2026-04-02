# Lab 10 — Activity 2: Distributions (`main.py`)

## Problem Summary

Sample 6 probability distributions (1,000,000 times each) using NumPy and plot their histograms in a 3×2 subplot figure. Save as `plot.png`.

---

## Key Insight

The autograder does **pixel-level image comparison** between your `plot.png` and a reference. With seed=42 and 1M samples, the histograms are stable enough to score 5/5. The exact seed matters less than getting the parameters right — but always set `np.random.seed(42)`.

Scoring thresholds (based on `abs(pixel_diff / total_pixels)`):
| Threshold | Score |
|-----------|-------|
| < 0.0015 | 5/5 |
| < 0.003 | 3/5 |
| < 0.005 | 2/5 |
| > 0.1 | -5 (penalised) |

---

## Distribution Parameters

| # | Distribution | Parameters | Multiply by | Bins |
|---|-------------|-----------|------------|------|
| 1 | Beta | a=4, b=20 | ×100 | `arange(-5, 51, 1)` |
| 2 | Exponential | scale=0.1 | ×100 | `arange(-1, 51, 1)` |
| 3 | Gamma | shape=2, scale=0.1 | ×100 | `arange(-1, 51, 1)` |
| 4 | Laplace | loc=0, scale=0.5 | ×100 | `arange(-1, 51, 1)` |
| 5 | Normal | loc=0, scale=3 | ×1 | `arange(-10, 12, 1)` |
| 6 | Poisson | lam=3 | ×1 | `arange(-1, 12, 1)` |

## Visual Styling

| # | Color | Alpha | Orientation |
|---|-------|-------|------------|
| 1 Beta | red | — | vertical (default) |
| 2 Exponential | green | 0.5 | vertical |
| 3 Gamma | black | 0.8 | **horizontal** |
| 4 Laplace | orange | — | vertical |
| 5 Normal | default | — | vertical |
| 6 Poisson | default | — | vertical |

---

## Solution

```python
import numpy as np
from matplotlib import pyplot as plt

np.random.seed(42)

beta_samples    = np.random.beta(a=4, b=20, size=1000000) * 100
exp_samples     = np.random.exponential(scale=0.1, size=1000000) * 100
gamma_samples   = np.random.gamma(shape=2, scale=0.1, size=1000000) * 100
laplace_samples = np.random.laplace(loc=0, scale=0.5, size=1000000) * 100
normal_samples  = np.random.normal(loc=0, scale=3, size=1000000)
poisson_samples = np.random.poisson(lam=3, size=1000000)

plt.subplot(3, 2, 1)
plt.hist(beta_samples, bins=np.arange(-5, 51, 1), color='red')
plt.title('Beta')

plt.subplot(3, 2, 2)
plt.hist(exp_samples, bins=np.arange(-1, 51, 1), color='green', alpha=0.5)
plt.title('Exponential')

plt.subplot(3, 2, 3)
plt.hist(gamma_samples, bins=np.arange(-1, 51, 1), color='black', alpha=0.8, orientation='horizontal')
plt.title('Gamma')

plt.subplot(3, 2, 4)
plt.hist(laplace_samples, bins=np.arange(-1, 51, 1), color='orange')
plt.title('Laplace')

plt.subplot(3, 2, 5)
plt.hist(normal_samples, bins=np.arange(-10, 12, 1))
plt.title('Normal')

plt.subplot(3, 2, 6)
plt.hist(poisson_samples, bins=np.arange(-1, 12, 1))
plt.title('Poisson')

plt.tight_layout()
plt.savefig('plot.png')
```

---

## Common Student Mistakes

| Symptom | Likely Cause |
|---------|-------------|
| -5 score (penalised) | Wrong distribution or completely wrong parameters |
| 2-3/5 instead of 5/5 | No seed / different seed; minor styling mismatch |
| Shape mismatch error | Different figure size or DPI |
| Gamma looks wrong | Missing `orientation='horizontal'` |
| Exponential wrong shape | Using `scale=1` instead of `scale=0.1` |
| Bins off | Using `range(a, b)` instead of `np.arange(a, b+1, 1)` |
| Normal not multiplied | Forgetting Normal is NOT multiplied by 100 |
