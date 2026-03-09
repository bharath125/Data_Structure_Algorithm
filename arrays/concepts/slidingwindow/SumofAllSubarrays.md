# ➕ Sum of All Subarray Sums
### Three Approaches: O(N³) → O(N²) → O(N)

> **Difficulty:** Beginner → Advanced (Google / Facebook Interview Problem)
> **Topic:** Arrays · Prefix Sum · Mathematical Contribution Technique
> **Language:** Python
> **Constraints:** 1 ≤ N ≤ 10⁵ · 1 ≤ A[i] ≤ 10⁴

---

## 📋 Problem Statement

Given an integer array **A** of length **N**, find the **sum of all subarray sums**.

A **subarray** is a contiguous part of the array. For each subarray, compute its sum, then add all those sums together.

```
For A = [1, 2, 3]:
  Subarrays → [1], [2], [3], [1,2], [2,3], [1,2,3]
  Sums      →   1    2    3     3      5       6
  Total     = 1 + 2 + 3 + 3 + 5 + 6 = 20
```

> ⚠️ **Overflow warning:** With N=10⁵ and A[i]=10⁴, max answer ≈ 10⁴ × N² ≈ 10¹⁴.
> Use `long long` in C++/Java. Python handles big integers automatically.

---

## 🌍 Real-World Analogy — Before Any Code

### 🏪 Sales Report Across Every Time Window

Imagine a shop's daily sales over N days: `A = [2, 8, 1, 3]`

A business analyst wants to sum up the **revenue across every possible consecutive window**:
- All single-day windows: Day 1, Day 2, Day 3, Day 4
- All 2-day windows: Days 1-2, Days 2-3, Days 3-4
- All 3-day windows: Days 1-3, Days 2-4
- The full window: Days 1-4

The total across all these windows = **sum of all subarray sums**.

Three ways to calculate this — ranging from "obvious but slow" to "elegant and instant."

---

## 🔢 All Subarrays of `A = [2, 8, 1, 3]`

```
Starting at index 0:   [2]         → 2
                       [2, 8]      → 10
                       [2, 8, 1]   → 11
                       [2, 8, 1, 3]→ 14

Starting at index 1:   [8]         → 8
                       [8, 1]      → 9
                       [8, 1, 3]   → 12

Starting at index 2:   [1]         → 1
                       [1, 3]      → 4

Starting at index 3:   [3]         → 3

Grand Total = 2+10+11+14+8+9+12+1+4+3 = 74
```

All three approaches must produce **74**.

---

---

# 🐢 Approach 1 — Brute Force: O(N³) Time, O(1) Space

---

## 🔍 The Code

```python
A = [2, 8, 1, 3]
n = len(A)
total_sum = 0

for i in range(n):          # i = start index of subarray
    for j in range(i, n):   # j = end index of subarray
        subArraySum = 0
        for k in range(i, j+1):   # k = scan elements inside [i..j]
            subArraySum += A[k]
        total_sum += subArraySum

print(total_sum)   # 74
```

## 🔍 Every Line Explained

**Outer loop `i`:** Fixes the **start** of the subarray. Runs from 0 to N-1.

**Middle loop `j`:** Fixes the **end** of the subarray. Starts at `i` (single element) and goes to N-1.

**Inner loop `k`:** Walks through every element from `i` to `j` and sums them.

Every possible subarray `A[i..j]` is enumerated — there are `N*(N+1)/2` of them — and each is summed from scratch.

## 📊 Dry Run for `A = [2, 8, 1, 3]`

