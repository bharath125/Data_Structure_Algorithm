# ⚖️ Equilibrium Index of an Array

> **Difficulty:** Beginner → Advanced
> **Topic:** Arrays · Prefix Sum · Running Sum
> **Language:** Python
> **Constraints:** 1 ≤ N ≤ 10⁵ · -10⁵ ≤ A[i] ≤ 10⁵

---

## 📋 Problem Statement

Given an integer array **A** of size **N**, find the **equilibrium index** —
an index `i` such that:

```
Sum of A[0..i-1]  ==  Sum of A[i+1..N-1]
     (left sum)             (right sum)
```

**Rules:**
- If `i = 0`, left sum = **0** (no elements to the left)
- If `i = N-1`, right sum = **0** (no elements to the right)
- If **no** equilibrium index exists → return **-1**
- If **multiple** equilibrium indexes exist → return the **minimum** (leftmost) one
- Array indexing starts from **0**

---

## 🌍 Real-World Analogy — Before Any Code

### ⚖️ The Seesaw / Balance Scale

Imagine a **seesaw** with weights placed at each position:

```
Positions:  0     1     2     3     4     5     6
Weights:  [-7]   [1]   [5]   [2]  [-4]   [3]   [0]
           │     │     │     │     │     │     │
           ●─────●─────●─────●─────●─────●─────●
                             ▲
                         PIVOT HERE?
```

- Everything **left of the pivot** = left pan of the scale
- Everything **right of the pivot** = right pan of the scale
- The pivot itself = **NOT on either pan**

The equilibrium index is the **pivot position** where the seesaw perfectly balances — left weight equals right weight.

---

### 🏦 Bank Account Analogy

Think of A as daily **profit/loss** records of a business:

```
Day:    0     1     2     3     4     5     6
P&L:  [-7]   [1]   [5]   [2]  [-4]   [3]   [0]
```

**Question:** Is there a day `i` where:
- Total profit/loss of all days **before** day `i` = Total profit/loss of all days **after** day `i`?

That "balancing day" is the equilibrium index.

---

## 🧩 Understanding With the Given Examples

### Example 1

```python
A = [-7, 1, 5, 2, -4, 3, 0]
```

Let's check every index manually:

| Index `i` | A[i] | Left Sum (before i)      | Right Sum (after i)       | Balanced? |
|:---------:|:----:|:-------------------------|:--------------------------|:---------:|
| 0         | -7   | 0 (no elements)          | 1+5+2+(−4)+3+0 = **7**   | ❌        |
| 1         | 1    | −7 = **−7**              | 5+2+(−4)+3+0 = **6**     | ❌        |
| 2         | 5    | −7+1 = **−6**            | 2+(−4)+3+0 = **1**       | ❌        |
| 3         | 2    | −7+1+5 = **−1**          | (−4)+3+0 = **−1**        | ✅ **YES**|
| 4         | -4   | −7+1+5+2 = **1**         | 3+0 = **3**              | ❌        |
| 5         | 3    | −7+1+5+2+(−4) = **−3**   | 0 = **0**                | ❌        |
| 6         | 0    | −7+1+5+2+(−4)+3 = **0**  | 0 (no elements)          | ✅        |

- Index **3** balances ✅ and index **6** also balances ✅
- Return the **minimum** → **Answer = 3** ✅

---

### Example 2

```python
A = [1, 2, 3]
```

| Index `i` | A[i] | Left Sum | Right Sum | Balanced? |
|:---------:|:----:|:--------:|:---------:|:---------:|
| 0         | 1    | 0        | 2+3 = 5   | ❌        |
| 1         | 2    | 1        | 3         | ❌        |
| 2         | 3    | 1+2 = 3  | 0         | ❌        |

No index balances → **Answer = −1** ✅

---

## 💡 Key Insight — The Smart Formula

### Brute Force thinking (slow):

For every index `i`, re-calculate left sum and right sum from scratch.
That's **O(N²)** — too slow for N = 10⁵.

### Smart Observation:

```
total_sum  =  left_sum  +  A[i]  +  right_sum

Rearranging:
right_sum  =  total_sum  −  left_sum  −  A[i]

Equilibrium condition:
left_sum  ==  right_sum
left_sum  ==  total_sum  −  left_sum  −  A[i]
2 × left_sum  ==  total_sum  −  A[i]
```

So instead of computing right sum separately, just derive it from total sum!

---

## 🔍 Algorithm — Step by Step

```
Step 1: Compute total_sum of the entire array
Step 2: Initialize left_sum = 0
Step 3: Loop through each index i:
           right_sum = total_sum − left_sum − A[i]
           if left_sum == right_sum:
               return i   ← found equilibrium!
           left_sum += A[i]   ← grow left sum for next iteration
Step 4: If loop ends without returning → return -1
```

---

## 🔍 The Code — Every Line Explained

