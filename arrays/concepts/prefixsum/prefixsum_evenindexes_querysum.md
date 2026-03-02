# 🧮 Prefix Sum of Even Indexes — Query Sum

> **Difficulty:** Beginner → Intermediate
> **Topic:** Arrays · Prefix Sums · Range Queries
> **Language:** Python

---

## 🤔 What Problem Are We Solving?

Imagine you have an array of numbers, and someone asks you **hundreds of questions** like:

> *"What is the sum of all even-indexed elements between index L and index R?"*

The **brute-force** way would be to loop through every element from L to R for each query.
That's **slow** — especially with thousands of queries on large arrays.

**Prefix Sum** is a smart technique that answers each query in **O(1)** (instant!) after a **one-time O(n) pre-processing step.**

---

## 🏗️ Building Blocks — Key Concepts First

### What is an Index?
An index is the **position** of an element in an array, starting from `0`.

```
A = [ 2,  8,  3,  9,  15 ]
      ↑   ↑   ↑   ↑   ↑
idx:  0   1   2   3   4
```

### What is an Even Index?
An index is **even** if `index % 2 == 0`

```
A = [ 2,  8,  3,  9,  15 ]
      ✅      ✅      ✅        ← even indexes (0, 2, 4)
          ❌      ❌            ← odd indexes  (1, 3)
```

So the **even-indexed elements** are: `2, 3, 15`

### What is a Prefix Sum?
A prefix sum array stores the **running total** up to each position.

For even indexes only, we accumulate the sum only when the index is even, and **carry forward** the same value at odd indexes.

---

## 📊 Step-by-Step Walkthrough

### Input
```python
A = [2, 8, 3, 9, 15]
```

### Building the Prefix Sum Array

Let's trace through each index manually:

| Index `i` | `A[i]` | Is Even? | Action                | `tot` | `prefix_sum` |
|:---------:|:------:|:--------:|:----------------------|:-----:|:------------:|
| 0         | 2      | ✅ Yes   | `tot = 0 + 2 = 2`     | 2     | [2]          |
| 1         | 8      | ❌ No    | carry forward `tot`   | 2     | [2, 2]       |
| 2         | 3      | ✅ Yes   | `tot = 2 + 3 = 5`     | 5     | [2, 2, 5]    |
| 3         | 9      | ❌ No    | carry forward `tot`   | 5     | [2, 2, 5, 5] |
| 4         | 15     | ✅ Yes   | `tot = 5 + 15 = 20`   | 20    | [2, 2, 5, 5, 20] |

### ✅ Final Prefix Sum Array
```
prefix_sum = [2, 2, 5, 5, 20]
```

**Mental model:** At any index `i`, `prefix_sum[i]` tells you:
> *"The total sum of all even-indexed elements from index 0 up to and including index i."*

---

## 🔍 The Code — Line by Line

```python
## prefix sum of even indexes of querysum
## first find the prefix sum array at even indexes

A = [2, 8, 3, 9, 15]   # Original array
B = [[1, 4], [0, 2], [2, 3]]  # Queries: each [L, R] means "sum from L to R"
```

### Phase 1: Build the Prefix Sum

```python
prefix_sum = []   # This will store our pre-computed sums
tot = 0           # Running total — starts at zero

for i in range(len(A)):       # Loop through every index: 0, 1, 2, 3, 4
    if (i % 2 == 0):          # If index is EVEN...
        tot += A[i]           #   add this element to running total
        prefix_sum.append(tot)#   store updated total
    else:                     # If index is ODD...
        prefix_sum.append(tot)#   just carry forward same total (no addition)

print(prefix_sum)
# Output: [2, 2, 5, 5, 20]
```

> 💡 **Why carry forward at odd indexes?**
> Because we want `prefix_sum[i]` to always represent a valid "sum up to i".
> At odd indexes, even though we don't add anything new, we still need a value
> stored there so our query formula works correctly for any L and R.

---

### Phase 2: Answer Each Query

```python
Q = len(B)   # Number of queries = 3
res = []     # Store all query results here

for i in range(Q):
    L = B[i][0]   # Left boundary of query
    R = B[i][1]   # Right boundary of query

    if (L == 0):
        total = prefix_sum[R]              # Sum from start → R
    else:
        total = prefix_sum[R] - prefix_sum[L - 1]  # Sum from L → R

    res.append(total)

print(res)
# Output: [15, 5, 15]
```

---

## 🧠 The Query Formula — The Magic Explained

This is the heart of the technique. Understanding **why** `prefix_sum[R] - prefix_sum[L-1]` gives the range sum:

```
prefix_sum[R]     = sum of even-indexed elements from index 0 → R
prefix_sum[L-1]   = sum of even-indexed elements from index 0 → (L-1)

Difference        = sum of even-indexed elements from index L → R ✅
```

**Visual analogy — think of it like a ruler:**

