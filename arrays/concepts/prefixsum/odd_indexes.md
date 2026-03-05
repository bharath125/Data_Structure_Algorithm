# 🔢 Prefix Sum of Odd-Indexed Elements — Range Query

> **Difficulty:** Beginner → Advanced
> **Topic:** Arrays · Prefix Sum · Range Queries · Index Parity
> **Language:** Python
> **Constraints:** 1 ≤ N, Q ≤ 10⁵ · −10⁵ ≤ A[i] ≤ 10⁵

---

## 📋 Problem Statement

You are given:
- An integer array **A** of size **N**
- A 2D query array **B** of size **Q**, each row `[L, R]` defines a range

**Goal:** For each query `[L, R]`, find the **sum of elements at odd indexes only** within that range.

```
Answer = A[L if L is odd] + ... + A[R if R is odd]
       = sum of A[i] where L ≤ i ≤ R AND i is ODD
```

---

## 🔑 First — What is an Odd Index?

An index `i` is **odd** when `i % 2 == 1` (not divisible by 2).

```
A  = [  2,   8,   3,   9,  15 ]
idx:   0    1    2    3    4
       EVEN ODD  EVEN ODD  EVEN
       ❌   ✅   ❌   ✅   ❌

Odd-indexed elements: A[1]=8, A[3]=9
```

> ⚠️ It's about the **position (index)**, NOT the value.
> A[1] = 8 is included because index 1 is odd.
> A[4] = 15 is excluded because index 4 is even — even though 15 is odd as a number!

---

## 🌍 Real-World Analogy — Before Any Code

### 🚌 Bus Seat Analogy

Imagine a bus with seats numbered **0 to N-1**. Each seat has a passenger with some weight.

```
Seat:     0     1     2     3     4
Weight: [ 2,    8,    3,    9,   15 ]
          A-side B-side A-side B-side A-side
```

- **Odd seats** (1, 3, 5, …) = B-side of the bus
- **Even seats** (0, 2, 4, …) = A-side of the bus

A query `[L, R]` asks:
> *"What is the total weight of all B-side passengers sitting between seats L and R?"*

Prefix sum lets you answer this in **O(1)** per query, no matter how many queries arrive.

---

## 🧩 Understanding the Examples

### Example 1: `A = [2, 8, 3, 9, 15]`

```
Index:  0    1    2    3    4
Value: [2,   8,   3,   9,  15]
       even  ODD  even ODD  even
              ✅         ✅
```

**Query 1: `[1, 4]`**
```
Range: indices 1, 2, 3, 4
Odd indices in range: 1, 3
Sum = A[1] + A[3] = 8 + 9 = 17 ✅
```

**Query 2: `[0, 2]`**
```
Range: indices 0, 1, 2
Odd indices in range: 1
Sum = A[1] = 8 ✅
```

**Query 3: `[2, 3]`**
```
Range: indices 2, 3
Odd indices in range: 3
Sum = A[3] = 9 ✅
```

---

### Example 2: `A = [5, 15, 25, 35, 45]`

```
Index:  0    1    2    3    4
Value: [5,  15,  25,  35,  45]
       even ODD  even ODD  even
```

**Query 1: `[2, 2]`**
```
Range: index 2 only
Index 2 is EVEN → no odd indexes in range
Sum = 0 ✅
```

**Query 2: `[2, 4]`**
```
Range: indices 2, 3, 4
Odd index in range: 3
Sum = A[3] = 35 ✅
```

---

## 💡 The Key Insight — Why Prefix Sum?

### Brute Force (Slow — O(N×Q))
For every query, loop through the range and add only odd-indexed elements:

```python
for L, R in B:
    total = 0
    for i in range(L, R+1):
        if i % 2 == 1:
            total += A[i]
    res.append(total)
```

This works but is **too slow** for N, Q = 10⁵ (10¹⁰ operations worst case).

### Prefix Sum Trick (Fast — O(N + Q))

**Pre-compute** a running total that only accumulates odd-indexed values.
Then answer any query in **O(1)** using subtraction.

---

