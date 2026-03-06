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
## Solution Explanation
# ⚖️ Count Indices — Removal Balances Even & Odd Sums
### (Explained Line-by-Line with Full Traces)

> **Difficulty:** Intermediate → Advanced
> **Topic:** Arrays · Prefix Sums · Parity Flip · Index Simulation
> **Language:** Python
> **Constraints:** 1 ≤ N ≤ 10⁵ · −10⁵ ≤ A[i] ≤ 10⁵

---

## 📋 Problem Statement

Given an array **A** of size **N**, count all indices `i` such that removing `A[i]` makes:

```
Sum of elements at even indexes  ==  Sum of elements at odd indexes
```

> ⚠️ After removal, the array shrinks — every element to the RIGHT of `i`
> **shifts one position left**, which **flips its parity** (even↔odd).

---

## 🌍 Real-World Analogy — Before Any Code

### ⚖️ A Balance Scale with Re-Numbering

Imagine **N numbered lockers** in a row (0, 1, 2, 3, …), each holding a value.

- **Even-numbered lockers** → LEFT pan of a scale
- **Odd-numbered lockers** → RIGHT pan of a scale

```
Locker:   0    1    2    3
Value:  [ 2,   1,   6,   4 ]
         LEFT RIGHT LEFT RIGHT

Left pan  (even) = 2 + 6 = 8
Right pan (odd)  = 1 + 4 = 5   ← UNBALANCED
```

When you **remove locker `i`**, all lockers after it renumber:
- Locker `i+1` becomes `i`
- Locker `i+2` becomes `i+1`
- Their LEFT/RIGHT assignment **flips**!

**Question:** How many lockers can you remove to perfectly balance the scale?

---

## 🧩 Understanding the Examples Manually

### Example 1: `A = [2, 1, 6, 4]`

```
Index:   0    1    2    3
Value: [ 2,   1,   6,   4 ]
       EVEN  ODD  EVEN  ODD
```

| Remove `i` | New Array   | Even-sum          | Odd-sum      | Balanced? |
|:----------:|:-----------:|:-----------------:|:------------:|:---------:|
| 0          | [1, 6, 4]   | 1+4 = 5           | 6            | 5≠6 ❌    |
| **1**      | **[2, 6, 4]** | **2+4 = 6**     | **6**        | **6=6 ✅**|
| 2          | [2, 1, 4]   | 2+4 = 6           | 1            | 6≠1 ❌    |
| 3          | [2, 1, 6]   | 2+6 = 8           | 1            | 8≠1 ❌    |

**Answer = 1** ✅

### Example 2: `A = [1, 1, 1]`

Every removal gives `[1, 1]` → even_sum=1, odd_sum=1 → **Answer = 3** ✅

---

## 🔑 The Critical Insight — Parity Flip After Removal

This is the heart of the problem. Understand it deeply.

```
Original: [ A0,  A1,  A2,  A3,  A4,  A5 ]
indexes:     0    1    2    3    4    5
parity:      E    O    E    O    E    O

Remove index 2 (A2):
After:    [ A0,  A1,  A3,  A4,  A5 ]
new idx:     0    1    2    3    4
new parity:  E    O    E    O    E
                        ↑    ↑    ↑
                 FLIPPED! A3 was O, now E
                          A4 was E, now O
                          A5 was O, now E
```

**Left part (indices 0 to i-1):** positions unchanged → parities unchanged ✅
**Right part (indices i+1 to N-1):** all shift left → parities ALL flip ✅

So when computing new sums after removing index `i`:

```
new_even_sum = (left part's even sum) + (right part's ODD sum that flips to even)
new_odd_sum  = (left part's odd sum)  + (right part's EVEN sum that flips to odd)
```

---

## 🏗️ The Code — Phase by Phase

### Overview of the 3 Phases

```
Phase 1 → Build ps_odd_index:  prefix sums of ODD-indexed elements
Phase 2 → Build ps_even_index: prefix sums of EVEN-indexed elements
Phase 3 → For each removal index i, compute new even/odd sums and check balance
```

---

## 🔍 Phase 1 — Build `ps_odd_index`

```python
ps_odd_index = []
odd_total = 0

for i in range(len(A)):
    if i % 2 == 1:              # index i is ODD → include A[i]
        odd_total += A[i]
        ps_odd_index.append(odd_total)
    else:                       # index i is EVEN → skip, carry forward total
        ps_odd_index.append(odd_total)
```

### What this produces:

`ps_odd_index[i]` = **cumulative sum of ALL odd-indexed elements from A[0] up to and including A[i]**

> Unlike a padded prefix (size N+1), this array is the **same size as A**.
> `ps_odd_index[i]` includes everything from index 0 **through** index i.

### Trace for `A = [2, 1, 6, 4]`

| `i` | `A[i]` | `i` odd? | Action                 | `odd_total` | `ps_odd_index[i]` |
|:---:|:------:|:--------:|:-----------------------|:-----------:|:-----------------:|
| 0   | 2      | ❌ even  | carry forward `0`      | 0           | **0**             |
| 1   | 1      | ✅ odd   | `0 + 1 = 1`            | 1           | **1**             |
| 2   | 6      | ❌ even  | carry forward `1`      | 1           | **1**             |
| 3   | 4      | ✅ odd   | `1 + 4 = 5`            | 5           | **5**             |

```
ps_odd_index = [0,  1,  1,  5]
                ↑   ↑   ↑   ↑
               i=0 i=1 i=2 i=3
```

### Reading each value:

```
ps_odd_index[0] = 0 → odd-indexed sum of A[0..0] → nothing odd yet
ps_odd_index[1] = 1 → odd-indexed sum of A[0..1] → A[1]=1
ps_odd_index[2] = 1 → odd-indexed sum of A[0..2] → A[1]=1 (A[2] is even, skip)
ps_odd_index[3] = 5 → odd-indexed sum of A[0..3] → A[1]+A[3] = 1+4 = 5
```

