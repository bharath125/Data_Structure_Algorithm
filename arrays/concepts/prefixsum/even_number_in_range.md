# 🔢 Count of Even Numbers in a Range — Prefix Sum Approach

> **Difficulty:** Beginner → Intermediate
> **Topic:** Arrays · Prefix Sum · Range Queries · Even/Odd Detection
> **Language:** Python
> **Constraints:** 1 ≤ N, Q ≤ 10⁵ · 1 ≤ A[i] ≤ 10⁹

---

## 📋 Problem Statement

You are given:
- An integer array **A** of size **N**
- A 2D query array **B** of **Q** rows, each row `[L, R]` defines a range

**Goal:** For each query `[L, R]`, count how many elements in `A[L..R]` are **even numbers**.

```
Answer = count of values A[i] where L ≤ i ≤ R AND A[i] % 2 == 0
```

---

## 🌍 Real-World Analogy — Before Any Code

### 🚦 Traffic Counter on a Highway

Imagine cars passing through toll booths numbered **0 to N-1**.
Each car has a unique ID number.

- Cars with **even IDs** are commercial trucks (pay extra toll)
- Cars with **odd IDs** are regular cars (pay standard toll)

```
Booth:    0     1     2     3     4
Car ID: [ 1,    2,    3,    4,    5 ]
          odd  EVEN   odd  EVEN   odd
               🚛           🚛
```

A manager asks:
- *"How many trucks passed booths 0 to 2?"*
- *"How many trucks passed booths 2 to 4?"*
- *"How many trucks passed booths 1 to 4?"*

Checking one by one every time = slow. A **running counter** built once = instant answers.
That running counter is the **prefix sum of even counts**.

---

## 🧩 Understanding the Examples

### Example 1: `A = [1, 2, 3, 4, 5]`

```
Index:    0    1    2    3    4
Value:  [ 1,   2,   3,   4,   5 ]
          odd EVEN  odd EVEN  odd
               ✅        ✅
```

| Query `[L, R]` | Subarray       | Even elements | Count |
|:--------------:|:---------------|:-------------:|:-----:|
| `[0, 2]`       | [1, **2**, 3]  | 2             | **1** |
| `[2, 4]`       | [3, **4**, 5]  | 4             | **1** |
| `[1, 4]`       | [**2**, 3, **4**, 5] | 2, 4   | **2** |

**Output: `[1, 1, 2]`** ✅

---

### Example 2: `A = [2, 1, 8, 3, 9, 6]`

```
Index:    0    1    2    3    4    5
Value:  [ 2,   1,   8,   3,   9,   6 ]
         EVEN  odd EVEN  odd  odd EVEN
          ✅        ✅              ✅
```

| Query `[L, R]` | Subarray              | Even elements | Count |
|:--------------:|:----------------------|:-------------:|:-----:|
| `[0, 3]`       | [**2**, 1, **8**, 3]  | 2, 8          | **2** |
| `[3, 5]`       | [3, 9, **6**]         | 6             | **1** |
| `[1, 3]`       | [1, **8**, 3]         | 8             | **1** |
| `[2, 4]`       | [**8**, 3, 9]         | 8             | **1** |

**Output: `[2, 1, 1, 1]`** ✅

---

## 💡 The Key Insight — Count as a Sum

> Counting even numbers = **summing 1s and 0s**

Instead of storing the actual values, treat each element as:
- `1` if the element is **even**
- `0` if the element is **odd**

```
A         = [  1,   2,   3,   4,   5 ]
is_even   = [  0,   1,   0,   1,   0 ]   ← 1 for even, 0 for odd

Prefix sum of is_even:
  [  0,   1,   1,   2,   2 ]
```

Now "count of even numbers in range [L, R]" = sum of `is_even[L..R]` = standard prefix sum query!

This is the exact approach this code uses — it just builds the prefix directly without creating the `is_even` array separately.

---

## 🔍 Phase 1 — Building `even_prefix_sum`

```python
even_prefix_sum = []
total = 0

for i in range(len(A)):
    if A[i] % 2 == 0:          # Is A[i] even?
        total += 1              # Yes → increment count
        even_prefix_sum.append(total)
    else:                       # No → carry forward unchanged count
        even_prefix_sum.append(total)
```

### What Each Line Does

| Line | Purpose |
|:-----|:--------|
| `even_prefix_sum = []` | Empty list — will grow to size N |
| `total = 0` | Running count of even numbers seen so far |
| `if A[i] % 2 == 0` | Check if current element is even using modulo |
| `total += 1` | Found an even number — bump the counter |
| `even_prefix_sum.append(total)` | Store current running count at position i |

### What `even_prefix_sum[i]` means:

```
even_prefix_sum[i] = count of even numbers in A[0], A[1], ..., A[i]
                                               └──────── inclusive ─────────┘
```

