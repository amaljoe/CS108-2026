# Lab 09 — Activity 2: Complex & Polar Geometry (`main.py`)

## Problem Summary

Given `complex.py` (Complex class) and `polar.py` (Polar class), students must fill in `main.py` with 5 functions and import the classes correctly.

| Function | Input | Output |
|----------|-------|--------|
| `modulus(c)` | `Complex` | `√(x² + y²)` |
| `arg(c)` | `Complex` | `atan2(y, x)` (angle in radians) |
| `abscissa(p)` | `Polar` | `r · cos(θ)` (x-coordinate) |
| `ordinate(p)` | `Polar` | `r · sin(θ)` (y-coordinate) |
| `distance(z1, z2)` | two `Complex` | `modulus(z1 - z2)` |

All results are **rounded to 2 decimal places**.

---

## Critical: Import Statement

The autograder checks for `import Complex` and `import Polar` as substrings in `main.py`. Students must write:

```python
from complex import Complex
from polar import Polar
```

**If missing, the autograder exits early with 0 marks on all tests.**

---

## Provided Classes (read-only)

**`complex.py`** — `Complex(a, b)` stores `self.x = a`, `self.y = b`. Supports `+` and `-`.

**`polar.py`** — `Polar(a, b)` stores `self.r = a`, `self.t = b`. Supports `*` and `**`.

---

## Solution

```python
import math
from complex import Complex
from polar import Polar

def modulus(c: Complex):
    return round(math.sqrt(c.x**2 + c.y**2), 2)

def arg(c: Complex):
    return round(math.atan2(c.y, c.x), 2)

def abscissa(p: Polar):
    return round(p.r * math.cos(p.t), 2)

def ordinate(p: Polar):
    return round(p.r * math.sin(p.t), 2)

def distance(z1: Complex, z2: Complex):
    return modulus(z1 - z2)
```

---

## Testcase Breakdown

**modulus** (`sqrt(x²+y²)`):
| Input (x, y) | Expected |
|---|---|
| 3, 4 | 5.0 |
| 8, 15 | 17.0 |
| -9, -40 | 41.0 |
| 7.5, 10 | 12.5 |
| 5, -12 | 13.0 |
| -2, -0.1 | 2.0 |
| 0, 11 | 11.0 |
| 99, 99 | 140.01 |

**arg** (`atan2(y, x)` in radians):
| Input (x, y) | Expected |
|---|---|
| 3, 4 | 0.93 |
| 8, 15 | 1.08 |
| -9, -40 | -1.79 |
| 7.5, 10 | 0.93 |
| 5, -12 | -1.18 |
| -2, -0.1 | -3.09 |
| 0, 11 | 1.57 |
| 99, 99 | 0.79 |

**abscissa** (`r·cos(θ)`):
| Input (r, θ) | Expected |
|---|---|
| 5, 0.643 | 4.0 |
| 2, 1.571 | -0.0 |
| 6, -3.139 | -6.0 |
| 10, -1.11 | 4.45 |

**ordinate** (`r·sin(θ)`):
| Input (r, θ) | Expected |
|---|---|
| 5, 0.643 | 3.0 |
| 2, 1.571 | 2.0 |
| 6, -3.139 | -0.02 |
| 10, -1.11 | -8.96 |

**distance** (`modulus(z1 - z2)`):
| Input | Expected |
|---|---|
| (3,4) and (3,4) | 0.0 |
| (-5.5,7) and (0,-1) | 9.71 |

---

## Common Student Mistakes

| Symptom | Likely Cause |
|---------|-------------|
| All 0 marks, "Import Classes" failure | Missing `from complex import Complex` / `from polar import Polar` |
| `arg` wrong for negative quadrants | Using `math.atan(y/x)` instead of `math.atan2(y, x)` |
| `arg` gives `ZeroDivisionError` | Using `atan(y/x)` when x=0 (testcase: `0, 11`) |
| Off-by-small-amount errors | Not rounding to 2 decimal places |
| `distance` wrong | Not reusing `modulus()` — recalculating from scratch without `__sub__` |
| `abscissa`/`ordinate` attribute errors | Using `p.x`/`p.y` instead of `p.r`/`p.t` |
| `modulus`/`arg` attribute errors | Using `c.r`/`c.t` instead of `c.x`/`c.y` |

---

## Scoring

5 functions × 1 mark each = **5 marks total**. Each function is scored as `(passing testcases) / (total testcases)`.