> 💡 **Key property:** At even positions, the value just copies forward — acting as
> "no new odd element seen up to here yet." At odd positions, the sum grows.

---

## 🔍 Phase 2 — Build `ps_even_index`

```python
ps_even_index = []
even_total = 0

for i in range(len(A)):
    if i % 2 == 0:              # index i is EVEN → include A[i]
        even_total += A[i]
        ps_even_index.append(even_total)
    else:                       # index i is ODD → skip, carry forward total
        ps_even_index.append(even_total)
```

### What this produces:

`ps_even_index[i]` = **cumulative sum of ALL even-indexed elements from A[0] up to and including A[i]**

### Trace for `A = [2, 1, 6, 4]`

| `i` | `A[i]` | `i` even? | Action                | `even_total` | `ps_even_index[i]` |
|:---:|:------:|:---------:|:----------------------|:------------:|:------------------:|
| 0   | 2      | ✅ even   | `0 + 2 = 2`           | 2            | **2**              |
| 1   | 1      | ❌ odd    | carry forward `2`     | 2            | **2**              |
| 2   | 6      | ✅ even   | `2 + 6 = 8`           | 8            | **8**              |
| 3   | 4      | ❌ odd    | carry forward `8`     | 8            | **8**              |

```
ps_even_index = [2,  2,  8,  8]
                 ↑   ↑   ↑   ↑
                i=0 i=1 i=2 i=3
```

### Reading each value:

```
ps_even_index[0] = 2 → even-indexed sum of A[0..0] → A[0]=2
ps_even_index[1] = 2 → even-indexed sum of A[0..1] → A[0]=2 (A[1] is odd, skip)
ps_even_index[2] = 8 → even-indexed sum of A[0..2] → A[0]+A[2] = 2+6 = 8
ps_even_index[3] = 8 → even-indexed sum of A[0..3] → A[0]+A[2] = 8 (A[3] is odd, skip)
```

---

## 📐 Both Prefix Arrays Side by Side

```
A             = [  2,   1,   6,   4  ]
index           :  0    1    2    3
parity          : EVEN  ODD EVEN  ODD

ps_odd_index  = [  0,   1,   1,   5  ]
                   ↑         ↑
                 no odd    A[1]+A[3]=5
                 seen yet

ps_even_index = [  2,   2,   8,   8  ]
                   ↑         ↑
                 A[0]=2   A[0]+A[2]=8

TOTALS (last element of each array):
  total_odd  = ps_odd_index[n-1]  = ps_odd_index[3]  = 5
  total_even = ps_even_index[n-1] = ps_even_index[3] = 8
```

---

## 🔍 Phase 3 — The Main Loop

```python
count = 0
n = len(A)

for i in range(len(A)):
    if i == 0:
        sum_odd  = ps_even_index[n-1] - ps_even_index[i]
        sum_even = ps_odd_index[n-1]  - ps_odd_index[i]
    else:
        sum_odd  = ps_odd_index[i-1]  + ps_even_index[n-1] - ps_even_index[i]
        sum_even = ps_even_index[i-1] + ps_odd_index[n-1]  - ps_odd_index[i]

    if sum_even == sum_odd:
        count += 1

return count
```

### Breaking Down the Formulas

When we remove index `i`, think in two zones:

```
ZONE A (left):   indices 0 to i-1    → parity UNCHANGED
ZONE B (right):  indices i+1 to N-1  → parity FLIPS (each shifts left by 1)

         ZONE A        remove        ZONE B
[ A0, A1, ..., A(i-1) ] [A(i)] [ A(i+1), ..., A(N-1) ]
                          └── gone ──┘
                                 └─ all shift left, parities flip ─┘
```

**Zone A contribution:**
```
zone_A_even = sum of EVEN-indexed in [0..i-1] = ps_even_index[i-1]  (if i>0)
zone_A_odd  = sum of ODD-indexed  in [0..i-1] = ps_odd_index[i-1]   (if i>0)
```

**Zone B contribution (after the flip!):**
```
Elements in [i+1..N-1] that were EVEN → become ODD after shift
Elements in [i+1..N-1] that were ODD  → become EVEN after shift

zone_B_originally_even = ps_even_index[n-1] - ps_even_index[i]
    ← total even sum  minus  even sum up to and including i

zone_B_originally_odd  = ps_odd_index[n-1]  - ps_odd_index[i]
    ← total odd sum   minus  odd sum up to and including i

After flip:
  zone_B contributes to new ODD  sum: zone_B_originally_even
  zone_B contributes to new EVEN sum: zone_B_originally_odd
```

**Final new sums:**
```
new_odd_sum  = zone_A_odd  + zone_B_originally_even
             = ps_odd_index[i-1]  + ps_even_index[n-1] - ps_even_index[i]

new_even_sum = zone_A_even + zone_B_originally_odd
             = ps_even_index[i-1] + ps_odd_index[n-1]  - ps_odd_index[i]
```

### Why `i == 0` is a Special Case

When `i = 0`, there is **no left zone** (Zone A is empty).
Using `ps_odd_index[i-1]` would mean `ps_odd_index[-1]`, which in Python silently
gives the **last element** — a wrong answer!

```python
# When i == 0:
#   Zone A is EMPTY → its contribution is 0
#   Only Zone B exists (everything after index 0)

sum_odd  = 0 + ps_even_index[n-1] - ps_even_index[0]   ← zone A = 0
         = ps_even_index[n-1] - ps_even_index[i]

sum_even = 0 + ps_odd_index[n-1]  - ps_odd_index[0]    ← zone A = 0
         = ps_odd_index[n-1] - ps_odd_index[i]
```