```python
A = [-7, 1, 5, 2, -4, 3, 0]

# Step 1: Total sum of the entire array
total_sum = sum(A)
# total_sum = -7+1+5+2+(-4)+3+0 = 0

# Step 2: Track left sum as we scan left → right
left_sum = 0

# Step 3: Check every index
for i in range(len(A)):

    # Derive right sum using the formula
    # right_sum = total_sum - left_sum - A[i]
    right_sum = total_sum - left_sum - A[i]

    # Check equilibrium condition
    if left_sum == right_sum:
        print(i)       # Found it!
        break

    # Expand left sum to include A[i] for the next iteration
    left_sum += A[i]

else:
    # Loop ended without break → no equilibrium found
    print(-1)
```

---

## 📊 Dry Run — Example 1 Traced

```python
A          = [-7,  1,  5,  2,  -4,  3,  0]
total_sum  = 0
```

| Step | `i` | `A[i]` | `left_sum` | `right_sum = 0 − left − A[i]` | `left == right?` | Action             |
|:----:|:---:|:------:|:----------:|:-----------------------------:|:----------------:|:------------------:|
| 1    | 0   | -7     | 0          | 0 − 0 − (−7) = **7**         | 0 ≠ 7 ❌         | left_sum = 0+(−7) = −7 |
| 2    | 1   | 1      | -7         | 0 − (−7) − 1 = **6**         | −7 ≠ 6 ❌        | left_sum = −7+1 = −6 |
| 3    | 2   | 5      | -6         | 0 − (−6) − 5 = **1**         | −6 ≠ 1 ❌        | left_sum = −6+5 = −1 |
| 4    | 3   | 2      | -1         | 0 − (−1) − 2 = **−1**        | −1 == −1 ✅      | **return 3** 🎉    |

**Output: 3** ✅

---

## 📊 Dry Run — Example 2 Traced

```python
A          = [1,  2,  3]
total_sum  = 6
```

| Step | `i` | `A[i]` | `left_sum` | `right_sum = 6 − left − A[i]` | `left == right?` | Action           |
|:----:|:---:|:------:|:----------:|:-----------------------------:|:----------------:|:----------------:|
| 1    | 0   | 1      | 0          | 6 − 0 − 1 = **5**            | 0 ≠ 5 ❌         | left_sum = 1     |
| 2    | 1   | 2      | 1          | 6 − 1 − 2 = **3**            | 1 ≠ 3 ❌         | left_sum = 3     |
| 3    | 2   | 3      | 3          | 6 − 3 − 3 = **0**            | 3 ≠ 0 ❌         | left_sum = 6     |

Loop ends without finding equilibrium.

**Output: −1** ✅

---

## 🎨 Visual Walkthrough — Example 1

```
A = [-7,  1,  5,  2, -4,  3,  0]
         ↑
     total_sum = 0

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
i=0  │  LEFT:[ ]      │ A[0]=-7 │  RIGHT:[1,5,2,-4,3,0]
     │  left_sum= 0   │         │  right_sum= 7
     │  0 ≠ 7  ❌                              │
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
i=1  │  LEFT:[-7]     │ A[1]=1  │  RIGHT:[5,2,-4,3,0]
     │  left_sum=-7   │         │  right_sum= 6
     │  -7 ≠ 6  ❌                             │
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
i=2  │  LEFT:[-7,1]   │ A[2]=5  │  RIGHT:[2,-4,3,0]
     │  left_sum=-6   │         │  right_sum= 1
     │  -6 ≠ 1  ❌                             │
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
i=3  │  LEFT:[-7,1,5] │ A[3]=2  │  RIGHT:[-4,3,0]
     │  left_sum=-1   │         │  right_sum=-1
     │  -1 == -1  ✅  ← EQUILIBRIUM FOUND!     │
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                   ANSWER = 3
```

---

## ⏱️ Time & Space Complexity

| Approach        | Time Complexity | Space Complexity | Notes                            |
|:----------------|:---------------:|:----------------:|:---------------------------------|
| **Brute Force** | **O(N²)**       | O(1)             | Recompute sums at every index    |
| **This Solution** | **O(N)**      | O(1)             | One pass after O(N) total sum    |

### Why Brute Force is Too Slow

```
N = 100,000

Brute Force: 100,000 × 100,000 = 10,000,000,000 ops  😱  TLE
This method:         100,000   =        100,000 ops  🚀  Instant
```

---

## 🧩 Complete Clean Solution

```python
def equilibrium_index(A):
    total_sum = sum(A)    # O(N) — compute once
    left_sum  = 0

    for i in range(len(A)):
        # Right sum derived from total — no separate loop needed
        right_sum = total_sum - left_sum - A[i]

        if left_sum == right_sum:
            return i       # First (minimum) equilibrium index

        left_sum += A[i]   # Slide left boundary forward

    return -1              # No equilibrium found


# Test
print(equilibrium_index([-7, 1, 5, 2, -4, 3, 0]))  # 3
print(equilibrium_index([1, 2, 3]))                  # -1
print(equilibrium_index([0]))                        # 0  ← single element
print(equilibrium_index([1, -1, 1, -1, 1]))          # 0
```