At **even elements** → `total` grows, so the value stored increases.
At **odd elements** → `total` stays the same, so the value just copies forward.

> 💡 This is a **same-size prefix array** (not padded). `even_prefix_sum[i]`
> covers A[0] through A[i] **inclusive**, unlike a sentinel-padded array.

---

## 📊 Build Trace — Example 1: `A = [1, 2, 3, 4, 5]`

| Step | `i` | `A[i]` | Even? | Action          | `total` | `eps[i]` |
|:----:|:---:|:------:|:-----:|:----------------|:-------:|:--------:|
| 1    | 0   | 1      | ❌    | carry forward 0 | 0       | **0**    |
| 2    | 1   | 2      | ✅    | total = 0+1 = 1 | 1       | **1**    |
| 3    | 2   | 3      | ❌    | carry forward 1 | 1       | **1**    |
| 4    | 3   | 4      | ✅    | total = 1+1 = 2 | 2       | **2**    |
| 5    | 4   | 5      | ❌    | carry forward 2 | 2       | **2**    |

```
even_prefix_sum = [0, 1, 1, 2, 2]
                   ↑  ↑  ↑  ↑  ↑
                  i=0 i=1 i=2 i=3 i=4
```

**Reading each cell:**
```
eps[0] = 0 → 0 even numbers in A[0..0]   → {1}         → none
eps[1] = 1 → 1 even number  in A[0..1]   → {1,2}       → just 2
eps[2] = 1 → 1 even number  in A[0..2]   → {1,2,3}     → just 2
eps[3] = 2 → 2 even numbers in A[0..3]   → {1,2,3,4}   → 2 and 4
eps[4] = 2 → 2 even numbers in A[0..4]   → {1,2,3,4,5} → 2 and 4
```

---

## 📊 Build Trace — Example 2: `A = [2, 1, 8, 3, 9, 6]`

| Step | `i` | `A[i]` | Even? | Action          | `total` | `eps[i]` |
|:----:|:---:|:------:|:-----:|:----------------|:-------:|:--------:|
| 1    | 0   | 2      | ✅    | total = 0+1 = 1 | 1       | **1**    |
| 2    | 1   | 1      | ❌    | carry forward 1 | 1       | **1**    |
| 3    | 2   | 8      | ✅    | total = 1+1 = 2 | 2       | **2**    |
| 4    | 3   | 3      | ❌    | carry forward 2 | 2       | **2**    |
| 5    | 4   | 9      | ❌    | carry forward 2 | 2       | **2**    |
| 6    | 5   | 6      | ✅    | total = 2+1 = 3 | 3       | **3**    |

```
even_prefix_sum = [1, 1, 2, 2, 2, 3]
                   ↑  ↑  ↑  ↑  ↑  ↑
                  i=0 i=1 i=2 i=3 i=4 i=5
```

**Reading each cell:**
```
eps[0] = 1 → 1 even in A[0..0]   → {2}           → just 2
eps[1] = 1 → 1 even in A[0..1]   → {2,1}         → just 2
eps[2] = 2 → 2 evens in A[0..2]  → {2,1,8}       → 2 and 8
eps[3] = 2 → 2 evens in A[0..3]  → {2,1,8,3}     → 2 and 8
eps[4] = 2 → 2 evens in A[0..4]  → {2,1,8,3,9}   → 2 and 8
eps[5] = 3 → 3 evens in A[0..5]  → {2,1,8,3,9,6} → 2, 8 and 6
```

---

## 🔍 Phase 2 — Answering Queries

```python
res = []

for i in range(Q):
    L = B[i][0]            # Left boundary of query
    R = B[i][1]            # Right boundary of query
    tot = 0

    if L == 0:
        tot = even_prefix_sum[R]                       # Count from start → R
    else:
        tot = even_prefix_sum[R] - even_prefix_sum[L-1]  # Count from L → R

    res.append(tot)

return res
```

### The Query Formula

The logic is identical to any range prefix sum:

```
Count of evens in A[L..R]
    = (count of evens in A[0..R]) − (count of evens in A[0..L-1])
    = even_prefix_sum[R] − even_prefix_sum[L-1]
```

**Why `L-1`?** We want to subtract everything **before** L, not including L itself.

**Why `L == 0` is special?** When L=0, `even_prefix_sum[L-1]` = `even_prefix_sum[-1]`.
Python's `-1` index silently returns the **last element** — a wrong answer!
So we handle L=0 separately: the count is simply `even_prefix_sum[R]`.

---

## 🔬 Query Traces — Example 1

**`even_prefix_sum = [0, 1, 1, 2, 2]`**

### Query 1: `[L=0, R=2]`