## 🏗️ Building the Prefix Array — The Core Idea

We build a padded prefix array of size **N+1** where:

```
prefix[0]   = 0           (sentinel — nothing before index 0)
prefix[i+1] = prefix[i] + (A[i]  if  i is ODD  else  0)
```

At every position, we either:
- **Add A[i]** → if index `i` is odd ✅
- **Add 0** → if index `i` is even ❌ (skip it)

This gives us `prefix[i]` = *"sum of all odd-indexed elements from A[0] up to A[i-1]"*

---

## 📊 Building the Prefix Array — Full Trace

### Input: `A = [2, 8, 3, 9, 15]`

| Step | `i` | `A[i]` | `i` odd? | Value added | `prefix[i+1]` |
|:----:|:---:|:------:|:--------:|:-----------:|:-------------:|
| Init | —   | —      | —        | —           | prefix[0] = **0** |
| 1    | 0   | 2      | ❌ Even  | 0           | prefix[1] = **0** |
| 2    | 1   | 8      | ✅ Odd   | 8           | prefix[2] = **8** |
| 3    | 2   | 3      | ❌ Even  | 0           | prefix[3] = **8** |
| 4    | 3   | 9      | ✅ Odd   | 9           | prefix[4] = **17** |
| 5    | 4   | 15     | ❌ Even  | 0           | prefix[5] = **17** |

### ✅ Final Prefix Array

```
prefix = [0,  0,  8,  8,  17,  17]
          ↑   ↑   ↑   ↑    ↑    ↑
         p[0] p[1] p[2] p[3] p[4] p[5]
```

**Reading each value:**
```
prefix[1] = 0   → sum of odd-indexed elements in A[0..0]   → none
prefix[2] = 8   → sum of odd-indexed elements in A[0..1]   → A[1]=8
prefix[3] = 8   → sum of odd-indexed elements in A[0..2]   → A[1]=8
prefix[4] = 17  → sum of odd-indexed elements in A[0..3]   → A[1]+A[3]=8+9=17
prefix[5] = 17  → sum of odd-indexed elements in A[0..4]   → A[1]+A[3]=17
```

---

## 🧠 The Query Formula

Because `prefix[i]` = sum of odd-indexed elements from A[0] to A[i-1]:

```
Sum of odd-indexed elements in range [L, R]
    = prefix[R+1] - prefix[L]
```

**Why `R+1`?** Because `prefix[R+1]` covers up to and including `A[R]`.
**Why `prefix[L]`?** To subtract everything before index `L`.

### Visual Proof:

```
prefix[R+1] = odd-sum of A[0 .. R]
prefix[L]   = odd-sum of A[0 .. L-1]
              └────────────────────┘
                   this cancels out!

Difference  = odd-sum of A[L .. R]   ✅
```

### 🍕 Pizza Analogy:
```
prefix[R+1] = total odd-indexed slices from the start up to R
prefix[L]   = total odd-indexed slices from the start up to L-1

Subtract → only the slices between L and R remain ✅
```

---

## 🔍 The Code — Every Line Explained

```python
def solve(A, B):
    n = len(A)

    # ── Phase 1: Build prefix array of odd-index sums ──────────────────────
    prefix = [0] * (n + 1)      # size N+1, all zeros; prefix[0]=0 is the sentinel

    for i in range(n):
        if i % 2 == 1:          # index i is ODD → include A[i]
            prefix[i+1] = prefix[i] + A[i]
        else:                   # index i is EVEN → skip, carry forward
            prefix[i+1] = prefix[i]

    # Compact one-liner equivalent:
    # prefix[i+1] = prefix[i] + (A[i] if i % 2 == 1 else 0)

    # ── Phase 2: Answer each query in O(1) ─────────────────────────────────
    res = []
    for L, R in B:
        ans = prefix[R + 1] - prefix[L]   # core formula
        res.append(ans)

    return res
```

---

## 🔬 Query Traces — Example 1

**Prefix array:** `[0, 0, 8, 8, 17, 17]`

