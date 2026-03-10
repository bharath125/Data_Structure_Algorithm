# 🎯 Maximum Subarray Sum ≤ B

> **Difficulty:** Beginner → Intermediate
> **Topic:** Arrays · Prefix Sum · Range Queries · Constrained Optimisation
> **Language:** Python
> **Constraints:** 1 ≤ A ≤ 10³ · 1 ≤ B ≤ 10⁹ · 1 ≤ C[i] ≤ 10⁶

---

## 📋 Problem Statement

Given:
- **A** — the size of the array
- **B** — the maximum allowed sum (upper bound, inclusive)
- **C** — an array of A integers

Find the **maximum subarray sum** that does **not exceed B**.
If no valid subarray exists, return **0**.

```
Goal: max( sum(C[i..j]) )   where   sum(C[i..j]) ≤ B
```

---

## 🌍 Real-World Analogy — Before Any Code

### 🛒 Shopping on a Budget

You're at a supermarket with a **budget of ₹12**. Items are arranged in a row on a shelf, and you can only pick a **consecutive block** of items (no skipping).

```
Shelf: [2,  1,  3,  4,  5]  ← prices
        ↑   ↑   ↑   ↑   ↑
       ₹2  ₹1  ₹3  ₹4  ₹5
```

You want to spend **as much as possible** without going over ₹12.

- Take items 1–5? Total = ₹15 → ❌ over budget
- Take items 3–5? Total = ₹12 → ✅ **exactly ₹12 — perfect!**
- Take items 1–4? Total = ₹10 → ✅ valid but not as good

**Answer: ₹12** — the largest valid spend.

This is exactly the problem. Find the maximum subarray sum that fits within budget **B**.

---

## 🧩 Understanding the Examples

### Example 1: `A=5, B=12, C=[2,1,3,4,5]`

```
Index:   0    1    2    3    4
Value: [ 2,   1,   3,   4,   5 ]
         ↑              ↑    ↑
         budget = 12
```

Let's look at every possible subarray and its sum:

| Subarray       | Elements      | Sum | ≤ 12? |
|:---------------|:--------------|:---:|:------:|
| C[0..0]        | [2]           | 2   | ✅     |
| C[0..1]        | [2,1]         | 3   | ✅     |
| C[0..2]        | [2,1,3]       | 6   | ✅     |
| C[0..3]        | [2,1,3,4]     | 10  | ✅     |
| C[0..4]        | [2,1,3,4,5]   | 15  | ❌     |
| C[1..1]        | [1]           | 1   | ✅     |
| C[1..2]        | [1,3]         | 4   | ✅     |
| C[1..3]        | [1,3,4]       | 8   | ✅     |
| C[1..4]        | [1,3,4,5]     | 13  | ❌     |
| C[2..2]        | [3]           | 3   | ✅     |
| C[2..3]        | [3,4]         | 7   | ✅     |
| **C[2..4]**    | **[3,4,5]**   | **12** | ✅ ← **MAX!** |
| C[3..3]        | [4]           | 4   | ✅     |
| C[3..4]        | [4,5]         | 9   | ✅     |
| C[4..4]        | [5]           | 5   | ✅     |

**Answer = 12** ✅ (subarray `[3,4,5]`)

---

### Example 2: `A=3, B=1, C=[2,2,2]`

```
All elements = 2, but B = 1
Every single element (2) already exceeds B (1).
Every subarray sum ≥ 2 > 1.
No valid subarray exists → return 0
```

| Subarray | Sum | ≤ 1? |
|:--------:|:---:|:----:|
| [2]      | 2   | ❌   |
| [2,2]    | 4   | ❌   |
| [2,2,2]  | 6   | ❌   |
| [2]      | 2   | ❌   |
| [2,2]    | 4   | ❌   |
| [2]      | 2   | ❌   |

**Answer = 0** ✅ (no valid subarray, so empty subarray sum = 0)

---

## 💡 The Approach — Prefix Sum + Constrained Max

### Why Prefix Sum?

Without prefix sum, computing every subarray sum means nesting three loops — O(N³).
With prefix sum, we compute each subarray sum in **O(1)** after an O(N) build — total **O(N²)**.

Since **A ≤ 10³**, O(N²) = 10⁶ operations — perfectly fast.

### Two-Phase Strategy

```
Phase 1: Build prefix sum array  →  O(N)
Phase 2: Check all (i,j) pairs,
         keep largest sum ≤ B   →  O(N²)
```

---

## 🔍 Phase 1 — Building the Prefix Sum Array

