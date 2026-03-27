# Lab 09 — Activity 4: Casino Dice (`main.py`)

## Problem Summary

Given `n` as a command-line argument, count the number of **ordered sequences of dice rolls** (each die: 1–6) that sum to exactly `n`. Output the result mod 10^9+7.

**Command:** `python3 main.py <n>`

**Output:** A single integer.

---

## Key Insight

This is a classic **DP / ordered partition** problem: count the number of ways to write `n` as an ordered sum of integers from 1 to 6. It's equivalent to counting how many sequences of dice rolls (order matters) sum to `n`.

The recurrence:
```
dp[0] = 1   (empty sequence sums to 0)
dp[i] = dp[i-1] + dp[i-2] + dp[i-3] + dp[i-4] + dp[i-5] + dp[i-6]
```

This is a **generalised Fibonacci** over 6 terms, taken mod 10^9+7.

---

## Solution

```python
import sys

MOD = 10**9 + 7

n = int(sys.argv[1])
dp = [0] * (n + 1)
dp[0] = 1
for i in range(1, n + 1):
    for j in range(1, 7):
        if i - j >= 0:
            dp[i] = (dp[i] + dp[i-j]) % MOD
print(dp[n])
```

Time complexity: O(6n) — handles n=1,000,000 well within the 3-second timeout.

---

## Why It's Not 2^(n-1)

For n=1,2,3: the values 1, 2, 4 look like 2^(n-1), which matches compositions of n (parts ≥ 1). But dice are capped at 6, so for n≥7 the count diverges from 2^(n-1).

| n | 2^(n-1) | Dice DP |
|---|---------|---------|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 4 | 4 |
| 7 | 64 | 63 |
| 10 | 512 | **492** |

Students who guess `2**(n-1) % MOD` will pass the first 3 testcases and fail the rest.

---

## Testcase Table

| n | Expected output |
|---|----------------|
| 1 | 1 |
| 2 | 2 |
| 3 | 4 |
| 10 | 492 |
| 40 | 567401756 |
| 50 | 660641036 |
| 1000 | 937196411 |
| 654321 | 615247550 |
| 999998 | 39372206 |
| 1000000 | 874273980 |

---

## Common Student Mistakes

| Symptom | Likely Cause |
|---------|-------------|
| Passes n=1,2,3 but fails n=10+ | Using `2**(n-1) % MOD` (unlimited parts, not capped at 6) |
| Correct logic but TLE on large n | Using recursion without memoization |
| Wrong large outputs | Forgetting `% MOD` inside the loop (overflow in other langs, wrong in Python too since mod must be applied per step) |
| Off-by-one on small n | Initialising `dp[1]=1` instead of `dp[0]=1` |
| `IndexError` | Not checking `if i-j >= 0` before accessing `dp[i-j]` |

---

## Scoring

10 testcases × 1 mark = **10 marks total**. 3-second timeout per testcase.