```
L == 0 → special case:
  tot = even_prefix_sum[2] = 1

Subarray A[0..2] = [1, 2, 3]
Even numbers: {2} → count = 1 ✅

Visual:
  A:  [ [1,  2,  3]  4,  5 ]
         ↑            ↑
        L=0          L=0 so whole range from start
  eps[2] = 1 → answer ✅
```

---

### Query 2: `[L=2, R=4]`

```
L ≠ 0 → formula:
  tot = even_prefix_sum[4] - even_prefix_sum[1]
      = 2 - 1 = 1

Subarray A[2..4] = [3, 4, 5]
Even numbers: {4} → count = 1 ✅

What's happening:
  eps[4] = 2  → 2 evens in A[0..4] (which are 2 and 4)
  eps[1] = 1  → 1 even  in A[0..1] (which is just 2)
  Difference  → 1 even  in A[2..4] (which is just 4) ✅

Visual:
  A:  [ 1,  2, [3,  4,  5] ]
                ↑        ↑
               L=2      R=4
  eps[4] - eps[1] = 2 - 1 = 1 ✅
```

---

### Query 3: `[L=1, R=4]`

```
L ≠ 0 → formula:
  tot = even_prefix_sum[4] - even_prefix_sum[0]
      = 2 - 0 = 2

Subarray A[1..4] = [2, 3, 4, 5]
Even numbers: {2, 4} → count = 2 ✅

What's happening:
  eps[4] = 2  → 2 evens in A[0..4]
  eps[0] = 0  → 0 evens in A[0..0] (just A[0]=1, which is odd)
  Difference  → 2 evens in A[1..4] ✅

Visual:
  A:  [ 1, [2,  3,  4,  5] ]
            ↑            ↑
           L=1           R=4
  eps[4] - eps[0] = 2 - 0 = 2 ✅
```

---

## 🔬 Query Traces — Example 2

**`even_prefix_sum = [1, 1, 2, 2, 2, 3]`**

### Query 1: `[L=0, R=3]`

```
L == 0 → tot = even_prefix_sum[3] = 2
Subarray [2, 1, 8, 3] → evens: {2, 8} → 2 ✅
```

### Query 2: `[L=3, R=5]`

```
tot = even_prefix_sum[5] - even_prefix_sum[2]
    = 3 - 2 = 1
Subarray [3, 9, 6] → evens: {6} → 1 ✅
```

### Query 3: `[L=1, R=3]`

```
tot = even_prefix_sum[3] - even_prefix_sum[0]
    = 2 - 1 = 1
Subarray [1, 8, 3] → evens: {8} → 1 ✅
```

### Query 4: `[L=2, R=4]`

```
tot = even_prefix_sum[4] - even_prefix_sum[1]
    = 2 - 1 = 1
Subarray [8, 3, 9] → evens: {8} → 1 ✅
```

**Output: `[2, 1, 1, 1]`** ✅

---

## 🗺️ Complete Visual Summary

```
ARRAY A:
┌────┬────┬────┬────┬────┐
│  1 │  2 │  3 │  4 │  5 │
└────┴────┴────┴────┴────┘
  i=0  i=1  i=2  i=3  i=4
  odd EVEN  odd EVEN  odd
   ❌   ✅   ❌   ✅   ❌

TRANSFORM (is A[i] even?):
┌────┬────┬────┬────┬────┐
│  0 │  1 │  0 │  1 │  0 │
└────┴────┴────┴────┴────┘

BUILD even_prefix_sum (running count of evens):
  Start: total=0
  i=0: A[0]=1 odd  → carry 0   → eps=[0]
  i=1: A[1]=2 EVEN → total=1   → eps=[0,1]
  i=2: A[2]=3 odd  → carry 1   → eps=[0,1,1]
  i=3: A[3]=4 EVEN → total=2   → eps=[0,1,1,2]
  i=4: A[4]=5 odd  → carry 2   → eps=[0,1,1,2,2]

┌────┬────┬────┬────┬────┐
│  0 │  1 │  1 │  2 │  2 │
└────┴────┴────┴────┴────┘
 p[0] p[1] p[2] p[3] p[4]

QUERY FORMULA:
  L == 0  →  answer = eps[R]
  L  > 0  →  answer = eps[R] - eps[L-1]
                       ↑           ↑
               evens 0→R   minus  evens 0→(L-1)
               = evens in L→R  ✅

QUERIES:
  [0,2] → L==0 → eps[2]          =  1  →  1 even  ✅
  [2,4] → eps[4] - eps[1]  = 2-1 =  1  →  1 even  ✅
  [1,4] → eps[4] - eps[0]  = 2-0 =  2  →  2 evens ✅

OUTPUT: [1, 1, 2]
```

---

## ⏱️ Time & Space Complexity