### Query 1: `[L=1, R=4]`
```
ans = prefix[4+1] - prefix[1]
    = prefix[5]   - prefix[1]
    = 17          - 0
    = 17 ✅

Odd indexes in [1,4]: index 1 (A[1]=8), index 3 (A[3]=9)  → 8+9=17 ✅
```

```
A:   [ 2,  [8,   3,   9,  15] ]
idx:   0    1    2    3    4
             ✅        ✅
              └── odd ──┘
```

---

### Query 2: `[L=0, R=2]`
```
ans = prefix[2+1] - prefix[0]
    = prefix[3]   - prefix[0]
    = 8           - 0
    = 8 ✅

Odd indexes in [0,2]: index 1 (A[1]=8)  → 8 ✅
```

```
A:   [ [2,   8,   3]  9,  15 ]
idx:    0    1    2   3    4
              ✅
```

---

### Query 3: `[L=2, R=3]`
```
ans = prefix[3+1] - prefix[2]
    = prefix[4]   - prefix[2]
    = 17          - 8
    = 9 ✅

Odd indexes in [2,3]: index 3 (A[3]=9)  → 9 ✅
```

```
A:   [ 2,   8,  [3,   9]  15 ]
idx:   0    1    2    3    4
                      ✅
```

---

### Final Output: `[17, 8, 9]` ✅

---

## 🔬 Query Traces — Example 2

**`A = [5, 15, 25, 35, 45]`**

Build prefix:

| `i` | `A[i]` | odd? | added | `prefix[i+1]` |
|:---:|:------:|:----:|:-----:|:-------------:|
| 0   | 5      | ❌   | 0     | 0             |
| 1   | 15     | ✅   | 15    | 15            |
| 2   | 25     | ❌   | 0     | 15            |
| 3   | 35     | ✅   | 35    | 50            |
| 4   | 45     | ❌   | 0     | 50            |

**Prefix:** `[0, 0, 15, 15, 50, 50]`

**Query 1: `[2, 2]`**
```
ans = prefix[3] - prefix[2] = 15 - 15 = 0 ✅
(index 2 is even, nothing to add)
```

**Query 2: `[2, 4]`**
```
ans = prefix[5] - prefix[2] = 50 - 15 = 35 ✅
(only index 3 is odd in range, A[3]=35)
```

**Output: `[0, 35]`** ✅

---

## ⏱️ Time & Space Complexity

| Phase              | Operation             | Complexity   |
|:-------------------|:----------------------|:------------:|
| Build prefix array | One pass over A       | **O(N)**     |
| Answer each query  | Single subtraction    | **O(1)**     |
| All Q queries      | Q × O(1)              | **O(Q)**     |
| **Total**          |                       | **O(N + Q)** |
| Space              | Extra array of size N+1 | **O(N)**   |

### Brute Force vs Prefix Sum at Scale

```
N = 100,000 elements · Q = 100,000 queries

Brute Force:   100,000 × 100,000 = 10,000,000,000 ops  😱  TLE
Prefix Sum:    100,000 + 100,000 =        200,000 ops  🚀  Instant
```

---

## 🗺️ Complete Visual Summary

```
ARRAY A:
┌────┬────┬────┬────┬────┐
│  2 │  8 │  3 │  9 │ 15 │
└────┴────┴────┴────┴────┘
  i=0  i=1  i=2  i=3  i=4
 EVEN  ODD  EVEN  ODD EVEN
  ❌   ✅    ❌   ✅    ❌

BUILDING PREFIX (size N+1):
┌────┬────┬────┬────┬────┬────┐
│  0 │  0 │  8 │  8 │ 17 │ 17 │
└────┴────┴────┴────┴────┴────┘
 p[0] p[1] p[2] p[3] p[4] p[5]
  ↑ sentinel

QUERY FORMULA:
  ans = prefix[R+1] - prefix[L]
            ↑               ↑
      covers up to R    subtracts everything before L

QUERIES:
  [1,4] → prefix[5] - prefix[1] = 17 -  0 = 17
  [0,2] → prefix[3] - prefix[0] =  8 -  0 =  8
  [2,3] → prefix[4] - prefix[2] = 17 -  8 =  9

OUTPUT: [17, 8, 9]
```