```python
pf_sum = []
tot = 0

for i in range(A):           # loop through all A elements
    tot += C[i]              # add current element to running total
    pf_sum.append(tot)       # store: "sum from C[0] to C[i]"
```

### What `pf_sum[i]` means

```
pf_sum[i] = C[0] + C[1] + C[2] + ... + C[i]
            └───────── sum from start up to and including i ───────────┘
```

This is a **same-size, non-padded** prefix array — `pf_sum[i]` covers C[0] through C[i] inclusive.

### Build Trace for `C = [2, 1, 3, 4, 5]`

| `i` | `C[i]` | Calculation          | `tot` | `pf_sum[i]` |
|:---:|:------:|:---------------------|:-----:|:-----------:|
| 0   | 2      | 0 + 2 = 2            | 2     | **2**       |
| 1   | 1      | 2 + 1 = 3            | 3     | **3**       |
| 2   | 3      | 3 + 3 = 6            | 6     | **6**       |
| 3   | 4      | 6 + 4 = 10           | 10    | **10**      |
| 4   | 5      | 10 + 5 = 15          | 15    | **15**      |

```
pf_sum = [2,  3,  6,  10,  15]
          ↑   ↑   ↑    ↑    ↑
         i=0 i=1 i=2  i=3  i=4

Reading it:
  pf_sum[0] =  2  → sum of C[0..0] = {2}
  pf_sum[1] =  3  → sum of C[0..1] = {2,1}
  pf_sum[2] =  6  → sum of C[0..2] = {2,1,3}
  pf_sum[3] = 10  → sum of C[0..3] = {2,1,3,4}
  pf_sum[4] = 15  → sum of C[0..4] = {2,1,3,4,5}
```

---

## 🔍 Phase 2 — Query Every Subarray with the Budget Check

```python
res = 0                     # Best answer so far (0 = empty subarray)

for i in range(A):          # i = start of subarray
    for j in range(i, A):   # j = end of subarray (j >= i always)

        subarraysum = 0

        if i == 0:
            subarraysum = pf_sum[j]              # sum C[0..j]
        else:
            subarraysum = pf_sum[j] - pf_sum[i-1]  # sum C[i..j]

        if subarraysum <= B:                     # within budget?
            res = max(res, subarraysum)          # update best if larger

return res
```

### Line by Line

```python
res = 0
```
> Initialised to **0** — the sum of the "empty subarray." If every subarray exceeds B,
> we return 0 (as in Example 2). This is not an arbitrary choice — it means
> "if nothing fits the budget, we took nothing."

---

```python
for i in range(A):
    for j in range(i, A):
```
> `i` fixes the **start** of the subarray.
> `j` fixes the **end** — starts at `i` (single element) and goes to `A-1`.
> `j >= i` always, so we never look at empty or reversed subarrays.
> Total pairs: A*(A+1)/2 = 15 for A=5.

---

```python
        if i == 0:
            subarraysum = pf_sum[j]
        else:
            subarraysum = pf_sum[j] - pf_sum[i-1]
```
> **When `i = 0`:** The subarray starts at index 0 — `pf_sum[j]` already holds
> exactly C[0]+…+C[j]. No subtraction needed.
>
> **When `i > 0`:** We subtract `pf_sum[i-1]` to remove the prefix before index `i`.
>
> ```
> pf_sum[j]     = C[0] + C[1] + ... + C[i-1] + C[i] + ... + C[j]
> pf_sum[i-1]   = C[0] + C[1] + ... + C[i-1]
>                 └────────────────────────────┘
>                          cancels out!
>
> Difference    = C[i] + C[i+1] + ... + C[j]   ✅
> ```
>
> **Why not just write `pf_sum[j] - (pf_sum[i-1] if i > 0 else 0)`?**
> Both work identically. The `if i == 0` form makes the two cases visually explicit.

---

```python
        if subarraysum <= B:
            res = max(res, subarraysum)
```
> **The budget gate:** Only consider subarrays that fit within B.
> Among all valid ones, keep the largest.
> `max(res, subarraysum)` ensures `res` only ever grows.

---

## 📊 Full Query Dry Run — Example 1

`C=[2,1,3,4,5]`, `B=12`, `pf_sum=[2,3,6,10,15]`