| `i` | `j` | Subarray    | `k` scan       | `subArraySum` | `total_sum` |
|:---:|:---:|:------------|:---------------|:-------------:|:-----------:|
| 0   | 0   | [2]         | k=0: +2        | 2             | 2           |
| 0   | 1   | [2,8]       | k=0,1: +2+8    | 10            | 12          |
| 0   | 2   | [2,8,1]     | k=0,1,2: +11   | 11            | 23          |
| 0   | 3   | [2,8,1,3]   | k=0..3: +14    | 14            | 37          |
| 1   | 1   | [8]         | k=1: +8        | 8             | 45          |
| 1   | 2   | [8,1]       | k=1,2: +9      | 9             | 54          |
| 1   | 3   | [8,1,3]     | k=1..3: +12    | 12            | 66          |
| 2   | 2   | [1]         | k=2: +1        | 1             | 67          |
| 2   | 3   | [1,3]       | k=2,3: +4      | 4             | 71          |
| 3   | 3   | [3]         | k=3: +3        | 3             | **74**      |

## ⏱️ Why O(N³)?

```
Outer loop:  N iterations
Middle loop: up to N iterations
Inner loop:  up to N iterations
Total operations: N × N × N = N³

For N=10⁵: 10⁵ × 10⁵ × 10⁵ = 10¹⁵ operations  😱  (impossible)
```

---

---

# 🚶 Approach 2 — Prefix Sum: O(N²) Time, O(N) Space

---

## 💡 Key Insight: Pre-compute running totals

Instead of re-summing `A[i..j]` from scratch every time, build a **prefix sum array** once.
Then any subarray sum is just one subtraction — O(1) instead of O(N) per query.

## 🔍 The Code

```python
# Phase 1: Build prefix sum array
prefix_sum = []
total = 0
for i in range(n):
    total += A[i]
    prefix_sum.append(total)

# Phase 2: Use prefix sums to answer each [i,j] in O(1)
total_sum = 0
for i in range(n):
    for j in range(i, n):
        if i == 0:
            subArraySum = prefix_sum[j]
        else:
            subArraySum = prefix_sum[j] - prefix_sum[i-1]
        total_sum += subArraySum

print(total_sum)   # 74
```

## 📊 Phase 1 — Build Prefix Array

For `A = [2, 8, 1, 3]`:

| `i` | `A[i]` | Calculation      | `prefix_sum[i]` |
|:---:|:------:|:-----------------|:---------------:|
| 0   | 2      | 0 + 2 = 2        | **2**           |
| 1   | 8      | 2 + 8 = 10       | **10**          |
| 2   | 1      | 10 + 1 = 11      | **11**          |
| 3   | 3      | 11 + 3 = 14      | **14**          |

```
prefix_sum = [2, 10, 11, 14]
              ↑   ↑   ↑   ↑
             i=0 i=1 i=2 i=3
```

`prefix_sum[i]` = sum of A[0] + A[1] + … + A[i] (inclusive)

## 📊 Phase 2 — Query Every Subarray in O(1)

| `[i,j]` | Formula                         | Value | `total_sum` |
|:-------:|:--------------------------------|:-----:|:-----------:|
| [0,0]   | `prefix[0]` = 2                 | 2     | 2           |
| [0,1]   | `prefix[1]` = 10                | 10    | 12          |
| [0,2]   | `prefix[2]` = 11                | 11    | 23          |
| [0,3]   | `prefix[3]` = 14                | 14    | 37          |
| [1,1]   | `prefix[1]-prefix[0]`=10-2      | 8     | 45          |
| [1,2]   | `prefix[2]-prefix[0]`=11-2      | 9     | 54          |
| [1,3]   | `prefix[3]-prefix[0]`=14-2      | 12    | 66          |
| [2,2]   | `prefix[2]-prefix[1]`=11-10     | 1     | 67          |
| [2,3]   | `prefix[3]-prefix[1]`=14-10     | 4     | 71          |
| [3,3]   | `prefix[3]-prefix[2]`=14-11     | 3     | **74** ✅   |

## ⏱️ Why O(N²)?

```
Build prefix: O(N)      ← one pass
Double loop:  O(N²)     ← but inner operation is now O(1)!
Total: O(N + N²) = O(N²)

For N=10⁵: 10¹⁰ operations  ⚠️  Still too slow for tight constraints
```

