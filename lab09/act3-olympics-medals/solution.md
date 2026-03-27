# Lab 09 — Activity 3: Olympics Medals (`main.py`)

## Problem Summary

Given a directory of files (one per Olympic year), each containing lines of `country-gold-silver-bronze`, aggregate the totals per country across all files and print them sorted.

**Command:** `python3 main.py --path data/testcase1/`

**Output:** A Python dict printed to stdout, e.g.:
```
{'usa': [128, 104, 105], 'china': [64, 49, 48], ...}
```

**Sort order:** Primary — gold medals descending. Ties — country name alphabetically ascending.

---

## Key Insight

Two things students commonly miss:

1. **Aggregation across files** — each directory has multiple year files; totals must be summed across all of them.
2. **Tie-breaking** — when two countries have the same gold count, sort alphabetically by name. Need a compound sort key.

---

## Core Approach

```python
# Aggregate
for fileName in os.listdir(args.path):
    with open(os.path.join(args.path, fileName)) as f:
        for line in f:
            country, gold, silver, bronze = line.strip().split('-')
            if country not in totalData:
                totalData[country] = [0, 0, 0]
            totalData[country][0] += int(gold)
            totalData[country][1] += int(silver)
            totalData[country][2] += int(bronze)

# Sort: gold desc, then name asc
sorted_data = dict(sorted(totalData.items(), key=lambda x: (-x[1][0], x[0])))
print(sorted_data)
```

---

## Testcase Breakdown

**Testcase 1** — 3 files (2008, 2012, 2016):

| Country | Gold | Silver | Bronze |
|---------|------|--------|--------|
| usa | 128 | 104 | 105 |
| china | 64 | 49 | 48 |
| russia | 39 | 37 | 48 |
| germany | 28 | 30 | 28 |
| japan | 28 | 30 | 46 |
| italy | 16 | 21 | 18 |
| australia | 14 | 15 | 17 |
| france | 11 | 11 | 13 |
| kenya | 6 | 4 | 6 |
| poland | 4 | 5 | 2 |
| romania | 4 | 1 | 4 |
| canada | 3 | 9 | 8 |
| india | 0 | 3 | 5 |
| vietnam | 0 | 0 | 1 |

Note ties: germany/japan (both 28 gold) → germany first alphabetically. poland/romania (both 4 gold) → poland first. india/vietnam (both 0 gold) → india first.

**Testcase 2** — 2 files (2020, 2024):

| Country | Gold | Silver | Bronze |
|---------|------|--------|--------|
| usa | 20 | 30 | 40 |
| china | 2 | 3 | 4 |
| india | 2 | 25 | 49 |
| japan | 2 | 60 | 73 |
| indonesia | 1 | 30 | 40 |

Note ties: china/india/japan (all 2 gold) → china < india < japan alphabetically.

---

## Common Student Mistakes

| Symptom | Likely Cause |
|---------|-------------|
| Missing countries or wrong totals | Only reading one file instead of all files in the directory |
| Wrong order for tied countries | Sorting by gold only, no alphabetical tie-break |
| Reversed tie-break order | Using `x[0]` descending instead of ascending for country name |
| `ValueError` on parse | Using `split('-')` but not stripping newlines first |
| Output format mismatch | Using `json.dumps` or custom formatting instead of `print(dict)` |
| `FileNotFoundError` | Using `fileName` directly instead of `os.path.join(args.path, fileName)` |

---

## Scoring

2 testcases × 1 mark = **2 marks total**. Exact string match required (autograder does `f1 == f2` line comparison).
