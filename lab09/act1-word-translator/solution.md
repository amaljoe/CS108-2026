# Lab 09 — Word Translator (`language.py`)

## Problem Summary

Given a `translations.csv` file with rows of format `lang1,word1,lang2,word2`, implement a translator with 3 modes:

| Mode | Command | Output |
|------|---------|--------|
| 1 | `python3 language.py 1 <lang>` | All words in that language, reverse-sorted |
| 2 | `python3 language.py 2 <lang1> <lang2>` | All translation pairs, sorted by first element |
| 3 | `python3 language.py 3 <lang1> <lang2> <word>` | Translated word, or `UNK` |

Languages in dataset: `english`, `hindi`, `punjabi`

---

## Key Insight: Indirect Translations

The CSV only stores **direct** pairs (e.g. english↔punjabi, english↔hindi, hindi↔punjabi). But translations can be **transitive** — you may need to go through an intermediate language.

Examples:
- `god` (english) → `rab` (punjabi) → `bhagwan` (hindi)
- `pedh` (hindi) → `rukh` (punjabi) → `tree` (english)

**If a student only does direct lookups, they will fail ~2 testcases in Q2 and Q3.**

---

## Core Data Structure

Build a **bidirectional graph**: each node is `(language, word)`, edges connect translations.

```python
from collections import defaultdict
graph = defaultdict(list)  # (lang, word) -> [(lang, word)]

# For each CSV row: l1,w1,l2,w2
graph[(l1, w1)].append((l2, w2))
graph[(l2, w2)].append((l1, w1))   # bidirectional
```

---

## Mode 1 — List words in a language

Collect all nodes with matching language:

```python
words = sorted({w for (l, w) in graph if l == lang}, reverse=True)
print(words)
```

**Common mistake:** forgetting `reverse=True` → wrong order.

---

## Mode 2 — Find all translation pairs

For every word in `lang1`, BFS to find its translation in `lang2`:

```python
pairs = set()
for word in {w for (l, w) in graph if l == lang1}:
    trans = bfs_translate(graph, lang1, word, lang2)
    if trans:
        pairs.add((word, trans))
print(sorted(pairs))
```

**Common mistakes:**
- Only doing direct lookup (misses transitive pairs like `god→bhagwan`)
- Not deduplicating (CSV has duplicate entries like `brother↔bhai` appearing twice)
- Wrong sort order (should sort ascending by first element)

---

## Mode 3 — Translate a single word

BFS from `(lang1, word)` until a node with `lang2` is found:

```python
def find_translation(graph, lang1, word, lang2):
    start = (lang1, word)
    if start not in graph:
        return None
    visited = {start}
    queue = deque([start])
    while queue:
        curr = queue.popleft()
        for neighbor in graph[curr]:
            if neighbor[0] == lang2:
                return neighbor[1]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return None
```

Return `UNK` if no path found.

**Common mistakes:**
- Not handling unknown words (`mundaa` → `UNK`, not a KeyError)
- Doing direct dict lookup instead of BFS (misses transitive cases)
- Printing `None` instead of `UNK`

---

## CSV Parsing Notes

- Each row: `lang1,word1,lang2,word2` (no header)
- Some pairs appear **twice** in different directions — use a `set` to deduplicate
- Strip whitespace from values just in case

```python
import csv
with open('translations.csv') as f:
    for row in csv.reader(f):
        l1, w1, l2, w2 = [x.strip() for x in row]
```

---

## Testcase Breakdown

| Test | Command | Expected |
|------|---------|----------|
| q1_1 | `language.py 1 english` | `['water', 'tree', 'sister', 'mother', 'love', 'god', 'brother']` |
| q1_2 | `language.py 1 hindi` | `['sundar', 'pita', 'pedh', 'paani', 'maa', 'ladki', 'bhai', 'bhagwan']` |
| q1_3 | `language.py 1 punjabi` | `['soni', 'rukh', 'rab', 'pyar', 'piyo', 'kudi', 'bhra', 'bhain']` |
| q2_1 | `language.py 2 hindi english` | `[('bhagwan', 'god'), ('bhai', 'brother'), ('maa', 'mother'), ('paani', 'water'), ('pedh', 'tree')]` |
| q2_2 | `language.py 2 english hindi` | `[('brother', 'bhai'), ('god', 'bhagwan'), ('mother', 'maa'), ('tree', 'pedh'), ('water', 'paani')]` |
| q2_3 | `language.py 2 english punjabi` | `[('brother', 'bhra'), ('god', 'rab'), ('love', 'pyar'), ('sister', 'bhain'), ('tree', 'rukh')]` |
| q2_4 | `language.py 2 hindi punjabi` | `[('bhagwan', 'rab'), ('bhai', 'bhra'), ('ladki', 'kudi'), ('pedh', 'rukh'), ('pita', 'piyo'), ('sundar', 'soni')]` |
| q3_1 | `language.py 3 punjabi hindi kudi` | `ladki` |
| q3_2 | `language.py 3 hindi punjabi bhai` | `bhra` |
| q3_3 | `language.py 3 english hindi god` | `bhagwan` (transitive via punjabi) |
| q3_4 | `language.py 3 hindi english pedh` | `tree` (transitive via punjabi) |
| q3_5 | `language.py 3 punjabi hindi mundaa` | `UNK` |

---

## Quick Debugging Help for Students

| Symptom | Likely cause |
|---------|-------------|
| Q2 missing 2 pairs | Direct lookup only, not BFS |
| Q3 returning `None` | Forgot to print `UNK` for unknown words |
| Q1 wrong order | Missing `reverse=True` in sort |
| KeyError on unknown word | Not checking `if start not in graph` before BFS |
| Duplicate pairs in Q2 output | Not using a `set` to collect results |