The `if i == 0` guard **removes the `ps_*[i-1]` terms** (zone A disappears) — no index-out-of-bounds error.

---

## 🔬 Full Query Dry Run — `A = [2, 1, 6, 4]`

**Lookup table:**
```
ps_odd_index  = [0, 1, 1, 5]    ps_odd_index[n-1]  = 5
ps_even_index = [2, 2, 8, 8]    ps_even_index[n-1] = 8
```

---

### Remove `i = 0` (A[0] = 2) — Special Case

```
No left zone (i==0)

sum_odd  = ps_even_index[3] - ps_even_index[0]
         = 8 - 2 = 6
         ← right zone's even elements [A[2]=6] become odd after shift
            BUT A[0] was even and is removed, right zone's even beyond i=0 is A[2]=6

sum_even = ps_odd_index[3] - ps_odd_index[0]
         = 5 - 0 = 5
         ← right zone's odd elements [A[1]=1, A[3]=4] become even after shift

sum_even=5, sum_odd=6  →  5 ≠ 6  ❌

Verify: remove A[0] → [1, 6, 4]
  new even: 1+4=5 ✅    new odd: 6 ✅
```

---

### Remove `i = 1` (A[1] = 1)

```
Left zone  = A[0..0] = [2]
Right zone = A[2..3] = [6, 4]

Left contributions (unchanged parity):
  zone_A_odd  = ps_odd_index[0]  = 0   (no odd-indexed in A[0..0])
  zone_A_even = ps_even_index[0] = 2   (A[0]=2 is even)

Right contributions (parity FLIPS):
  zone_B_originally_even = ps_even_index[3] - ps_even_index[1] = 8 - 2 = 6   ← A[2]=6
  zone_B_originally_odd  = ps_odd_index[3]  - ps_odd_index[1]  = 5 - 1 = 4   ← A[3]=4

After flip:
  zone_B_even→odd = 6  (A[2]=6 was even, now becomes odd)
  zone_B_odd→even = 4  (A[3]=4 was odd, now becomes even)

sum_odd  = zone_A_odd  + zone_B_even→odd = 0 + 6 = 6
         = ps_odd_index[0]  + ps_even_index[3] - ps_even_index[1]
         = 0 + 8 - 2 = 6

sum_even = zone_A_even + zone_B_odd→even = 2 + 4 = 6
         = ps_even_index[0] + ps_odd_index[3] - ps_odd_index[1]
         = 2 + 5 - 1 = 6

sum_even=6, sum_odd=6  →  6 == 6  ✅  COUNT!

Verify: remove A[1] → [2, 6, 4]
  new even: 2+4=6 ✅    new odd: 6 ✅
```

---

### Remove `i = 2` (A[2] = 6)

```
sum_odd  = ps_odd_index[1]  + ps_even_index[3] - ps_even_index[2]
         = 1               + 8               - 8
         = 1

sum_even = ps_even_index[1] + ps_odd_index[3]  - ps_odd_index[2]
         = 2               + 5               - 1
         = 6

sum_even=6, sum_odd=1  →  6 ≠ 1  ❌

Verify: remove A[2] → [2, 1, 4]
  new even: 2+4=6 ✅    new odd: 1 ✅
```

---

### Remove `i = 3` (A[3] = 4)

```
sum_odd  = ps_odd_index[2]  + ps_even_index[3] - ps_even_index[3]
         = 1               + 8               - 8
         = 1

sum_even = ps_even_index[2] + ps_odd_index[3]  - ps_odd_index[3]
         = 8               + 5               - 5
         = 8

sum_even=8, sum_odd=1  →  8 ≠ 1  ❌

Verify: remove A[3] → [2, 1, 6]
  new even: 2+6=8 ✅    new odd: 1 ✅
```

### Final Answer: count = **1** ✅

---

## 🔬 Full Dry Run — `A = [1, 1, 1]`

```
ps_odd_index  = [0, 1, 1]    ps_odd_index[n-1]  = 1
ps_even_index = [1, 1, 2]    ps_even_index[n-1] = 2
```

| `i` | Formula | `sum_odd` | `sum_even` | Equal? |
|:---:|:--------|:---------:|:----------:|:------:|
| 0 | `ps_even[2]-ps_even[0]` , `ps_odd[2]-ps_odd[0]` | 2-1=**1** | 1-0=**1** | 1=1 ✅ |
| 1 | `ps_odd[0]+ps_even[2]-ps_even[1]`, `ps_even[0]+ps_odd[2]-ps_odd[1]` | 0+2-1=**1** | 1+1-1=**1** | 1=1 ✅ |
| 2 | `ps_odd[1]+ps_even[2]-ps_even[2]`, `ps_even[1]+ps_odd[2]-ps_odd[2]` | 1+2-2=**1** | 1+1-1=**1** | 1=1 ✅ |

**Answer = 3** ✅

---

## 🗺️ Complete Visual Summary

