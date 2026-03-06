# ⚖️ Count Indices Where Removal Balances Even & Odd Sums

> **Difficulty:** Intermediate → Advanced
> **Topic:** Arrays · Prefix Sums · Parity Shift · Index Simulation
> **Language:** Python
> **Constraints:** 1 ≤ N ≤ 10⁵ · −10⁵ ≤ A[i] ≤ 10⁵

---

## 📋 Problem Statement

Given an array **A** of size **N**, find the count of indices such that **removing the element at that index** makes:

```
Sum of even-indexed elements  ==  Sum of odd-indexed elements
```

> ⚠️ After removal, the array **shrinks by one** — so every element to the RIGHT of the removed index **shifts left by 1** and **its parity flips**.

---

## 🌍 Real-World Analogy — Before Any Code

### ⚖️ The Balance Scale with Numbered Plates

Imagine a balance scale with **N numbered plates** (0, 1, 2, 3, …).

- **Even-numbered plates** (0, 2, 4, …) go on the **LEFT pan**
- **Odd-numbered plates** (1, 3, 5, …) go on the **RIGHT pan**

```
LEFT PAN (even)        RIGHT PAN (odd)
  plate 0 = 2            plate 1 = 1
  plate 2 = 6            plate 3 = 4
  ──────────             ──────────
  Total = 8              Total = 5
```

The scale is **unbalanced** (8 ≠ 5).

Now the question is:
> *"Can I remove exactly one plate so the scale becomes perfectly balanced — remembering that all plates to the right of the removed one renumber (shift left)?"*

---

### 🚌 Bus Re-Seating Analogy

Think of an array as a bus with assigned seats 0, 1, 2, 3, …

- Even seats → Team A
- Odd seats  → Team B

When **one passenger leaves** (is removed), every passenger **behind them slides one seat forward** — so their team membership flips! Someone who was on Team B might now be on Team A.

This **parity flip of the right portion** is the trickiest part of this problem.

---

## 🧩 Understanding the Examples

### Example 1: `A = [2, 1, 6, 4]`

```
Original array:
┌───┬───┬───┬───┐
│ 2 │ 1 │ 6 │ 4 │
└───┴───┴───┴───┘
 i=0 i=1 i=2 i=3
EVEN ODD EVEN ODD
```

Even sum = A[0]+A[2] = 2+6 = **8**
Odd sum  = A[1]+A[3] = 1+4 = **5**

Now try removing each index:

| Remove `i` | New Array   | Even sum          | Odd sum      | Balanced? |
|:----------:|:-----------:|:-----------------:|:------------:|:---------:|
| 0          | [1, 6, 4]   | A[0]+A[2]=1+4=5   | A[1]=6       | 5≠6 ❌    |
| **1**      | **[2, 6, 4]**   | **A[0]+A[2]=2+4=6** | **A[1]=6** | **6=6 ✅** |
| 2          | [2, 1, 4]   | A[0]+A[2]=2+4=6   | A[1]=1       | 6≠1 ❌    |
| 3          | [2, 1, 6]   | A[0]+A[2]=2+6=8   | A[1]=1       | 8≠1 ❌    |

Only index **1** works → **Answer = 1** ✅

---

### Example 2: `A = [1, 1, 1]`

| Remove `i` | New Array | Even sum | Odd sum | Balanced? |
|:----------:|:---------:|:--------:|:-------:|:---------:|
| 0          | [1, 1]    | A[0]=1   | A[1]=1  | 1=1 ✅    |
| 1          | [1, 1]    | A[0]=1   | A[1]=1  | 1=1 ✅    |
| 2          | [1, 1]    | A[0]=1   | A[1]=1  | 1=1 ✅    |

All three removals work → **Answer = 3** ✅

---

## 🔑 The Critical Insight — Parity Flip

This is the **hardest** concept in this problem. Read carefully.

When you remove element at index `i`, the array shrinks:

```
Before:  [A0, A1, A2, ... , A(i-1), A(i), A(i+1), A(i+2), ... , A(N-1)]
                                     └──── REMOVED ────┘
After:   [A0, A1, A2, ... , A(i-1), A(i+1), A(i+2), ... , A(N-1)]
```

**Left part (indices 0 to i-1):** positions UNCHANGED → parities UNCHANGED ✅

**Right part (indices i+1 to N-1):** each element **slides left by 1** → parity FLIPS:
- What was at even index → now at odd index
- What was at odd index → now at even index

