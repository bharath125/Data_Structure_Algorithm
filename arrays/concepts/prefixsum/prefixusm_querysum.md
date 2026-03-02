# 🧮 Prefix Sum — Range Query Sum

> **Difficulty:** Beginner → Advanced
> **Topic:** Arrays · Prefix Sums · Range Queries
> **Language:** Python
> **Constraints:** 1 ≤ N, M ≤ 10⁵ · 1 ≤ A[i] ≤ 10⁹ · 0 ≤ L ≤ R < N

---

## 📋 Problem Statement

You are given:
- An integer array **A** of length **N**
- A 2D array **B** of **M** queries, where each query is `[L, R]`

**Goal:** For every query `[L, R]`, find:

```
A[L] + A[L+1] + A[L+2] + ... + A[R-1] + A[R]
```

In plain English: *"What is the sum of all elements between index L and index R (inclusive)?"*

---

## 🎒 Real-World Analogy — Before Any Code

Imagine a **cashier's receipt** with daily sales amounts:

```
Day:     0    1    2    3    4    5    6    7    8    9
Sales: [ 7,   3,   1,   5,   5,   5,   1,   2,   4,   5 ]
```

Your manager asks:
- *"What were total sales from Day 6 to Day 9?"*
- *"What were total sales from Day 2 to Day 9?"*
- *"What were total sales from Day 2 to Day 4?"*
- *"What were total sales from Day 0 to Day 9?"*

You could add them up fresh every time (slow). Or prepare a **running total sheet** once and answer every question instantly. That running total sheet = **Prefix Sum Array**. 🚀

---

## 🏗️ Core Concepts

### What is an Index?

```
A = [ 7,  3,  1,  5,  5,  5,  1,  2,  4,  5 ]
      ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑
idx:  0   1   2   3   4   5   6   7   8   9
```

- `A[0]` = 7 · `A[3]` = 5 · `A[9]` = 5

### What is a Range Query `[L, R]`?

```
Query [2, 4]:  A[2] + A[3] + A[4] = 1 + 5 + 5 = 11
               └─ start              └─ end
```

### What is a Prefix Sum?

Prefix sum at index `i` = **sum of all elements from index 0 up to index i**.

```
prefix_sum[0] = A[0]                           = 7
prefix_sum[1] = A[0] + A[1]                    = 10
prefix_sum[2] = A[0] + A[1] + A[2]             = 11
prefix_sum[3] = A[0] + A[1] + A[2] + A[3]      = 16
... and so on
```

---

## 📊 Building the Prefix Sum — Full Trace

### Input
```python
A = [7, 3, 1, 5, 5, 5, 1, 2, 4, 5]
```

### Step-by-Step Table

| Index `i` | `A[i]` | Calculation       | `pre_sum` | `prefix_sum` so far              |
|:---------:|:------:|:------------------|:---------:|:---------------------------------|
| 0         | 7      | `0 + 7 = 7`       | 7         | [7]                              |
| 1         | 3      | `7 + 3 = 10`      | 10        | [7, 10]                          |
| 2         | 1      | `10 + 1 = 11`     | 11        | [7, 10, 11]                      |
| 3         | 5      | `11 + 5 = 16`     | 16        | [7, 10, 11, 16]                  |
| 4         | 5      | `16 + 5 = 21`     | 21        | [7, 10, 11, 16, 21]              |
| 5         | 5      | `21 + 5 = 26`     | 26        | [7, 10, 11, 16, 21, 26]          |
| 6         | 1      | `26 + 1 = 27`     | 27        | [7, 10, 11, 16, 21, 26, 27]      |
| 7         | 2      | `27 + 2 = 29`     | 29        | [..., 27, 29]                    |
| 8         | 4      | `29 + 4 = 33`     | 33        | [..., 29, 33]                    |
| 9         | 5      | `33 + 5 = 38`     | 38        | [..., 33, 38]                    |

### ✅ Final Prefix Sum Array

```python
prefix_sum = [7, 10, 11, 16, 21, 26, 27, 29, 33, 38]
#              ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑   ↑
#        idx:  0   1   2   3   4   5   6   7   8   9
```

**Reading each value:**

```
prefix_sum[0]  =  7   →  sum of A[0..0]
prefix_sum[4]  = 21   →  sum of A[0..4]  =  7+3+1+5+5
prefix_sum[9]  = 38   →  sum of A[0..9]  =  entire array
```

---

## 🔍 The Code — Every Line Explained

### Phase 1: Build the Prefix Sum Array