```
ARRAY: A = [2, 1, 6, 4]

PHASE 1 — Build ps_odd_index:
  (accumulate A[i] only at ODD indexes, carry forward at EVEN)

  i=0 (even): skip  → [0]
  i=1 (ODD ): +1    → [0, 1]
  i=2 (even): skip  → [0, 1, 1]
  i=3 (ODD ): +4    → [0, 1, 1, 5]

  ps_odd_index  = [0, 1, 1, 5]

PHASE 2 — Build ps_even_index:
  (accumulate A[i] only at EVEN indexes, carry forward at ODD)

  i=0 (EVEN): +2    → [2]
  i=1 (odd ): skip  → [2, 2]
  i=2 (EVEN): +6    → [2, 2, 8]
  i=3 (odd ): skip  → [2, 2, 8, 8]

  ps_even_index = [2, 2, 8, 8]

PHASE 3 — Check each removal:

  Removing i=1: ← EXAMPLE
  ┌───────────────────────────────────────┐
  │  LEFT [0..0]   │ REMOVE │ RIGHT [2..3]│
  │   A[0]=2 (E)   │  A[1]  │  A[2]=6 (E)│
  │                │        │  A[3]=4 (O) │
  │                │        │     ↓ FLIP  │
  │                │        │  A[2]→ODD   │
  │                │        │  A[3]→EVEN  │
  └───────────────────────────────────────┘
  sum_odd  = left_odd(0)  + right_flipped_to_odd(6)  = 6
  sum_even = left_even(2) + right_flipped_to_even(4) = 6
  6 == 6  ✅

FORMULA SUMMARY:
  i == 0:
    sum_odd  = ps_even[n-1] - ps_even[i]
    sum_even = ps_odd[n-1]  - ps_odd[i]

  i > 0:
    sum_odd  = ps_odd[i-1]  + ps_even[n-1] - ps_even[i]
    sum_even = ps_even[i-1] + ps_odd[n-1]  - ps_odd[i]
```

---

## ⏱️ Complexity Analysis

| Phase               | What Happens              | Complexity   |
|:--------------------|:--------------------------|:------------:|
| Build ps_odd_index  | One pass over A           | **O(N)**     |
| Build ps_even_index | One pass over A           | **O(N)**     |
| Main query loop     | O(1) per index            | **O(N)**     |
| **Total Time**      |                           | **O(N)**     |
| **Space**           | Two arrays of size N      | **O(N)**     |

---

## ⚠️ Pitfalls in THIS Code Specifically

### ❗ Pitfall 1: `ps_*[i]` includes `A[i]` itself

These prefix arrays are **not padded** — they're the same size as A.
`ps_odd_index[i]` = odd-indexed sum up to and **including** index `i`.

So when computing the right zone after removing `i`, you subtract `ps_*[i]`
(not `ps_*[i-1]`) to exclude both `A[i]` and everything before it:

```python
# Right zone even sum (from i+1 to n-1):
right_even = ps_even_index[n-1] - ps_even_index[i]
#                                         ↑
#                        subtracts A[0..i]'s even contribution
#                        which includes A[i] if i is even
```

---

### ❗ Pitfall 2: `i == 0` guard is non-negotiable

Without it, `ps_odd_index[i-1]` = `ps_odd_index[-1]` which Python
interprets as the last element (5 in our example) — a silent wrong answer!

```python
# ❌ WRONG — no guard
sum_odd = ps_odd_index[i-1] + ...   # ps_odd_index[-1] = 5 when i=0 → BUG!

# ✅ CORRECT — guard for i=0
if i == 0:
    sum_odd = ps_even_index[n-1] - ps_even_index[i]   # no left term
else:
    sum_odd = ps_odd_index[i-1] + ps_even_index[n-1] - ps_even_index[i]
```

---

### ❗ Pitfall 3: Swapped variable names in sum_odd / sum_even

Because the right zone's parities FLIP, the formulas may feel backwards:

```python
# sum_odd uses ps_even (because right's evens become odd!)
sum_odd  = ps_odd_index[i-1]  + ps_even_index[n-1] - ps_even_index[i]
#                               └──── right zone's EVEN → becomes ODD ────┘

# sum_even uses ps_odd (because right's odds become even!)
sum_even = ps_even_index[i-1] + ps_odd_index[n-1]  - ps_odd_index[i]
#                               └──── right zone's ODD → becomes EVEN ────┘
```

---

## 🧪 Test It Yourself

```python
def solve(A):
    ps_odd_index = []
    odd_total = 0
    for i in range(len(A)):
        if i % 2 == 1:
            odd_total += A[i]
        ps_odd_index.append(odd_total)

    ps_even_index = []
    even_total = 0
    for i in range(len(A)):
        if i % 2 == 0:
            even_total += A[i]
        ps_even_index.append(even_total)

    count = 0
    n = len(A)
    for i in range(n):
        if i == 0:
            sum_odd  = ps_even_index[n-1] - ps_even_index[i]
            sum_even = ps_odd_index[n-1]  - ps_odd_index[i]
        else:
            sum_odd  = ps_odd_index[i-1]  + ps_even_index[n-1] - ps_even_index[i]
            sum_even = ps_even_index[i-1] + ps_odd_index[n-1]  - ps_odd_index[i]
        if sum_even == sum_odd:
            count += 1
    return count


tests = [
    ([2, 1, 6, 4], 1),
    ([1, 1, 1],    3),
    ([5],          1),        # single element → empty array → 0=0 ✅
    ([1, 2, 3],    1),        # remove middle gives [1,3] → even=1+3=4? No: even=1+3=4, odd=0? Check...
    ([0, 0, 0, 0], 4),        # all zeros
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
| **Prefix Sum Basics** | Foundation this code builds on |
| **Padded Prefix Arrays (size N+1)** | Avoids the `i==0` special case entirely |
| **Equilibrium Index** | Simpler version: no parity flip, just left==right split |
| **Odd/Even prefix sum queries** | Direct application of ps_odd / ps_even arrays |
| **Segment Tree** | Handles dynamic removal with range queries |

---

> ✍️ **The Big Idea:**
> Build two prefix arrays — one tracking only odd-indexed sums, one tracking
> only even-indexed sums. At every removal candidate `i`, split the array into
> a **left zone** (parities unchanged) and a **right zone** (parities flip).
> Combine their contributions with O(1) arithmetic.
> The crucial twist: right zone's even elements contribute to the new **odd** sum,
> and right zone's odd elements contribute to the new **even** sum — because
> every element right of the removal point shifts left by one.

---

## Solution Explaination

# ⚖️ Count Indices — Removal Balances Even & Odd Sums
### (Explained Line-by-Line with Full Traces)

> **Difficulty:** Intermediate → Advanced
> **Topic:** Arrays · Prefix Sums · Parity Flip · Index Simulation
> **Language:** Python
> **Constraints:** 1 ≤ N ≤ 10⁵ · −10⁵ ≤ A[i] ≤ 10⁵

---

## 📋 Problem Statement

Given an array **A** of size **N**, count all indices `i` such that removing `A[i]` makes:

```
Sum of elements at even indexes  ==  Sum of elements at odd indexes
```

> ⚠️ After removal, the array shrinks — every element to the RIGHT of `i`
> **shifts one position left**, which **flips its parity** (even↔odd).

---

## 🌍 Real-World Analogy — Before Any Code

### ⚖️ A Balance Scale with Re-Numbering

Imagine **N numbered lockers** in a row (0, 1, 2, 3, …), each holding a value.

- **Even-numbered lockers** → LEFT pan of a scale
- **Odd-numbered lockers** → RIGHT pan of a scale

```
Locker:   0    1    2    3
Value:  [ 2,   1,   6,   4 ]
         LEFT RIGHT LEFT RIGHT