---

---

# 🚀 Approach 3 — Mathematical Formula: O(N) Time, O(1) Space
### *The Google / Facebook Interview Answer*

---

## 💡 The "Contribution" Insight

**Instead of summing subarrays, ask: how many times does each element contribute to the grand total?**

Every element `A[i]` appears in **multiple subarrays**. If we know how many subarrays contain `A[i]`, then its total contribution = `A[i] × count`.

Sum up contributions of all elements → done in O(N)!

---

## 🔬 How Many Subarrays Contain Index `i`?

A subarray `A[L..R]` contains index `i` if and only if:
```
L ≤ i  AND  R ≥ i
```

So we need to count all valid (L, R) pairs where `L ≤ i ≤ R`.

**Choices for the left boundary L:**
```
L can be:  0, 1, 2, ..., i
           └────────────────┘
           That's (i + 1) choices
```

**Choices for the right boundary R:**
```
R can be:  i, i+1, i+2, ..., N-1
           └──────────────────────┘
           That's (N - i) choices
```

**Total subarrays containing index `i`:**
```
count = (i + 1) × (N - i)
```

Since any left boundary can be paired with any right boundary independently, we multiply the choices.

---

## 🗺️ Visualising the Formula

For `A = [2, 8, 1, 3]` (N=4), let's find how many subarrays contain **index 1** (value 8):

```
              ↓ fixed
A:  [ 2,   8,   1,   3 ]
      0    1    2    3

Left boundary L can be:  0 or 1         → 2 choices  = (i+1) = 1+1 = 2
Right boundary R can be: 1, 2, or 3     → 3 choices  = (N-i) = 4-1 = 3

Total = 2 × 3 = 6 subarrays
```

Which 6 subarrays? Let's verify:
```
L=0, R=1 → A[0..1] = [2, 8]       ✅ contains index 1
L=0, R=2 → A[0..2] = [2, 8, 1]    ✅ contains index 1
L=0, R=3 → A[0..3] = [2, 8, 1, 3] ✅ contains index 1
L=1, R=1 → A[1..1] = [8]           ✅ contains index 1
L=1, R=2 → A[1..2] = [8, 1]        ✅ contains index 1
L=1, R=3 → A[1..3] = [8, 1, 3]     ✅ contains index 1
```

Exactly 6! ✅ So A[1]=8 contributes `8 × 6 = 48` to the grand total.

---

## 📊 Contribution Table for `A = [2, 8, 1, 3]`

| Index `i` | `A[i]` | Left choices `(i+1)` | Right choices `(N-i)` | Occurrences | Contribution |
|:---------:|:------:|:--------------------:|:---------------------:|:-----------:|:------------:|
| 0         | 2      | 0+1 = **1**          | 4-0 = **4**           | 1×4 = **4** | 2×4 = **8**  |
| 1         | 8      | 1+1 = **2**          | 4-1 = **3**           | 2×3 = **6** | 8×6 = **48** |
| 2         | 1      | 2+1 = **3**          | 4-2 = **2**           | 3×2 = **6** | 1×6 = **6**  |
| 3         | 3      | 3+1 = **4**          | 4-3 = **1**           | 4×1 = **4** | 3×4 = **12** |
|           |        |                      |                       | **Total:**  | **74** ✅    |

> 🔍 Notice: Elements at the **centre** of the array appear in the most subarrays
> (e.g., indices 1 and 2 both appear 6 times). Elements at the **edges**
> (indices 0 and 3) appear in only 4 subarrays each.

---

## 📐 Why the Pattern Is Symmetric

For N=4, the occurrence counts are: **4, 6, 6, 4**

For N=5, they would be: **5, 8, 9, 8, 5**

This follows from `(i+1)*(N-i)`:
- Index 0: 1×N = N
- Index N-1: N×1 = N (same as index 0)
- Middle index(es): have the largest values

The pattern is always symmetric and peaks at the centre.

---