| Phase               | Operation                  | Complexity   |
|:--------------------|:---------------------------|:------------:|
| Build prefix array  | One pass over A            | **O(N)**     |
| Answer each query   | One subtraction            | **O(1)**     |
| All Q queries       | Q × O(1)                   | **O(Q)**     |
| **Total Time**      |                            | **O(N + Q)** |
| **Space**           | One prefix array of size N | **O(N)**     |

### Scale Comparison

```
N = 100,000 elements · Q = 100,000 queries

Brute Force: loop each query range → O(N×Q) = 10,000,000,000 ops 😱
Prefix Sum:  build once, query fast → O(N+Q) =       200,000 ops 🚀
```

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: Confusing Even Value vs Even Index

This problem checks if the **value** `A[i]` is even — NOT whether the index `i` is even.

```python
# ✅ CORRECT — check the VALUE
if A[i] % 2 == 0:
    total += 1

# ❌ WRONG — checking the INDEX (different problem!)
if i % 2 == 0:
    total += 1
```

---

### ❗ Pitfall 2: The `L == 0` Silent Bug

When `L = 0`, `even_prefix_sum[L - 1]` = `even_prefix_sum[-1]`.
Python's negative indexing silently fetches the **last element** — no error, wrong answer!

```python
# ❌ WRONG — no guard (Python -1 index fires)
tot = even_prefix_sum[R] - even_prefix_sum[L - 1]
# When L=0: even_prefix_sum[-1] = last element ← WRONG!

# ✅ FIX A — if/else guard (this code's approach):
if L == 0:
    tot = even_prefix_sum[R]
else:
    tot = even_prefix_sum[R] - even_prefix_sum[L - 1]

# ✅ FIX B — padded sentinel approach (no special case needed):
padded = [0] + even_prefix_sum      # prepend a 0
tot = padded[R + 1] - padded[L]     # always works, even when L=0
```

---

### ❗ Pitfall 3: Large Values Still Work

`A[i]` can be up to **10⁹**. Even-checking with `% 2 == 0` works perfectly
regardless of value size — the modulo operation doesn't care how large the number is.

```python
A[i] = 1_000_000_000   # 10^9
A[i] % 2 == 0          # True — 10^9 is even ✅

A[i] = 999_999_999     # 10^9 - 1
A[i] % 2 == 0          # False — odd ✅
```

---

### ❗ Pitfall 4: Prefix Stores Count, Not Sum

This prefix array counts **how many** even numbers appear — not their sum.

```
A             = [2,  1,  8,  3,  9,  6]
even_prefix   = [1,  1,  2,  2,  2,  3]   ← count of evens seen so far
                 ↑               ↑
              1 even in       still 2 evens,
              A[0..0]         no new even at i=3,4
```

Don't confuse this with a prefix-sum-of-values. The query answer is a **count**, never a sum of A values.

---

## 🧪 Test It Yourself

```python
def solve(A, B):
    even_prefix_sum = []
    total = 0
    for i in range(len(A)):
        if A[i] % 2 == 0:
            total += 1
        even_prefix_sum.append(total)

    res = []
    for L, R in B:
        if L == 0:
            res.append(even_prefix_sum[R])
        else:
            res.append(even_prefix_sum[R] - even_prefix_sum[L - 1])
    return res


tests = [
    ([1, 2, 3, 4, 5],    [[0,2],[2,4],[1,4]],     [1, 1, 2]),
    ([2, 1, 8, 3, 9, 6], [[0,3],[3,5],[1,3],[2,4]], [2, 1, 1, 1]),
    ([2, 4, 6, 8],        [[0,3]],                  [4]),  # all even
    ([1, 3, 5, 7],        [[0,3]],                  [0]),  # all odd
    ([2],                 [[0,0]],                  [1]),  # single even
    ([1],                 [[0,0]],                  [0]),  # single odd
]

for A, B, expected in tests:
    result = solve(A, B)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  A={A}  B={B}  → {result}")
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Prefix Sum (basic)** | Exact same structure, just sums values instead of counting |
| **Count of odd numbers in range** | Flip condition: `A[i] % 2 != 0` |
| **Count of multiples of K in range** | Generalise: `A[i] % K == 0` |
| **2D Prefix Sum** | Count evens in a sub-rectangle of a matrix |
| **Segment Tree** | Handles updates (what if A[i] changes?) |
| **Binary Indexed Tree (BIT)** | Dynamic even count with point updates |

---

> ✍️ **The Big Idea:**
> Counting elements with a property (like "is even") across many range queries
> is solved by treating the property as a **0/1 value** and building a prefix sum
> of those 0s and 1s. The prefix sum at any position tells you how many "qualifying"
> elements exist from the start up to that point.
> Range count in O(1) = prefix[R] − prefix[L−1]. Pay once, answer forever.

---

*Happy Coding! 🚀*