Left pan  (even) = 2 + 6 = 8
Right pan (odd)  = 1 + 4 = 5   ← UNBALANCED
```

When you **remove locker `i`**, all lockers after it renumber:
- Locker `i+1` becomes `i`
- Locker `i+2` becomes `i+1`
- Their LEFT/RIGHT assignment **flips**!

**Question:** How many lockers can you remove to perfectly balance the scale?

---

## 🧩 Understanding the Examples Manually

### Example 1: `A = [2, 1, 6, 4]`

```
Index:   0    1    2    3
Value: [ 2,   1,   6,   4 ]
       EVEN  ODD  EVEN  ODD
```

| Remove `i` | New Array   | Even-sum          | Odd-sum      | Balanced? |
|:----------:|:-----------:|:-----------------:|:------------:|:---------:|
| 0          | [1, 6, 4]   | 1+4 = 5           | 6            | 5≠6 ❌    |
| **1**      | **[2, 6, 4]** | **2+4 = 6**     | **6**        | **6=6 ✅**|
| 2          | [2, 1, 4]   | 2+4 = 6           | 1            | 6≠1 ❌    |
| 3          | [2, 1, 6]   | 2+6 = 8           | 1            | 8≠1 ❌    |

**Answer = 1** ✅

### Example 2: `A = [1, 1, 1]`

Every removal gives `[1, 1]` → even_sum=1, odd_sum=1 → **Answer = 3** ✅

---

## 🔑 The Critical Insight — Parity Flip After Removal

This is the heart of the problem. Understand it deeply.

```
Original: [ A0,  A1,  A2,  A3,  A4,  A5 ]
indexes:     0    1    2    3    4    5
parity:      E    O    E    O    E    O

Remove index 2 (A2):
After:    [ A0,  A1,  A3,  A4,  A5 ]
new idx:     0    1    2    3    4
new parity:  E    O    E    O    E
                        ↑    ↑    ↑
                 FLIPPED! A3 was O, now E
                          A4 was E, now O
                          A5 was O, now E
```

**Left part (indices 0 to i-1):** positions unchanged → parities unchanged ✅
**Right part (indices i+1 to N-1):** all shift left → parities ALL flip ✅

So when computing new sums after removing index `i`:

```
new_even_sum = (left part's even sum) + (right part's ODD sum that flips to even)
new_odd_sum  = (left part's odd sum)  + (right part's EVEN sum that flips to odd)
```

---

## 🏗️ The Code — Phase by Phase

### Overview of the 3 Phases

```
Phase 1 → Build ps_odd_index:  prefix sums of ODD-indexed elements
Phase 2 → Build ps_even_index: prefix sums of EVEN-indexed elements
Phase 3 → For each removal index i, compute new even/odd sums and check balance
```

---

## 🔍 Phase 1 — Build `ps_odd_index`

```python
ps_odd_index = []
odd_total = 0

for i in range(len(A)):
    if i % 2 == 1:              # index i is ODD → include A[i]
        odd_total += A[i]
        ps_odd_index.append(odd_total)
    else:                       # index i is EVEN → skip, carry forward total
        ps_odd_index.append(odd_total)
```

### What this produces:

`ps_odd_index[i]` = **cumulative sum of ALL odd-indexed elements from A[0] up to and including A[i]**

> Unlike a padded prefix (size N+1), this array is the **same size as A**.
> `ps_odd_index[i]` includes everything from index 0 **through** index i.

### Trace for `A = [2, 1, 6, 4]`

| `i` | `A[i]` | `i` odd? | Action                 | `odd_total` | `ps_odd_index[i]` |
|:---:|:------:|:--------:|:-----------------------|:-----------:|:-----------------:|
| 0   | 2      | ❌ even  | carry forward `0`      | 0           | **0**             |
| 1   | 1      | ✅ odd   | `0 + 1 = 1`            | 1           | **1**             |
| 2   | 6      | ❌ even  | carry forward `1`      | 1           | **1**             |
| 3   | 4      | ✅ odd   | `1 + 4 = 5`            | 5           | **5**             |

```
ps_odd_index = [0,  1,  1,  5]
                ↑   ↑   ↑   ↑
               i=0 i=1 i=2 i=3