## 🔍 The Code

```python
n = len(A)
total_sum = 0

for i in range(n):
    total_sum += A[i] * (i + 1) * (n - i)
    #              ↑        ↑         ↑
    #           value   left      right
    #                  choices   choices

print(total_sum)   # 74
```

Three operations per element. No nested loops. No extra arrays.

## 📊 Code Trace for `A = [2, 8, 1, 3]`

```
n = 4, total_sum starts at 0

i=0: total_sum += A[0]*(0+1)*(4-0) = 2 * 1 * 4  = 8     → total_sum = 8
i=1: total_sum += A[1]*(1+1)*(4-1) = 8 * 2 * 3  = 48    → total_sum = 56
i=2: total_sum += A[2]*(2+1)*(4-2) = 1 * 3 * 2  = 6     → total_sum = 62
i=3: total_sum += A[3]*(3+1)*(4-3) = 3 * 4 * 1  = 12    → total_sum = 74

Final: 74 ✅
```

---

## 🔬 Verify with Example 1: `A = [1, 2, 3]`

```
n = 3

i=0: 1 * (0+1) * (3-0) = 1 * 1 * 3 = 3
i=1: 2 * (1+1) * (3-1) = 2 * 2 * 2 = 8
i=2: 3 * (2+1) * (3-2) = 3 * 3 * 1 = 9

Total = 3 + 8 + 9 = 20 ✅
```

## 🔬 Verify with Example 2: `A = [2, 1, 3]`

```
n = 3

i=0: 2 * 1 * 3 = 6
i=1: 1 * 2 * 2 = 4
i=2: 3 * 3 * 1 = 9

Total = 6 + 4 + 9 = 19 ✅
```

---

## ⏱️ Why O(N)?

```
Single loop: N iterations
Each iteration: 3 multiplications + 1 addition = O(1)
Total: N × O(1) = O(N)

For N=10⁵: 100,000 operations  🚀  Instant
```

---

---

# 📊 Comparison of All Three Approaches

| Approach     | Time       | Space | Key Idea                          |
|:-------------|:----------:|:-----:|:----------------------------------|
| Brute Force  | **O(N³)**  | O(1)  | Sum each subarray from scratch    |
| Prefix Sum   | **O(N²)**  | O(N)  | Pre-compute running sums          |
| Formula      | **O(N)**   | O(1)  | Count each element's contribution |

### Speed at Scale (N = 100,000)

```
O(N³) Brute Force: 10^15 operations  ❌  Would take ~100,000 seconds
O(N²) Prefix Sum:  10^10 operations  ⚠️  Would take ~10 seconds (TLE)
O(N)  Formula:     10^5  operations  ✅  Instant (<1 millisecond)
```

---

## 🗺️ Complete Visual Summary

```
PROBLEM: Sum of ALL subarray sums of A = [2, 8, 1, 3]

─────────────────────────────────────────────────────────
APPROACH 1 — O(N³): Triple nested loop

  for i (start):
    for j (end):
      for k (scan [i..j]):
        subArraySum += A[k]    ← recomputes each time
      total += subArraySum

  10^15 ops for N=10^5  ❌
─────────────────────────────────────────────────────────
APPROACH 2 — O(N²): Prefix sum

  Build once: prefix = [2, 10, 11, 14]

  for i (start):
    for j (end):
      subArraySum = prefix[j] - prefix[i-1]  ← O(1)!
      total += subArraySum

  10^10 ops for N=10^5  ⚠️
─────────────────────────────────────────────────────────
APPROACH 3 — O(N): Contribution formula

  For each element A[i]:
    It appears in (i+1) × (N-i) subarrays
    Its total contribution = A[i] × (i+1) × (N-i)

  A=[2, 8, 1, 3]
  i=0: 2 × 1 × 4 =  8
  i=1: 8 × 2 × 3 = 48
  i=2: 1 × 3 × 2 =  6
  i=3: 3 × 4 × 1 = 12
                  ────
                   74  ✅

  10^5 ops for N=10^5  ✅  FASTEST!
─────────────────────────────────────────────────────────
```

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: Integer Overflow (C++/Java)