| `[i,j]` | Subarray   | Formula                      | Sum | ≤ 12? | `res` |
|:-------:|:----------:|:-----------------------------|:---:|:-----:|:-----:|
| [0,0]   | [2]        | `pf[0]` = 2                  | 2   | ✅    | 2     |
| [0,1]   | [2,1]      | `pf[1]` = 3                  | 3   | ✅    | 3     |
| [0,2]   | [2,1,3]    | `pf[2]` = 6                  | 6   | ✅    | 6     |
| [0,3]   | [2,1,3,4]  | `pf[3]` = 10                 | 10  | ✅    | 10    |
| [0,4]   | [2,1,3,4,5]| `pf[4]` = 15                 | 15  | ❌ >B | 10    |
| [1,1]   | [1]        | `pf[1]-pf[0]`=3-2=1          | 1   | ✅    | 10    |
| [1,2]   | [1,3]      | `pf[2]-pf[0]`=6-2=4          | 4   | ✅    | 10    |
| [1,3]   | [1,3,4]    | `pf[3]-pf[0]`=10-2=8         | 8   | ✅    | 10    |
| [1,4]   | [1,3,4,5]  | `pf[4]-pf[0]`=15-2=13        | 13  | ❌ >B | 10    |
| [2,2]   | [3]        | `pf[2]-pf[1]`=6-3=3          | 3   | ✅    | 10    |
| [2,3]   | [3,4]      | `pf[3]-pf[1]`=10-3=7         | 7   | ✅    | 10    |
| **[2,4]** | **[3,4,5]** | **`pf[4]-pf[1]`=15-3=12** | **12** | **✅** | **12** ← |
| [3,3]   | [4]        | `pf[3]-pf[2]`=10-6=4         | 4   | ✅    | 12    |
| [3,4]   | [4,5]      | `pf[4]-pf[2]`=15-6=9         | 9   | ✅    | 12    |
| [4,4]   | [5]        | `pf[4]-pf[3]`=15-10=5        | 5   | ✅    | 12    |

**Final `res = 12`** ✅

---

## 📊 Full Query Dry Run — Example 2

`C=[2,2,2]`, `B=1`, `pf_sum=[2,4,6]`

| `[i,j]` | Sum | ≤ 1? | `res` |
|:-------:|:---:|:----:|:-----:|
| [0,0]   | 2   | ❌   | 0     |
| [0,1]   | 4   | ❌   | 0     |
| [0,2]   | 6   | ❌   | 0     |
| [1,1]   | 2   | ❌   | 0     |
| [1,2]   | 4   | ❌   | 0     |
| [2,2]   | 2   | ❌   | 0     |

Every subarray exceeds B=1. `res` never updates. **Returns 0** ✅

---

## 🗺️ Complete Visual Summary

```
INPUT: A=5, B=12, C=[2, 1, 3, 4, 5]

PHASE 1 — Build prefix sum:
┌────┬────┬────┬────┬────┐
│  2 │  3 │  6 │ 10 │ 15 │  ← pf_sum
└────┴────┴────┴────┴────┘
 i=0  i=1  i=2  i=3  i=4

PHASE 2 — Check every (i,j) pair:
  res = 0  (empty subarray baseline)

  i=0: sums = 2, 3, 6, 10 [✅ ≤12]  15 [❌ >12]  → res=10
  i=1: sums = 1, 4, 8 [✅]           13 [❌]      → res=10 (no change)
  i=2: sums = 3, 7, 12 [✅ 12==B]                → res=12 ← NEW MAX
  i=3: sums = 4, 9 [✅]                           → res=12 (no change)
  i=4: sums = 5 [✅]                              → res=12 (no change)

QUERY FORMULA:
  i == 0  →  subarraysum = pf_sum[j]
  i >  0  →  subarraysum = pf_sum[j] - pf_sum[i-1]

BUDGET GATE:
  if subarraysum <= B  →  candidate for res
  else                 →  skip

ANSWER: 12
        (subarray C[2..4] = [3,4,5] = 3+4+5 = 12 ≤ 12 ✅)
```

---

## ⚠️ Edge Cases & Pitfalls

### ❗ Pitfall 1: `pf_sum[-1]` Silent Python Bug

When `i = 0`, the formula `pf_sum[j] - pf_sum[i-1]` becomes `pf_sum[j] - pf_sum[-1]`.
Python's `-1` index silently returns the **last element** (15 here) — a wrong answer with no error!

```python
# ❌ BUG — pf_sum[-1] fires when i=0
subarraysum = pf_sum[j] - pf_sum[i-1]

# ✅ CORRECT — guard the i==0 case
if i == 0:
    subarraysum = pf_sum[j]
else:
    subarraysum = pf_sum[j] - pf_sum[i-1]
```

---

### ❗ Pitfall 2: Why `res = 0` and Not `res = float('-inf')`

This problem is different from "find maximum subarray sum" without constraints.