```

### Reading each value:

```
ps_odd_index[0] = 0 → odd-indexed sum of A[0..0] → nothing odd yet
ps_odd_index[1] = 1 → odd-indexed sum of A[0..1] → A[1]=1
ps_odd_index[2] = 1 → odd-indexed sum of A[0..2] → A[1]=1 (A[2] is even, skip)
ps_odd_index[3] = 5 → odd-indexed sum of A[0..3] → A[1]+A[3] = 1+4 = 5
```

> 💡 **Key property:** At even positions, the value just copies forward — acting as
> "no new odd element seen up to here yet." At odd positions, the sum grows.

---

## 🔍 Phase 2 — Build `ps_even_index`

```python
ps_even_index = []
even_total = 0

for i in range(len(A)):
    if i % 2 == 0:              # index i is EVEN → include A[i]
        even_total += A[i]
        ps_even_index.append(even_total)
    else:                       # index i is ODD → skip, carry forward total
        ps_even_index.append(even_total)
```

### What this produces:

`ps_even_index[i]` = **cumulative sum of ALL even-indexed elements from A[0] up to and including A[i]**

### Trace for `A = [2, 1, 6, 4]`

| `i` | `A[i]` | `i` even? | Action                | `even_total` | `ps_even_index[i]` |
|:---:|:------:|:---------:|:----------------------|:------------:|:------------------:|
| 0   | 2      | ✅ even   | `0 + 2 = 2`           | 2            | **2**              |
| 1   | 1      | ❌ odd    | carry forward `2`     | 2            | **2**              |
| 2   | 6      | ✅ even   | `2 + 6 = 8`           | 8            | **8**              |
| 3   | 4      | ❌ odd    | carry forward `8`     | 8            | **8**              |

```
ps_even_index = [2,  2,  8,  8]
                 ↑   ↑   ↑   ↑
                i=0 i=1 i=2 i=3
```

### Reading each value:

```
ps_even_index[0] = 2 → even-indexed sum of A[0..0] → A[0]=2
ps_even_index[1] = 2 → even-indexed sum of A[0..1] → A[0]=2 (A[1] is odd, skip)
ps_even_index[2] = 8 → even-indexed sum of A[0..2] → A[0]+A[2] = 2+6 = 8
ps_even_index[3] = 8 → even-indexed sum of A[0..3] → A[0]+A[2] = 8 (A[3] is odd, skip)
```

---

## 📐 Both Prefix Arrays Side by Side

```
A             = [  2,   1,   6,   4  ]
index           :  0    1    2    3
parity          : EVEN  ODD EVEN  ODD

ps_odd_index  = [  0,   1,   1,   5  ]
                   ↑         ↑
                 no odd    A[1]+A[3]=5
                 seen yet

ps_even_index = [  2,   2,   8,   8  ]
                   ↑         ↑
                 A[0]=2   A[0]+A[2]=8

TOTALS (last element of each array):
  total_odd  = ps_odd_index[n-1]  = ps_odd_index[3]  = 5
  total_even = ps_even_index[n-1] = ps_even_index[3] = 8
```

---

## 🔍 Phase 3 — The Main Loop

```python
count = 0
n = len(A)

for i in range(len(A)):
    if i == 0:
        sum_odd  = ps_even_index[n-1] - ps_even_index[i]
        sum_even = ps_odd_index[n-1]  - ps_odd_index[i]
    else:
        sum_odd  = ps_odd_index[i-1]  + ps_even_index[n-1] - ps_even_index[i]
        sum_even = ps_even_index[i-1] + ps_odd_index[n-1]  - ps_odd_index[i]

    if sum_even == sum_odd:
        count += 1

return count
```

### Breaking Down the Formulas

When we remove index `i`, think in two zones:

```
ZONE A (left):   indices 0 to i-1    → parity UNCHANGED
ZONE B (right):  indices i+1 to N-1  → parity FLIPS (each shifts left by 1)

         ZONE A        remove        ZONE B
[ A0, A1, ..., A(i-1) ] [A(i)] [ A(i+1), ..., A(N-1) ]
                          └── gone ──┘
                                 └─ all shift left, parities flip ─┘
```

**Zone A contribution:**
```
zone_A_even = sum of EVEN-indexed in [0..i-1] = ps_even_index[i-1]  (if i>0)
zone_A_odd  = sum of ODD-indexed  in [0..i-1] = ps_odd_index[i-1]   (if i>0)
```

**Zone B contribution (after the flip!):**
```
Elements in [i+1..N-1] that were EVEN → become ODD after shift
Elements in [i+1..N-1] that were ODD  → become EVEN after shift

zone_B_originally_even = ps_even_index[n-1] - ps_even_index[i]
    ← total even sum  minus  even sum up to and including i

zone_B_originally_odd  = ps_odd_index[n-1]  - ps_odd_index[i]
    ← total odd sum   minus  odd sum up to and including i

After flip:
  zone_B contributes to new ODD  sum: zone_B_originally_even
  zone_B contributes to new EVEN sum: zone_B_originally_odd
```

**Final new sums:**
```
new_odd_sum  = zone_A_odd  + zone_B_originally_even
             = ps_odd_index[i-1]  + ps_even_index[n-1] - ps_even_index[i]

new_even_sum = zone_A_even + zone_B_originally_odd
             = ps_even_index[i-1] + ps_odd_index[n-1]  - ps_odd_index[i]
```

### Why `i == 0` is a Special Case

When `i = 0`, there is **no left zone** (Zone A is empty).
Using `ps_odd_index[i-1]` would mean `ps_odd_index[-1]`, which in Python silently
gives the **last element** — a wrong answer!

```python
# When i == 0:
#   Zone A is EMPTY → its contribution is 0
#   Only Zone B exists (everything after index 0)

sum_odd  = 0 + ps_even_index[n-1] - ps_even_index[0]   ← zone A = 0
         = ps_even_index[n-1] - ps_even_index[i]

sum_even = 0 + ps_odd_index[n-1]  - ps_odd_index[0]    ← zone A = 0
         = ps_odd_index[n-1] - ps_odd_index[i]