```
Max A[i] = 10^4, max N = 10^5

Max contribution of one element = A[i] × (i+1) × (N-i)
  ≈ 10^4 × (N/2) × (N/2) = 10^4 × (5×10^4)² / 4 ≈ 6.25 × 10^12

Max total sum ≈ N × max_per_element ≈ 10^5 × 6.25×10^12 = way beyond int32!

C++: use long long  ✅
Java: use long      ✅
Python: automatic   ✅  (no overflow)
```

### ❗ Pitfall 2: Confusing `(i+1)*(n-i)` Direction

```
(i+1) = how many choices for LEFT boundary  (0, 1, ..., i)
(n-i) = how many choices for RIGHT boundary (i, i+1, ..., n-1)

Not the other way around! Double-check with i=0:
  (0+1) = 1 left choice  → only L=0  ✅
  (n-0) = n right choices → R=0,1,...,n-1  ✅
```

### ❗ Pitfall 3: Prefix Sum `i-1` bug when `i=0`

```python
# ❌ Forgetting the L==0 special case in Approach 2
subArraySum = prefix_sum[j] - prefix_sum[i-1]
# When i=0: prefix_sum[-1] = last element  ← WRONG in Python!

# ✅ Always guard:
if i == 0:
    subArraySum = prefix_sum[j]
else:
    subArraySum = prefix_sum[j] - prefix_sum[i-1]
```

---

## 🧪 Test It Yourself

```python
def solve_brute(A):
    n, total = len(A), 0
    for i in range(n):
        for j in range(i, n):
            s = 0
            for k in range(i, j+1):
                s += A[k]
            total += s
    return total

def solve_prefix(A):
    n = len(A)
    prefix, t = [], 0
    for x in A:
        t += x
        prefix.append(t)
    total = 0
    for i in range(n):
        for j in range(i, n):
            total += prefix[j] if i == 0 else prefix[j] - prefix[i-1]
    return total

def solve_formula(A):
    n = len(A)
    return sum(A[i] * (i+1) * (n-i) for i in range(n))


tests = [
    [1, 2, 3],      # 20
    [2, 1, 3],      # 19
    [2, 8, 1, 3],   # 74
    [1],            # 1
    [5, 5],         # 20   (5+5+5 = 15? No: [5],[5],[5,5] = 5+5+10=20)
    [1, 1, 1, 1],   # each A[i]=1, formula: 1*1*4 + 1*2*3 + 1*3*2 + 1*4*1 = 4+6+6+4 = 20
]

for A in tests:
    b, p, f = solve_brute(A), solve_prefix(A), solve_formula(A)
    match = "✅" if b == p == f else "❌"
    print(f"{match}  A={A}  → brute={b}  prefix={p}  formula={f}")
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Contribution technique** | Same idea: count how many times each element "counts" |
| **Sum of subarray minimums** (LeetCode 907) | Contribution with monotonic stack |
| **Sum of subarray maximums** | Same but for max |
| **Number of subarrays with sum K** | Prefix sum + hashmap |
| **Maximum subarray sum (Kadane's)** | Single-pass optimal subarray algorithm |
| **Sliding window** | Another O(N) window technique |

---

> ✍️ **The Big Idea:**
> The brute-force mindset says *"enumerate all subarrays, compute each sum."*
> The prefix sum mindset says *"pre-compute to make each sum query O(1)."*
> The **contribution** mindset flips the question entirely:
> *"Instead of summing each subarray, ask how much each element contributes."*
> Each element `A[i]` appears in exactly `(i+1) × (N-i)` subarrays.
> Multiply and sum — one pass, no extra space, O(N).
> This pattern of "per-element contribution" appears in dozens of interview problems.

---

*Happy Coding! 🚀*