```python
A = [7, 3, 1, 5, 5, 5, 1, 2, 4, 5]
B = [[6,9], [2,9], [2,4], [0,9]]

prefix_sum = []   # Will hold our running totals
pre_sum = 0       # Accumulator starts at 0

for i in range(0, len(A)):      # i goes: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    pre_sum = pre_sum + A[i]    # Add current element to running total
    prefix_sum.append(pre_sum)  # Store the running total at index i

print(prefix_sum)
# [7, 10, 11, 16, 21, 26, 27, 29, 33, 38]
```

---

### Phase 2: Answer Queries

```python
Q = len(B)   # Q = 4
res = []     # Collect answers here

for i in range(Q):
    L = B[i][0]   # Left bound
    R = B[i][1]   # Right bound
    total = 0

    if (L == 0):
        total = prefix_sum[R]                    # Sum from 0 → R
    else:
        total = prefix_sum[R] - prefix_sum[L-1]  # Sum from L → R

    res.append(total)

print(res)
# [12, 28, 11, 38]
```

---

## 🧠 The Query Formula — The Real Magic

```
prefix_sum[R]     = A[0] + A[1] + ... + A[L-1] + A[L] + ... + A[R]
prefix_sum[L-1]   = A[0] + A[1] + ... + A[L-1]
                    └──────────────────────────┘
                          this part cancels out!

Result:
prefix_sum[R] - prefix_sum[L-1]  =  A[L] + A[L+1] + ... + A[R]  ✅
```

### 🍕 Pizza Slice Analogy

Imagine the prefix sum as a **pizza with 10 slices (0–9)**:

```
prefix_sum[9] = the ENTIRE pizza
prefix_sum[1] = only the first 2 slices (0 and 1)

Query [2, 9]:
  = prefix_sum[9] - prefix_sum[1]
  = entire pizza  - first 2 slices
  = slices 2 through 9  ✅
```

### 📏 Number Line Analogy

```
0─────7──────10──────11──────16──────21──────26──────27──────29──────33──────38
│     │       │       │       │       │       │       │       │       │       │
0     1       2       3       4       5       6       7       8       9
```

To get the "length" of segment [2, 5]:
- Total up to index 5: `prefix_sum[5] = 26`
- Total before index 2: `prefix_sum[1] = 10`
- Answer: `26 - 10 = 16` = A[2]+A[3]+A[4]+A[5] = 1+5+5+5 = 16 ✅

---

## 🔬 All Four Queries — Full Trace

### Query 1: `[6, 9]` → L=6, R=9

```
L ≠ 0, so:
  total = prefix_sum[9] - prefix_sum[5]
        = 38 - 26
        = 12

Check: A[6]+A[7]+A[8]+A[9] = 1+2+4+5 = 12 ✅
```

```
A:    [ 7,  3,  1,  5,  5,  5, [1,  2,  4,  5] ]
idx:    0   1   2   3   4   5   6   7   8   9
                                └──── range ────┘
```

---

### Query 2: `[2, 9]` → L=2, R=9

```
L ≠ 0, so:
  total = prefix_sum[9] - prefix_sum[1]
        = 38 - 10
        = 28

Check: A[2]+A[3]+...+A[9] = 1+5+5+5+1+2+4+5 = 28 ✅
```

```
A:    [ 7,  3, [1,  5,  5,  5,  1,  2,  4,  5] ]
idx:    0   1   2   3   4   5   6   7   8   9
                └───────────── range ───────────┘
```

---

### Query 3: `[2, 4]` → L=2, R=4

```
L ≠ 0, so:
  total = prefix_sum[4] - prefix_sum[1]
        = 21 - 10
        = 11

Check: A[2]+A[3]+A[4] = 1+5+5 = 11 ✅
```

```
A:    [ 7,  3, [1,  5,  5]  5,  1,  2,  4,  5  ]
idx:    0   1   2   3   4   5   6   7   8   9
                └── range ──┘
```

---

### Query 4: `[0, 9]` → L=0, R=9

```
L == 0, so:
  total = prefix_sum[9]
        = 38

Check: 7+3+1+5+5+5+1+2+4+5 = 38 ✅
```

```
A:    [ [7,  3,  1,  5,  5,  5,  1,  2,  4,  5] ]
idx:     0   1   2   3   4   5   6   7   8   9
         └───────────── entire array ────────────┘
```

---

### ✅ Final Output

```python
res = [12, 28, 11, 38]
```

---

## ⏱️ Time & Space Complexity

| Phase              | Operation          | Complexity   |
|:-------------------|:-------------------|:------------:|
| Build prefix sum   | One pass over A    | **O(N)**     |
| Answer each query  | Single subtraction | **O(1)**     |
| All M queries      | M × O(1)           | **O(M)**     |
| **Total**          |                    | **O(N + M)** |
| Space              | Extra array size N | **O(N)**     |

### Why This Matters at Scale