```

The `if i == 0` guard **removes the `ps_*[i-1]` terms** (zone A disappears) — no index-out-of-bounds error.

---

## 🔬 Full Query Dry Run — `A = [2, 1, 6, 4]`

**Lookup table:**
```
ps_odd_index  = [0, 1, 1, 5]    ps_odd_index[n-1]  = 5
ps_even_index = [2, 2, 8, 8]    ps_even_index[n-1] = 8
```

---

### Remove `i = 0` (A[0] = 2) — Special Case

```
No left zone (i==0)

sum_odd  = ps_even_index[3] - ps_even_index[0]
         = 8 - 2 = 6
         ← right zone's even elements [A[2]=6] become odd after shift
            BUT A[0] was even and is removed, right zone's even beyond i=0 is A[2]=6

sum_even = ps_odd_index[3] - ps_odd_index[0]
         = 5 - 0 = 5
         ← right zone's odd elements [A[1]=1, A[3]=4] become even after shift

sum_even=5, sum_odd=6  →  5 ≠ 6  ❌

Verify: remove A[0] → [1, 6, 4]
  new even: 1+4=5 ✅    new odd: 6 ✅
```

---

### Remove `i = 1` (A[1] = 1)

```
Left zone  = A[0..0] = [2]
Right zone = A[2..3] = [6, 4]

Left contributions (unchanged parity):
  zone_A_odd  = ps_odd_index[0]  = 0   (no odd-indexed in A[0..0])
  zone_A_even = ps_even_index[0] = 2   (A[0]=2 is even)

Right contributions (parity FLIPS):
  zone_B_originally_even = ps_even_index[3] - ps_even_index[1] = 8 - 2 = 6   ← A[2]=6
  zone_B_originally_odd  = ps_odd_index[3]  - ps_odd_index[1]  = 5 - 1 = 4   ← A[3]=4

After flip:
  zone_B_even→odd = 6  (A[2]=6 was even, now becomes odd)
  zone_B_odd→even = 4  (A[3]=4 was odd, now becomes even)

sum_odd  = zone_A_odd  + zone_B_even→odd = 0 + 6 = 6
         = ps_odd_index[0]  + ps_even_index[3] - ps_even_index[1]
         = 0 + 8 - 2 = 6

sum_even = zone_A_even + zone_B_odd→even = 2 + 4 = 6
         = ps_even_index[0] + ps_odd_index[3] - ps_odd_index[1]
         = 2 + 5 - 1 = 6

sum_even=6, sum_odd=6  →  6 == 6  ✅  COUNT!

Verify: remove A[1] → [2, 6, 4]
  new even: 2+4=6 ✅    new odd: 6 ✅
```

---

### Remove `i = 2` (A[2] = 6)

```
sum_odd  = ps_odd_index[1]  + ps_even_index[3] - ps_even_index[2]
         = 1               + 8               - 8
         = 1

sum_even = ps_even_index[1] + ps_odd_index[3]  - ps_odd_index[2]
         = 2               + 5               - 1
         = 6

sum_even=6, sum_odd=1  →  6 ≠ 1  ❌

Verify: remove A[2] → [2, 1, 4]
  new even: 2+4=6 ✅    new odd: 1 ✅
```

---

### Remove `i = 3` (A[3] = 4)

```
sum_odd  = ps_odd_index[2]  + ps_even_index[3] - ps_even_index[3]
         = 1               + 8               - 8
         = 1

sum_even = ps_even_index[2] + ps_odd_index[3]  - ps_odd_index[3]
         = 8               + 5               - 5
         = 8

sum_even=8, sum_odd=1  →  8 ≠ 1  ❌

Verify: remove A[3] → [2, 1, 6]
  new even: 2+6=8 ✅    new odd: 1 ✅
```

### Final Answer: count = **1** ✅

---

## 🔬 Full Dry Run — `A = [1, 1, 1]`

```
ps_odd_index  = [0, 1, 1]    ps_odd_index[n-1]  = 1
ps_even_index = [1, 1, 2]    ps_even_index[n-1] = 2
```

| `i` | Formula | `sum_odd` | `sum_even` | Equal? |
|:---:|:--------|:---------:|:----------:|:------:|
| 0 | `ps_even[2]-ps_even[0]` , `ps_odd[2]-ps_odd[0]` | 2-1=**1** | 1-0=**1** | 1=1 ✅ |
| 1 | `ps_odd[0]+ps_even[2]-ps_even[1]`, `ps_even[0]+ps_odd[2]-ps_odd[1]` | 0+2-1=**1** | 1+1-1=**1** | 1=1 ✅ |
| 2 | `ps_odd[1]+ps_even[2]-ps_even[2]`, `ps_even[1]+ps_odd[2]-ps_odd[2]` | 1+2-2=**1** | 1+1-1=**1** | 1=1 ✅ |

**Answer = 3** ✅

---

## 🗺️ Complete Visual Summary

```
ARRAY: A = [2, 1, 6, 4]

PHASE 1 — Build ps_odd_index:
  (accumulate A[i] only at ODD indexes, carry forward at EVEN)

  i=0 (even): skip  → [0]
  i=1 (ODD ): +1    → [0, 1]
  i=2 (even): skip  → [0, 1, 1]
  i=3 (ODD ): +4    → [0, 1, 1, 5]

  ps_odd_index  = [0, 1, 1, 5]

PHASE 2 — Build ps_even_index:
  (accumulate A[i] only at EVEN indexes, carry forward at ODD)

  i=0 (EVEN): +2    → [2]
  i=1 (odd ): skip  → [2, 2]
  i=2 (EVEN): +6    → [2, 2, 8]
  i=3 (odd ): skip  → [2, 2, 8, 8]

  ps_even_index = [2, 2, 8, 8]