```python
res = float('-inf')   # ❌ WRONG for this problem
```

If no subarray sum ≤ B exists (Example 2), `float('-inf')` would be returned — but the
problem says return **0** (the empty subarray has sum 0 and 0 ≤ B always).

```python
res = 0   # ✅ CORRECT — represents "no valid subarray found → empty subarray"
```

> 💡 Think of it as: "we're always allowed to take **nothing**,
> which has sum 0. We're looking to beat that."

---

### ❗ Pitfall 3: All Elements Smaller Than B — Full Array Might Be Answer

```python
C = [2, 1, 3, 4, 5], B = 100
→ Every subarray is valid
→ Largest subarray = entire array = sum 15
→ Answer = 15
```

The code handles this naturally — `res` keeps updating until the largest valid subarray is found.

---

### ❗ Pitfall 4: `j` starts at `i`, not at `0`

```python
for j in range(i, A):    # ✅ CORRECT — j always >= i
for j in range(0, A):    # ❌ WRONG  — allows j < i (reversed/invalid subarrays)
```

A subarray `C[i..j]` only makes sense when `j >= i`. Starting `j` from `i` enforces this automatically.

---

### ❗ Pitfall 5: Single-Element Subarrays

If every multi-element subarray exceeds B but some single element equals B:

```python
C = [12, 1, 2], B = 12
→ C[0..0] = [12] sum=12 ≤ 12 ✅ → res=12
→ Answer = 12
```

The code checks every `(i, j)` including `i == j` (single element). Handled correctly ✅

---

## ⏱️ Complexity Analysis

| Phase              | Operation                | Complexity   |
|:-------------------|:-------------------------|:------------:|
| Build prefix sum   | One pass over A          | **O(A)**     |
| Double loop        | A*(A+1)/2 pairs          | **O(A²)**    |
| Each pair check    | One subtraction + compare | **O(1)**    |
| **Total Time**     |                          | **O(A²)**    |
| **Space**          | One prefix array size A  | **O(A)**     |

### Is O(A²) Fast Enough?

```
A ≤ 10³

A² = 10^6 operations → well within limits ✅

If A were 10^5: A² = 10^10 → TLE  (would need a smarter approach)
But with A ≤ 10³, O(A²) is perfectly fine.
```

---

## 🧪 Test It Yourself

```python
def solve(A, B, C):
    # Phase 1: Build prefix sum
    pf_sum = []
    tot = 0
    for i in range(A):
        tot += C[i]
        pf_sum.append(tot)

    # Phase 2: Find max subarray sum <= B
    res = 0
    for i in range(A):
        for j in range(i, A):
            if i == 0:
                sub = pf_sum[j]
            else:
                sub = pf_sum[j] - pf_sum[i-1]
            if sub <= B:
                res = max(res, sub)
    return res


tests = [
    (5, 12, [2,1,3,4,5],   12),   # [3,4,5] = 12
    (3,  1, [2,2,2],        0),   # all > B → 0
    (5, 100, [2,1,3,4,5],  15),   # B very large → full array
    (4,  7, [3,1,4,2],      7),   # [3,1,4-1]? Let's see: [3,4]? no adj. [3,1,4-nope. [1,4,2]=7
    (1,  5, [5],            5),   # single element == B
    (1,  4, [5],            0),   # single element > B
    (3, 10, [4,4,4],        8),   # [4,4]=8 fits, [4,4,4]=12 doesn't
]

for A, B, C, expected in tests:
    result = solve(A, B, C)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  B={B}  C={C}  → {result}")
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Prefix Sum (basic)** | Core building block used in this solution |
| **Kadane's Algorithm** | Max subarray sum with no upper bound — O(N) |
| **Maximum Subarray Sum ≤ K** (LeetCode 363) | Harder version: O(N log N) with sorted sets |
| **Sliding Window** | For max subarray of fixed size — O(N) |
| **Two Sum / HashMap** | Range sum queries using hashing |
| **Segment Trees** | Dynamic range queries with updates |

---

> ✍️ **The Big Idea:**
> This problem adds a **constraint** to the classic max-subarray problem:
> the sum must stay ≤ B. Rather than finding just any maximum, we need the
> **largest sum that still fits the budget**.
> The prefix sum makes every subarray sum computable in O(1).
> The `if subarraysum <= B` gate filters out subarrays that exceed the budget.
> Among all passing subarrays, we track the maximum.
> Initialising `res = 0` elegantly handles the "no valid subarray" case — the
> empty subarray always has sum 0, which is a valid fallback answer.

---

*Happy Coding! 🚀*