```
N = 100,000 elements · M = 100,000 queries

Brute Force:   100,000 × 100,000 = 10,000,000,000 ops  😱  (~10 seconds TLE)
Prefix Sum:    100,000 + 100,000 =        200,000 ops  🚀  (instant)
```

At the problem's max constraints (N, M = 10⁵), brute force **times out**. Prefix sum **breezes through**.

---

## ⚠️ Edge Cases & Common Pitfalls

### ❗ Pitfall 1: The `L == 0` Bug

When `L = 0`, `prefix_sum[L-1]` becomes `prefix_sum[-1]`.
In Python, `-1` index = **last element** of the array — silent wrong answer!

```python
# BUGGY:
total = prefix_sum[R] - prefix_sum[L - 1]   # prefix_sum[-1] = 38 ← WRONG!

# FIX A — if/else (used in this code):
if L == 0:
    total = prefix_sum[R]
else:
    total = prefix_sum[R] - prefix_sum[L - 1]

# FIX B — Sentinel/padding (cleaner, no special case ever):
padded = [0] + prefix_sum
total  = padded[R + 1] - padded[L]
```

Padded array:
```
padded = [0, 7, 10, 11, 16, 21, 26, 27, 29, 33, 38]
idx:      0  1   2   3   4   5   6   7   8   9  10
```
Now `L=0` → `padded[9+1] - padded[0]` = `38 - 0` = `38` ✅

---

### ❗ Pitfall 2: Integer Overflow (other languages)

```
Max prefix_sum = A[i]_max × N = 10⁹ × 10⁵ = 10¹⁴
```

- **Python** — safe, integers are unbounded
- **C++/Java** — must use `long long` / `long`, otherwise overflow!

---

### ❗ Pitfall 3: Query Validation

The constraints guarantee `0 ≤ L ≤ R < N`, but in production always guard:
```python
assert 0 <= L <= R < len(A), f"Invalid query [{L}, {R}]"
```

---

## 🗺️ Complete Visual Summary

```
INPUT ARRAY A:
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│  7 │  3 │  1 │  5 │  5 │  5 │  1 │  2 │  4 │  5 │
└────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
  i=0  i=1  i=2  i=3  i=4  i=5  i=6  i=7  i=8  i=9

PREFIX SUM ARRAY:
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│  7 │ 10 │ 11 │ 16 │ 21 │ 26 │ 27 │ 29 │ 33 │ 38 │
└────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
  i=0  i=1  i=2  i=3  i=4  i=5  i=6  i=7  i=8  i=9

QUERY FORMULA:
  L == 0  →  answer = prefix_sum[R]
  L  > 0  →  answer = prefix_sum[R] - prefix_sum[L-1]

QUERIES:
  [6, 9]  →  prefix_sum[9] - prefix_sum[5]  =  38 - 26  =  12
  [2, 9]  →  prefix_sum[9] - prefix_sum[1]  =  38 - 10  =  28
  [2, 4]  →  prefix_sum[4] - prefix_sum[1]  =  21 - 10  =  11
  [0, 9]  →  prefix_sum[9]                  =  38

OUTPUT:  [12, 28, 11, 38]
```

---

## 🧪 Test It Yourself

```python
A = [1, 4, 2, 8, 5, 7, 3]
B = [[0, 3], [1, 5], [3, 6], [0, 6]]

prefix_sum = []
pre_sum = 0
for x in A:
    pre_sum += x
    prefix_sum.append(pre_sum)
# prefix_sum → [1, 5, 7, 15, 20, 27, 30]

res = []
for L, R in B:
    if L == 0:
        res.append(prefix_sum[R])
    else:
        res.append(prefix_sum[R] - prefix_sum[L - 1])

print(res)
# Expected: [15, 26, 23, 30]
```

---

## 📚 What to Learn Next

| Topic                          | What It Solves                                      |
|:-------------------------------|:----------------------------------------------------|
| **2D Prefix Sum**              | Sum of any sub-rectangle in a matrix                |
| **Difference Array**           | Range update: add X to all elements L→R efficiently |
| **Segment Tree**               | Range queries AND point updates — O(log N) each     |
| **Binary Indexed Tree (BIT)**  | Range sum with updates — compact & fast             |
| **Sparse Table**               | Range min/max queries in O(1)                       |
| **Sliding Window**             | Fixed-size range problems without queries           |

---

> ✍️ **The Big Idea:**
> Prefix Sum is a **"pay once, use many times"** strategy.
> Spend **O(N)** once building the prefix array,
> then answer every range sum query in **O(1)** — no matter how many queries arrive.
> It is the cornerstone of range query algorithms and one of the first
> tools every competitive programmer reaches for.

---

*Happy Coding! 🚀*
