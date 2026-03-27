# Lab 09 — Activity 5: Tower of Hanoi (`main.py`)

## Problem Summary

Given `n` (number of disks) as a CLI argument, print all moves to solve the Tower of Hanoi.

**Command:** `python3 main.py <n>`

**Output format:**
```
<number of moves>
<src> <dst>
<src> <dst>
...
```

Pegs are numbered 1 (source), 2 (auxiliary), 3 (destination).

**Example for n=2:**
```
3
1 2
1 3
2 3
```

---

## Key Insight

Standard recursive Hanoi. To move `n` disks from `src` to `dst` using `aux`:
1. Move top `n-1` disks from `src` → `aux` (using `dst` as aux)
2. Move bottom disk from `src` → `dst`
3. Move `n-1` disks from `aux` → `dst` (using `src` as aux)

Total moves = 2^n - 1.

---

## Solution

```python
import argparse
n = argparse.ArgumentParser()
n.add_argument("n", type=int)
args = n.parse_args()
n = args.n

moves = []

def hanoi(n, src, aux, dst):
    if n == 1:
        moves.append(f"{src} {dst}")
        return
    hanoi(n-1, src, dst, aux)
    moves.append(f"{src} {dst}")
    hanoi(n-1, aux, src, dst)

hanoi(n, 1, 2, 3)
print(len(moves))
for m in moves:
    print(m)
```

---

## Testcase Table

| n | Moves (2^n-1) | First move | Last move |
|---|--------------|------------|-----------|
| 1 | 1 | 1 3 | 1 3 |
| 2 | 3 | 1 2 | 2 3 |
| 3 | 7 | 1 3 | 1 3 |
| 4 | 15 | 1 2 | 2 3 |
| 16 | 65535 | 1 2 | 2 3 |

Pattern: odd n → first move is 1→3, even n → first move is 1→2.

---

## Common Student Mistakes

| Symptom | Likely Cause |
|---------|-------------|
| Wrong peg numbers | Swapping aux and dst in recursive calls |
| Moves in wrong order | Printing move before recursive calls instead of between them |
| Missing move count on line 1 | Forgetting to print `len(moves)` first |
| TLE on large n | Printing inside recursion with excessive I/O — collect in list first |
| RecursionError | Python default limit is 1000; n≤16 is fine (max depth=16) |
| Off-by-one move count | Recalculating as `2**n - 1` independently instead of just `len(moves)` |

---

## Scoring

16 testcases (n=1 to 16) × 1 mark = **16 marks total**. Compared with `diff -w` (whitespace-insensitive).