---

## 🗺️ Complete Visual Summary

```
ARRAY A:
┌────┬────┬────┬────┬────┬────┬────┐
│ -7 │  1 │  5 │  2 │ -4 │  3 │  0 │
└────┴────┴────┴────┴────┴────┴────┘
  i=0  i=1  i=2  i=3  i=4  i=5  i=6

total_sum = 0

SCAN LEFT → RIGHT:
  i=0: left=0,  right=0−0−(−7)=7  → 0≠7   left becomes −7
  i=1: left=−7, right=0−(−7)−1=6  → −7≠6  left becomes −6
  i=2: left=−6, right=0−(−6)−5=1  → −6≠1  left becomes −1
  i=3: left=−1, right=0−(−1)−2=−1 → −1==−1 ✅ RETURN 3

SEESAW AT i=3:
  ┌───────────┐     ┌───────────┐
  │ -7 + 1 + 5│     │-4 + 3 + 0 │
  │   = -1    │ ⚖️  │   = -1    │
  └───────────┘     └───────────┘
      LEFT            RIGHT
         PERFECTLY BALANCED!
```

---

## ⚠️ Edge Cases & Pitfalls

### 1. Single Element Array

```python
A = [5]
# i=0: left_sum=0, right_sum=5−0−5=0 → 0==0 ✅
# Answer: 0
```
A single element is always an equilibrium index — nothing on either side means both sides sum to 0.

---

### 2. All Zeros

```python
A = [0, 0, 0, 0]
# Every index is an equilibrium index!
# Return minimum → 0
```

---

### 3. Negative Numbers

```python
A = [-5, 5, 0, -5, 5]
# total_sum = 0
# i=2: left_sum = -5+5 = 0, right_sum = 0−0−0 = 0 → 0==0 ✅
# Answer: 2
```
Works perfectly — the formula handles negatives naturally.

---

### 4. First or Last Index as Equilibrium

```python
A = [0, 1, -1]
# i=0: left_sum=0, right_sum=0−0−0=0 → 0==0 ✅
# Answer: 0  ← left side is empty (sum=0)

A = [-1, 1, 0]
# i=2: left_sum=0, right_sum=0−0−0=0 → 0==0 ✅
# Answer: 2  ← right side is empty (sum=0)
```

---

### 5. Multiple Equilibrium Indexes

```python
A = [1, 0, -1, 0, 1]
# Multiple equilibrium points may exist
# The loop returns the FIRST one found (minimum index) ✅
```

---

## 🔁 Alternative Approach — Using Prefix Sum Array

If you've already built a prefix sum array, you can use it directly:

```python
def equilibrium_prefix(A):
    n = len(A)
    prefix = [0] * (n + 1)

    # Build prefix sum: prefix[i] = A[0] + A[1] + ... + A[i-1]
    for i in range(n):
        prefix[i + 1] = prefix[i] + A[i]

    # prefix[i]     = sum of elements BEFORE index i  (left sum)
    # prefix[n] - prefix[i+1] = sum of elements AFTER index i (right sum)
    for i in range(n):
        left_sum  = prefix[i]
        right_sum = prefix[n] - prefix[i + 1]
        if left_sum == right_sum:
            return i

    return -1
```

Both approaches are **O(N)** time. The single-pass approach uses **O(1)** space.

---

## 🧪 Test It Yourself

```python
test_cases = [
    ([-7, 1, 5, 2, -4, 3, 0],  3),   # Standard case
    ([1, 2, 3],                 -1),  # No equilibrium
    ([0],                        0),  # Single element
    ([1, -1, 1, -1, 1],          0),  # First index
    ([-1, 1, 0],                 2),  # Last index
    ([0, 0, 0],                  0),  # All zeros → minimum
    ([2, 4, 2],                  1),  # Middle
]

for A, expected in test_cases:
    result = equilibrium_index(A)
    status = "✅" if result == expected else "❌"
    print(f"{status}  A={A}  →  got {result}, expected {expected}")
```

---

## 📚 Related Problems to Practice Next

| Problem | Key Idea |
|:--------|:---------|
| **Find pivot index** (LeetCode 724) | Identical to this problem |
| **Subarray sum equals K** | Prefix sum + hashmap |
| **Trapping Rain Water** | Left-max and right-max arrays |
| **Maximum subarray** | Kadane's algorithm |
| **Product of array except self** | Left and right product arrays |
| **Split array with equal sum** | Extension of equilibrium concept |

---

> ✍️ **The Big Idea:**
> Instead of recomputing left and right sums from scratch at every index (O(N²)),
> use the relationship:
> **`right_sum = total_sum − left_sum − A[i]`**
> to derive the right sum in O(1), reducing the entire problem to a single O(N) pass.
> The equilibrium index is where left and right sums meet — the perfect balance point.

---

*Happy Coding! 🚀*