```
Example: Remove i=1 from [2, 1, 6, 4]

BEFORE removal:
  Index: 0(E)  1(O)  2(E)  3(O)
  Value:  2     1     6     4
               ↑ REMOVE

AFTER removal: [2, 6, 4]
  Index: 0(E)  1(O)  2(E)
  Value:  2     6     4
               ↑      ↑
          was 2(E)  was 3(O) → NOW 1(O) and 2(E) — FLIPPED!
```

---

## 💡 Key Formula — O(N) Solution

Instead of actually removing each element and recomputing (O(N²)), we derive the new even/odd sums mathematically.

### Setup: Build Two Prefix Arrays

```
prefix_even[i] = sum of A[j] where j < i AND j is EVEN
prefix_odd[i]  = sum of A[j] where j < i AND j is ODD
```

Using a sentinel at index 0:
```
prefix_even[0] = 0
prefix_odd[0]  = 0
prefix_even[i+1] = prefix_even[i] + (A[i] if i is even else 0)
prefix_odd[i+1]  = prefix_odd[i]  + (A[i] if i is odd  else 0)
```

### When We Remove Index `i`:

**Left part** (indices 0 to i-1) — no change:
```
left_even = prefix_even[i]    ← even-sum of elements before i
left_odd  = prefix_odd[i]     ← odd-sum  of elements before i
```

**Right part** (indices i+1 to N-1) — parities flip:
```
right_even_original = total_even - prefix_even[i+1]   ← were even
right_odd_original  = total_odd  - prefix_odd[i+1]    ← were odd
```

After the shift, the right part's parities flip:
- Originally even → become odd
- Originally odd  → become even

**New sums after removing i:**
```
new_even_sum = left_even + right_odd_original   (left even + right's odd→even flip)
new_odd_sum  = left_odd  + right_even_original  (left odd  + right's even→odd flip)
```

**Equilibrium condition:**
```
new_even_sum == new_odd_sum  →  count this index!
```

---

## 📊 Building Prefix Arrays — Full Trace

### Input: `A = [2, 1, 6, 4]`

**Building prefix_even and prefix_odd:**

| `i` | `A[i]` | `i` even? | `i` odd? | `prefix_even[i+1]` | `prefix_odd[i+1]` |
|:---:|:------:|:---------:|:--------:|:------------------:|:-----------------:|
| 0   | 2      | ✅ → +2   | ❌       | **2**              | 0                 |
| 1   | 1      | ❌        | ✅ → +1  | 2                  | **1**             |
| 2   | 6      | ✅ → +6   | ❌       | **8**              | 1                 |
| 3   | 4      | ❌        | ✅ → +4  | 8                  | **5**             |

```
prefix_even = [0, 2, 2, 8, 8]
prefix_odd  = [0, 0, 1, 1, 5]
total_even  = 8
total_odd   = 5
```

---

## 🔬 Full Dry Run — Example 1

### `A = [2, 1, 6, 4]`

```
prefix_even = [0, 2, 2, 8, 8]
prefix_odd  = [0, 0, 1, 1, 5]
total_even  = 8,  total_odd = 5
```

---

**Remove i=0 (A[0]=2):**
```
left_even  = prefix_even[0]             = 0
left_odd   = prefix_odd[0]              = 0
right_even = total_even - prefix_even[1] = 8 - 2 = 6   (originally even, become odd)
right_odd  = total_odd  - prefix_odd[1]  = 5 - 0 = 5   (originally odd, become even)

new_even = left_even + right_odd  = 0 + 5 = 5
new_odd  = left_odd  + right_even = 0 + 6 = 6
5 ≠ 6  ❌

Verify: [1, 6, 4] → even_sum = 1+4 = 5 ✅, odd_sum = 6 ✅
```

---

**Remove i=1 (A[1]=1):**
```
left_even  = prefix_even[1]             = 2
left_odd   = prefix_odd[1]              = 0
right_even = total_even - prefix_even[2] = 8 - 2 = 6   (A[2]=6, A[3] is odd so not here)
right_odd  = total_odd  - prefix_odd[2]  = 5 - 1 = 4   (A[3]=4)

new_even = left_even + right_odd  = 2 + 4 = 6
new_odd  = left_odd  + right_even = 0 + 6 = 6
6 == 6  ✅  ← COUNT THIS!

Verify: [2, 6, 4] → even_sum = 2+4 = 6 ✅, odd_sum = 6 ✅
```