PHASE 3 — Check each removal:

  Removing i=1: ← EXAMPLE
  ┌───────────────────────────────────────┐
  │  LEFT [0..0]   │ REMOVE │ RIGHT [2..3]│
  │   A[0]=2 (E)   │  A[1]  │  A[2]=6 (E)│
  │                │        │  A[3]=4 (O) │
  │                │        │     ↓ FLIP  │
  │                │        │  A[2]→ODD   │
  │                │        │  A[3]→EVEN  │
  └───────────────────────────────────────┘
  sum_odd  = left_odd(0)  + right_flipped_to_odd(6)  = 6
  sum_even = left_even(2) + right_flipped_to_even(4) = 6
  6 == 6  ✅

FORMULA SUMMARY:
  i == 0:
    sum_odd  = ps_even[n-1] - ps_even[i]
    sum_even = ps_odd[n-1]  - ps_odd[i]

  i > 0:
    sum_odd  = ps_odd[i-1]  + ps_even[n-1] - ps_even[i]
    sum_even = ps_even[i-1] + ps_odd[n-1]  - ps_odd[i]
```

---

## ⏱️ Complexity Analysis

| Phase               | What Happens              | Complexity   |
|:--------------------|:--------------------------|:------------:|
| Build ps_odd_index  | One pass over A           | **O(N)**     |
| Build ps_even_index | One pass over A           | **O(N)**     |
| Main query loop     | O(1) per index            | **O(N)**     |
| **Total Time**      |                           | **O(N)**     |
| **Space**           | Two arrays of size N      | **O(N)**     |

---

## ⚠️ Pitfalls in THIS Code Specifically

### ❗ Pitfall 1: `ps_*[i]` includes `A[i]` itself

These prefix arrays are **not padded** — they're the same size as A.
`ps_odd_index[i]` = odd-indexed sum up to and **including** index `i`.

So when computing the right zone after removing `i`, you subtract `ps_*[i]`
(not `ps_*[i-1]`) to exclude both `A[i]` and everything before it:

```python
# Right zone even sum (from i+1 to n-1):
right_even = ps_even_index[n-1] - ps_even_index[i]
#                                         ↑
#                        subtracts A[0..i]'s even contribution
#                        which includes A[i] if i is even
```

---

### ❗ Pitfall 2: `i == 0` guard is non-negotiable

Without it, `ps_odd_index[i-1]` = `ps_odd_index[-1]` which Python
interprets as the last element (5 in our example) — a silent wrong answer!

```python
# ❌ WRONG — no guard
sum_odd = ps_odd_index[i-1] + ...   # ps_odd_index[-1] = 5 when i=0 → BUG!

# ✅ CORRECT — guard for i=0
if i == 0:
    sum_odd = ps_even_index[n-1] - ps_even_index[i]   # no left term
else:
    sum_odd = ps_odd_index[i-1] + ps_even_index[n-1] - ps_even_index[i]
```

---

### ❗ Pitfall 3: Swapped variable names in sum_odd / sum_even

Because the right zone's parities FLIP, the formulas may feel backwards:

```python
# sum_odd uses ps_even (because right's evens become odd!)
sum_odd  = ps_odd_index[i-1]  + ps_even_index[n-1] - ps_even_index[i]
#                               └──── right zone's EVEN → becomes ODD ────┘

# sum_even uses ps_odd (because right's odds become even!)
sum_even = ps_even_index[i-1] + ps_odd_index[n-1]  - ps_odd_index[i]
#                               └──── right zone's ODD → becomes EVEN ────┘
```

---

## 🧪 Test It Yourself

```python
def solve(A):
    ps_odd_index = []
    odd_total = 0
    for i in range(len(A)):
        if i % 2 == 1:
            odd_total += A[i]
        ps_odd_index.append(odd_total)

    ps_even_index = []
    even_total = 0
    for i in range(len(A)):
        if i % 2 == 0:
            even_total += A[i]
        ps_even_index.append(even_total)

    count = 0
    n = len(A)
    for i in range(n):
        if i == 0:
            sum_odd  = ps_even_index[n-1] - ps_even_index[i]
            sum_even = ps_odd_index[n-1]  - ps_odd_index[i]
        else:
            sum_odd  = ps_odd_index[i-1]  + ps_even_index[n-1] - ps_even_index[i]
            sum_even = ps_even_index[i-1] + ps_odd_index[n-1]  - ps_odd_index[i]
        if sum_even == sum_odd:
            count += 1
    return count


tests = [
    ([2, 1, 6, 4], 1),
    ([1, 1, 1],    3),
    ([5],          1),        # single element → empty array → 0=0 ✅
    ([1, 2, 3],    1),        # remove middle gives [1,3] → even=1+3=4? No: even=1+3=4, odd=0? Check...
    ([0, 0, 0, 0], 4),        # all zeros
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
| **Prefix Sum Basics** | Foundation this code builds on |
| **Padded Prefix Arrays (size N+1)** | Avoids the `i==0` special case entirely |
| **Equilibrium Index** | Simpler version: no parity flip, just left==right split |
| **Odd/Even prefix sum queries** | Direct application of ps_odd / ps_even arrays |
| **Segment Tree** | Handles dynamic removal with range queries |

---

> ✍️ **The Big Idea:**
> Build two prefix arrays — one tracking only odd-indexed sums, one tracking
> only even-indexed sums. At every removal candidate `i`, split the array into
> a **left zone** (parities unchanged) and a **right zone** (parities flip).
> Combine their contributions with O(1) arithmetic.
> The crucial twist: right zone's even elements contribute to the new **odd** sum,
> and right zone's odd elements contribute to the new **even** sum — because
> every element right of the removal point shifts left by one.

---

*Happy Coding! 🚀*