---

## ⚠️ Edge Cases & Pitfalls

### ❗ Pitfall 1: Using `prefix[R] - prefix[L-1]` Instead of `prefix[R+1] - prefix[L]`

This is the most common mistake. Two formulas look similar but work differently:

| Formula style | Prefix meaning | Query formula |
|:---|:---|:---|
| `prefix[i]` = sum of A[0..i] | Standard (no sentinel) | `prefix[R] - (prefix[L-1] if L>0 else 0)` → needs L==0 special case |
| `prefix[i+1]` = sum of A[0..i] | **Padded / Sentinel** | `prefix[R+1] - prefix[L]` → **always works, no special case** |

The padded approach (used here) is cleaner. The sentinel `prefix[0] = 0` eliminates the L==0 edge case entirely.

---

### ❗ Pitfall 2: Confusing Odd Index vs Odd Value

```python
A = [2, 8, 3, 9, 15]

# ❌ WRONG — checking if VALUE is odd
if A[i] % 2 == 1:   # 9, 3, 15 are odd values — NOT what we want

# ✅ CORRECT — checking if INDEX is odd
if i % 2 == 1:      # positions 1, 3 are odd indices — this is correct
```

---

### ❗ Pitfall 3: Off-by-One in Query

```python
# Query [L, R] is inclusive on both ends
# Correct:
ans = prefix[R + 1] - prefix[L]   # ✅ R+1 includes A[R]

# Wrong:
ans = prefix[R] - prefix[L]       # ❌ misses A[R]
```

---

### ❗ Pitfall 4: A range with no odd indexes

```
Query [2, 2] on A = [5, 15, 25, 35, 45]
→ only index 2, which is EVEN
→ prefix[3] - prefix[2] = 15 - 15 = 0

The formula handles this automatically — no special case needed. ✅
```

---

## 🧪 Test It Yourself

```python
def solve(A, B):
    n = len(A)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i+1] = prefix[i] + (A[i] if i % 2 == 1 else 0)
    return [prefix[R+1] - prefix[L] for L, R in B]


# Test cases
tests = [
    ([2, 8, 3, 9, 15],   [[1,4],[0,2],[2,3]],    [17, 8, 9]),
    ([5, 15, 25, 35, 45], [[2,2],[2,4]],          [0, 35]),
    ([1, 2, 3, 4, 5],    [[0,4]],                 [6]),     # A[1]+A[3]=2+4=6
    ([10],               [[0,0]],                 [0]),     # single element, even index
    ([10, 20],           [[0,1],[1,1]],            [20,20]), # A[1]=20
]

for A, B, expected in tests:
    result = solve(A, B)
    status = "✅" if result == expected else "❌"
    print(f"{status}  A={A}  B={B}")
    print(f"     got {result}, expected {expected}\n")
```

---

## 🔄 Variation — Even-Index Sum Instead

The same approach works for even-indexed elements — just flip the condition:

```python
# For ODD index sum:
prefix[i+1] = prefix[i] + (A[i] if i % 2 == 1 else 0)

# For EVEN index sum:
prefix[i+1] = prefix[i] + (A[i] if i % 2 == 0 else 0)
```

Same formula. Same query. Just one character changes.

---

## 📚 What to Learn Next

| Topic | What It Solves |
|:------|:---------------|
| **2D Prefix Sum** | Odd/even index sums in sub-rectangles of a matrix |
| **Difference Array** | Range updates efficiently |
| **Segment Tree** | Range queries with element updates |
| **BIT / Fenwick Tree** | Range sum with point updates in O(log N) |
| **Sparse Table** | Range min/max in O(1) |

---

> ✍️ **The Big Idea:**
> When a query only cares about a **subset** of elements (here, odd-indexed ones),
> build a prefix sum that **only accumulates that subset** — treating all other
> positions as zero. Then the standard range formula `prefix[R+1] - prefix[L]`
> works perfectly, delivering every answer in **O(1)** regardless of query count.

---

*Happy Coding! 🚀*