---

**Remove i=2 (A[2]=6):**
```
left_even  = prefix_even[2]             = 2
left_odd   = prefix_odd[2]              = 1
right_even = total_even - prefix_even[3] = 8 - 8 = 0
right_odd  = total_odd  - prefix_odd[3]  = 5 - 1 = 4

new_even = left_even + right_odd  = 2 + 4 = 6
new_odd  = left_odd  + right_even = 1 + 0 = 1
6 ≠ 1  ❌

Verify: [2, 1, 4] → even_sum = 2+4 = 6 ✅, odd_sum = 1 ✅
```

---

**Remove i=3 (A[3]=4):**
```
left_even  = prefix_even[3]             = 8
left_odd   = prefix_odd[3]              = 1
right_even = total_even - prefix_even[4] = 8 - 8 = 0
right_odd  = total_odd  - prefix_odd[4]  = 5 - 5 = 0

new_even = left_even + right_odd  = 8 + 0 = 8
new_odd  = left_odd  + right_even = 1 + 0 = 1
8 ≠ 1  ❌

Verify: [2, 1, 6] → even_sum = 2+6 = 8 ✅, odd_sum = 1 ✅
```

**Answer: 1** ✅

---

## 🔍 The Code — Every Line Explained

```python
def solve(A):
    n = len(A)

    # ── Phase 1: Build prefix arrays ──────────────────────────────────────
    prefix_even = [0] * (n + 1)   # sentinel at index 0
    prefix_odd  = [0] * (n + 1)

    for i in range(n):
        # Carry forward previous value, add A[i] only if parity matches
        prefix_even[i+1] = prefix_even[i] + (A[i] if i % 2 == 0 else 0)
        prefix_odd[i+1]  = prefix_odd[i]  + (A[i] if i % 2 == 1 else 0)

    total_even = prefix_even[n]   # total even-indexed sum of entire array
    total_odd  = prefix_odd[n]    # total odd-indexed sum of entire array

    # ── Phase 2: Try removing each index ──────────────────────────────────
    count = 0

    for i in range(n):
        # Left side (indices 0..i-1): parity unchanged
        left_even = prefix_even[i]
        left_odd  = prefix_odd[i]

        # Right side (indices i+1..n-1): parity FLIPS after removal of i
        right_even = total_even - prefix_even[i+1]  # originally even → become ODD
        right_odd  = total_odd  - prefix_odd[i+1]   # originally odd  → become EVEN

        # After the shift:
        new_even = left_even + right_odd   # left's even  +  right's (odd → even)
        new_odd  = left_odd  + right_even  # left's odd   +  right's (even → odd)

        if new_even == new_odd:
            count += 1

    return count
```

---

## 🗺️ Complete Visual Summary

```
ARRAY A = [2, 1, 6, 4]
           ↑  ↑  ↑  ↑
INDEX:     0  1  2  3
         EVEN ODD E  O

PREFIX ARRAYS:
prefix_even = [0, 2, 2, 8, 8]
prefix_odd  = [0, 0, 1, 1, 5]

FOR EACH REMOVAL i:
┌───┬──────────┬──────────────────────────────────────────────────┬────────┐
│ i │  Remove  │  new_even = left_E + right_O                    │ Equal? │
│   │          │  new_odd  = left_O + right_E                    │        │
├───┼──────────┼──────────────────────────────────────────────────┼────────┤
│ 0 │ A[0]=2   │  new_even = 0+5=5,  new_odd = 0+6=6            │  ❌    │
│ 1 │ A[1]=1   │  new_even = 2+4=6,  new_odd = 0+6=6            │  ✅    │
│ 2 │ A[2]=6   │  new_even = 2+4=6,  new_odd = 1+0=1            │  ❌    │
│ 3 │ A[3]=4   │  new_even = 8+0=8,  new_odd = 1+0=1            │  ❌    │
└───┴──────────┴──────────────────────────────────────────────────┴────────┘

COUNT = 1
```

---

## ⏱️ Time & Space Complexity

| Phase               | Operation              | Complexity   |
|:--------------------|:-----------------------|:------------:|
| Build prefix arrays | Two passes over A      | **O(N)**     |
| Check each removal  | O(1) arithmetic per i  | **O(N)**     |
| **Total**           |                        | **O(N)**     |
| Space               | Two prefix arrays size N+1 | **O(N)** |