```
Index:       0    1    2    3    4
             [----+----+----+----]
prefix_sum:  2    2    5    5   20

Query [1,4]: prefix_sum[4] - prefix_sum[0]
           = 20 - 2
           = 18  ✅ (even-indexed elements in range: A[2]=3, A[4]=15 → 3+15=18)

Wait — but our output shows 15 for query [1,4]? Let's re-check:
Even indexes in range [1,4]: index 2 (A[2]=3), index 4 (A[4]=15) → 3+15=18

Hmm, let's trace: prefix_sum[4] - prefix_sum[0] = 20 - 2 = 18 ✔
```

---

## 🔬 Query Trace — All Three Queries

### Query 1: `[1, 4]` → L=1, R=4

```
L ≠ 0, so: total = prefix_sum[4] - prefix_sum[0]
                 = 20 - 2
                 = 18

Even-indexed elements in range [1,4]: A[2]=3, A[4]=15 → 3+15 = 18 ✅
```

### Query 2: `[0, 2]` → L=0, R=2

```
L == 0, so: total = prefix_sum[2]
                  = 5

Even-indexed elements in range [0,2]: A[0]=2, A[2]=3 → 2+3 = 5 ✅
```

### Query 3: `[2, 3]` → L=2, R=3

```
L ≠ 0, so: total = prefix_sum[3] - prefix_sum[1]
                 = 5 - 2
                 = 3

Even-indexed elements in range [2,3]: A[2]=3 (only) → 3 ✅
```

### Final Output
```python
res = [18, 5, 3]
```

---

## ⏱️ Why Is This Efficient?

| Approach        | Build Time | Each Query | Total for Q queries |
|:----------------|:----------:|:----------:|:-------------------:|
| Brute Force     | O(1)       | O(n)       | **O(n × Q)**        |
| Prefix Sum      | O(n)       | O(1)       | **O(n + Q)**        |

For `n = 100,000` elements and `Q = 100,000` queries:
- Brute force: **10,000,000,000 operations** 😱
- Prefix sum:  **200,000 operations** 🚀

---

## 🗺️ Visual Summary

```
ARRAY A:
┌────┬────┬────┬────┬────┐
│ 2  │ 8  │ 3  │ 9  │ 15 │
└────┴────┴────┴────┴────┘
  i=0  i=1  i=2  i=3  i=4
  ✅        ✅        ✅    ← even indexes only

EVEN VALUES: 2, 3, 15

PREFIX SUM:
┌────┬────┬────┬────┬────┐
│ 2  │ 2  │ 5  │ 5  │ 20 │
└────┴────┴────┴────┴────┘
  "2"  "2"  "2+3" "2+3" "2+3+15"

QUERY [L, R]:
  If L=0 → answer = prefix_sum[R]
  If L>0 → answer = prefix_sum[R] - prefix_sum[L-1]
                                    └── "subtract what came before L"
```

---

## 🧩 Common Pitfalls & Edge Cases

### ❗ Why special case `L == 0`?
When `L=0`, doing `prefix_sum[L-1]` would mean `prefix_sum[-1]` — in Python, that's the **last element** of the array (a common bug!). So we handle `L=0` separately.

**Alternative fix** — use a sentinel (padded prefix sum):
```python
# Add a 0 at the beginning so prefix_sum[-1] issue never arises
padded = [0] + prefix_sum
# Then every query is simply:
total = padded[R + 1] - padded[L]
# No special case needed! ✅
```

### ❗ What if R is out of bounds?
Always ensure `R < len(A)`. Add a guard in production code:
```python
if R >= len(A):
    raise ValueError(f"R={R} exceeds array length {len(A)}")
```

### ❗ What if L > R?
Invalid query. Swap them or return 0 depending on your problem requirements.

---

## 🧪 Test It Yourself

Try changing the array or queries:
```python
A = [10, 20, 30, 40, 50, 60]
# Even indexes: A[0]=10, A[2]=30, A[4]=50
# prefix_sum → [10, 10, 40, 40, 90, 90]

B = [[0, 5], [1, 3], [4, 5]]
# Expected: [90, 30, 50]
```

---

## 📚 Related Concepts to Explore Next

| Concept | Description |
|:--------|:------------|
| **2D Prefix Sum** | Same idea extended to matrices for rectangle sum queries |
| **Difference Array** | Inverse of prefix sum — useful for range update queries |
| **Segment Tree** | Handles dynamic arrays where values can change |
| **Sparse Table** | Ultra-fast for range minimum/maximum queries |
| **Binary Indexed Tree (BIT/Fenwick Tree)** | Efficient prefix sums with updates |

---

> ✍️ **Key Takeaway:**
> Prefix Sum is a **pre-processing trick** — spend a little time upfront building a helper array,
> then answer any range query in **O(1)**. It's one of the most powerful and elegant tools
> in competitive programming and data engineering.

---

*Happy Coding! 🚀*