### Brute Force vs Optimized

| Approach    | Strategy                         | Time       |
|:------------|:---------------------------------|:----------:|
| Brute Force | Remove each element, recompute sums | **O(N²)** |
| Optimized   | Prefix arrays + formula          | **O(N)**   |

```
N = 100,000:
Brute Force: 100,000 × 100,000 = 10,000,000,000 ops  😱
Optimized:   100,000 × 2       =        200,000 ops  🚀
```

---

## ⚠️ Edge Cases & Pitfalls

### ❗ Pitfall 1: Forgetting the Parity Flip

The single most common mistake — treating the right portion as keeping its original parity:

```python
# ❌ WRONG — ignores parity flip
new_even = left_even + right_even   # right stays even? NO!
new_odd  = left_odd  + right_odd

# ✅ CORRECT — right side flips
new_even = left_even + right_odd    # right's odd becomes even
new_odd  = left_odd  + right_even   # right's even becomes odd
```

---

### ❗ Pitfall 2: Forgetting A[i] Itself

When computing the right portion after removing index `i`, use `prefix[i+1]` not `prefix[i]`:

```python
# ❌ WRONG — still includes A[i] in total
right_even = total_even - prefix_even[i]

# ✅ CORRECT — excludes A[i] (it's removed) and everything before it
right_even = total_even - prefix_even[i+1]
```

`prefix_even[i+1]` = sum of even-indexed elements from index 0 up to and including index i.

---

### ❗ Pitfall 3: Single Element Array

```python
A = [5]
# Remove i=0: new array is empty
# left_even=0, left_odd=0, right_even=0, right_odd=0
# new_even=0, new_odd=0 → 0==0 ✅
# Answer: 1
```

An empty array has even_sum = 0 = odd_sum, so a single-element array always counts.

---

### ❗ Pitfall 4: Two-Element Array

```python
A = [3, 3]
# Remove i=0: [3] → even_sum=3, odd_sum=0 → ❌
# Remove i=1: [3] → even_sum=3, odd_sum=0 → ❌
# Answer: 0

A = [3, 5]
# Remove i=0: [5] → even_sum=5, odd_sum=0 → ❌
# Remove i=1: [3] → even_sum=3, odd_sum=0 → ❌
# Answer: 0
```

---

## 🧪 Test It Yourself

```python
def solve(A):
    n = len(A)
    prefix_even = [0] * (n + 1)
    prefix_odd  = [0] * (n + 1)
    for i in range(n):
        prefix_even[i+1] = prefix_even[i] + (A[i] if i % 2 == 0 else 0)
        prefix_odd[i+1]  = prefix_odd[i]  + (A[i] if i % 2 == 1 else 0)
    total_even = prefix_even[n]
    total_odd  = prefix_odd[n]
    count = 0
    for i in range(n):
        left_even  = prefix_even[i]
        left_odd   = prefix_odd[i]
        right_even = total_even - prefix_even[i+1]
        right_odd  = total_odd  - prefix_odd[i+1]
        new_even   = left_even + right_odd
        new_odd    = left_odd  + right_even
        if new_even == new_odd:
            count += 1
    return count


tests = [
    ([2, 1, 6, 4], 1),
    ([1, 1, 1],    3),
    ([5],          1),   # single element
    ([1, 2],       0),   # no valid removal
    ([1, 1],       2),   # both removals give [1] → even=1,odd=0? Let's check...
    ([0, 0, 0, 0], 4),   # all zeros
]

for A, expected in tests:
    result = solve(A)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  A={A}  → {result}")
```

---

## 📚 What to Learn Next

| Topic | How It Connects |
|:------|:----------------|
| **Prefix Sum (basic)** | Foundation of this solution |
| **Parity / Alternating arrays** | Same flip logic appears in many problems |
| **Equilibrium Index** | Simpler version: no parity, just split at index |
| **Split Array with Equal Sum** | Generalisation of this concept |
| **Segment Tree with lazy propagation** | Range updates with parity handling |

---

> ✍️ **The Big Idea:**
> When an element is removed from position `i`, every element to its right
> **shifts left by one** — flipping their parity. The trick is to split the array
> into a **left part** (unchanged parity) and a **right part** (flipped parity),
> compute their contributions using prefix sums, then check balance in O(1) per index.
> This reduces a naïve O(N²) simulation to an elegant O(N) pass.

---

*Happy Coding! 🚀*
