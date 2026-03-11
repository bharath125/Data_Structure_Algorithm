# 🪟 Subarray with Given Sum and Length — Sliding Window

> **Difficulty:** Beginner → Intermediate
> **Topic:** Arrays · Fixed-Size Sliding Window
> **Language:** Python
> **Constraints:** 1 ≤ N ≤ 10⁵ · 1 ≤ A[i] ≤ 10⁴ · 1 ≤ B ≤ N · 1 ≤ C ≤ 10⁹

---

## 📋 Problem Statement

Given:
- **A** — integer array of length N
- **B** — required subarray length (window size)
- **C** — required subarray sum (target)

Return **1** if any contiguous subarray of length exactly **B** has sum exactly **C**, else return **0**.

```
Does there exist i such that:
  A[i] + A[i+1] + ... + A[i+B-1] == C  ?
```

---

## 🌍 Real-World Analogy — Before Any Code

### 🏃 Running Race Lap Times

A runner records lap times for each lap of a race:

```
Lap:   1    2    3    4    5
Time: [4,   3,   2,   6,   1]  seconds
```

A coach asks:
> *"Was there any 3-consecutive-lap stretch where the runner's total time was exactly 11 seconds?"*

The coach could re-add 3 laps from scratch at every starting position. That's the brute force.

Or the coach can be smarter: **look at 3 laps at a time, and when moving to the next stretch, just drop the first lap and pick up the next one.** That's the **Sliding Window** — reuse the previous calculation instead of starting over.

---

## 🧩 Understanding the Examples

### Example 1: `A=[4,3,2,6,1]`, B=3, C=11

```
Index:  0    1    2    3    4
Value: [4,   3,   2,   6,   1]
```

All windows of length B=3:

| Window     | Elements  | Sum | == 11? |
|:----------:|:---------:|:---:|:------:|
| A[0..2]    | [4, 3, 2] | 9   | ❌     |
| **A[1..3]**| **[3,2,6]**|**11**|**✅** |
| A[2..4]    | [2, 6, 1] | 9   | ❌     |

Found at index 1 → **Return 1** ✅

---

### Example 2: `A=[4,2,2,5,1]`, B=4, C=6

```
Index:  0    1    2    3    4
Value: [4,   2,   2,   5,   1]
```

All windows of length B=4:

| Window  | Elements     | Sum | == 6? |
|:-------:|:------------:|:---:|:-----:|
| A[0..3] | [4, 2, 2, 5] | 13  | ❌    |
| A[1..4] | [2, 2, 5, 1] | 10  | ❌    |

No window matches → **Return 0** ✅

---

## 💡 The Core Idea — The Sliding Window

### Why Not Recompute From Scratch?

For each of the `N-B+1` windows, recomputing the sum from scratch takes B additions.
Total: **(N-B+1) × B ≈ O(N·B)** — slow when B is large.

### The Insight: Consecutive Windows Share B-1 Elements

```
Window 1: A[0], A[1], A[2]      (first window)
Window 2:       A[1], A[2], A[3] (second window)

Overlap: A[1] and A[2] appear in BOTH windows!

So: window2_sum = window1_sum - A[0] + A[3]
                               ↑ leaves   ↑ joins
```

One subtraction + one addition per slide = **O(1)** per window = **O(N) total**.

---

## 🔍 The Code — Every Line Explained

### The Special Case Guard

```python
if n == 1 and A[0] == C:
    return 1
```

> This handles the edge case where the array has only one element and B=1.
> **However, this is NOT sufficient** — see the Bug section below.

---

### Phase 1: Build the First Window

```python
for i in range(0, B-1+1):    # same as range(0, B)
    window_sum += A[i]
```

> Sums up the first B elements: A[0], A[1], …, A[B-1].
>
> `B-1+1` is written to make it visually clear:
> *"Loop from index 0 to index B-1 inclusive."* (`range(0, B-1+1)` = `range(0, B)`)
>
> After this loop: `window_sum = A[0] + A[1] + ... + A[B-1]`

---

### Phase 2: Slide the Window

```python
start = 1     # start of the SECOND window
end   = B     # end   of the SECOND window

while end < n:
    window_sum = window_sum - A[start-1] + A[end]
    if window_sum == C:
        return 1
    start += 1
    end   += 1

return 0
```

> `start` and `end` together define the **current window** being checked.
> They always satisfy: `end - start + 1 == B` (window always has exactly B elements).
>
> The formula `window_sum - A[start-1] + A[end]`:
> - `A[start-1]` = the element **leaving** (it was in the previous window's left edge)
> - `A[end]` = the element **entering** (it's the new right edge)
>
> When `end == n`: the window would go out of bounds → stop.

---

## 📊 Why `start-1` and Not `start`?

This is the trickiest part of the code. Let's understand it with the second window as an example:

```
First window:   A[0], A[1], A[2]    (start=0, end=2)
                └─ this was the left edge of the PREVIOUS window

After slide:
  start=1, end=3
  The element that LEFT is A[start-1] = A[0]  ← the old start!
  The element that JOINED is A[end]   = A[3]  ← the new end!
```

```
  Before slide:  [A[0], A[1], A[2],  A[3],  A[4]]
                  ←── old window ──→
                        ←── new window ──→

  Removed: A[0]  (= A[start-1] when start=1)
  Added:   A[3]  (= A[end] when end=3)
```

> **The formula works because `start` has already advanced to the new window's left edge.**
> So `start-1` refers to the previous window's left edge — the one that just slid out.

---

## 📊 Full Dry Run — Example 1: `A=[4,3,2,6,1]`, B=3, C=11

### Phase 1: First Window

```
i=0: window_sum += A[0]=4  → window_sum = 4
i=1: window_sum += A[1]=3  → window_sum = 7
i=2: window_sum += A[2]=2  → window_sum = 9

First window A[0..2] = [4, 3, 2]  sum = 9
```

> ⚠️ **Notice: 9 ≠ 11** — first window doesn't match. But this is NOT checked by the code!
> (See the Bug section below.)

### Phase 2: Slide

```
n=5, B=3, start=1, end=3

─────────────────────────────────────────────────────────────
Iteration 1:  start=1, end=3
  Remove A[start-1] = A[0] = 4
  Add    A[end]     = A[3] = 6
  window_sum = 9 - 4 + 6 = 11
  Window A[1..3] = [3, 2, 6]
  11 == 11? ✅ return 1  ← FOUND!
─────────────────────────────────────────────────────────────

Answer: 1 ✅
(Would have continued if not found:)

Iteration 2 (for reference):  start=2, end=4
  Remove A[1]=3, Add A[4]=1
  window_sum = 11 - 3 + 1 = 9
  Window A[2..4] = [2, 6, 1]
  9 == 11? ❌
  start=3, end=5 → 5 < 5 is False → stop
```

---

## 📊 Full Dry Run — Example 2: `A=[4,2,2,5,1]`, B=4, C=6

### Phase 1: First Window

```
i=0: window_sum += 4  → 4
i=1: window_sum += 2  → 6
i=2: window_sum += 2  → 8
i=3: window_sum += 5  → 13

First window A[0..3] = [4, 2, 2, 5]  sum = 13
(not checked, 13 ≠ 6 anyway)
```

### Phase 2: Slide

```
n=5, B=4, start=1, end=4

Iteration 1:  start=1, end=4
  Remove A[0]=4, Add A[4]=1
  window_sum = 13 - 4 + 1 = 10
  Window A[1..4] = [2, 2, 5, 1]
  10 == 6? ❌
  start=2, end=5 → 5 < 5 is False → stop

return 0 ✅
```

---

## 🗺️ Visual Animation of the Sliding Window

```
A = [4,  3,  2,  6,  1],  B=3,  C=11

         Window size = 3 (always exactly 3 elements)

Step 0 (first window, BUILT not checked):
  [▓  ▓  ▓  ·  ·]    A[0..2] = [4,3,2]   sum=9
   4  3  2  6  1

Step 1 (start=1, end=3):
  [·  ▓  ▓  ▓  ·]    A[1..3] = [3,2,6]   sum=9-4+6=11 ✅ RETURN 1
       3  2  6
      ↑              ↑
   removed=4      added=6

(If not found, would continue:)
Step 2 (start=2, end=4):
  [·  ·  ▓  ▓  ▓]    A[2..4] = [2,6,1]   sum=11-3+1=9
          2  6  1
         ↑                 ↑
      removed=3          added=1
```

---

## 🔢 How Many Windows Exist?

For an array of length N and window size B:

```
Total windows = N - B + 1

N=5, B=3: 5-3+1 = 3 windows  ✅
N=5, B=4: 5-4+1 = 2 windows  ✅
N=5, B=5: 5-5+1 = 1 window   ✅ (only the entire array)
N=5, B=1: 5-1+1 = 5 windows  ✅ (every single element)
```

The code processes:
- 1 window in Phase 1 (the first window)
- N-B remaining windows in Phase 2 (via the while loop)
- Total: exactly **N-B+1** windows ✅

---

## 🐛 BUG IN THE CODE — First Window Never Checked!

This is the most important thing to understand about this solution.

### What the code does:

```python
# Phase 1: builds first window sum
for i in range(0, B):
    window_sum += A[i]

# Phase 2: checks windows starting from the SECOND one
start = 1
end   = B
while end < n:         # ← when B==N, end=N, N<N is False → loop NEVER runs!
    window_sum = window_sum - A[start-1] + A[end]
    if window_sum == C:
        return 1
    ...
return 0               # ← first window was never checked → WRONG!
```

### Failing test cases:

```python
A = [5, 5, 5],  B = 3,  C = 15
# Only one window: [5,5,5] = 15 == C → should return 1
# Code: end=3, n=3, 3<3 is False → loop never runs → returns 0  ❌ BUG!

A = [1, 2, 3, 4, 5],  B = 5,  C = 15
# Only one window: [1,2,3,4,5] = 15 == C → should return 1
# Code: end=5, n=5, 5<5 is False → loop never runs → returns 0  ❌ BUG!

A = [10, 1, 2, 3],  B = 1,  C = 10
# First window: [10] = 10 == C → should return 1
# n==1 guard doesn't fire (n=4 not 1) → loop checks A[1],A[2],A[3] → returns 0  ❌ BUG!
```

### The Fix — Check First Window Before Sliding

```python
def solve_fixed(A, B, C):
    n = len(A)

    # Build AND check the first window
    window_sum = 0
    for i in range(B):
        window_sum += A[i]

    if window_sum == C:        # ← ADD THIS CHECK
        return 1

    # Slide for remaining windows
    start = 1
    end   = B
    while end < n:
        window_sum = window_sum - A[start-1] + A[end]
        if window_sum == C:
            return 1
        start += 1
        end   += 1

    return 0
```

One line added. Handles all cases correctly.

---

## ⏱️ Complexity Analysis

| Phase                | Operation                  | Time      |
|:---------------------|:---------------------------|:---------:|
| Build first window   | B additions                | O(B)      |
| Slide (N-B windows)  | 1 subtract + 1 add each    | O(N-B)    |
| **Total Time**       |                            | **O(N)**  |
| **Space**            | Just one variable          | **O(1)**  |

### Why O(N) beats O(N·B):

```
N = 10^5, B = 10^4

O(N·B) brute: 10^5 × 10^4 = 10^9 ops  ⚠️  ~10 seconds
O(N) sliding: 10^5         = 10^5 ops  🚀  instant
```

---

## 🗺️ Complete Visual Summary

```
PROBLEM: Does any window of size B=3 have sum C=11?
ARRAY:   A = [4, 3, 2, 6, 1]

PHASE 1 — Build first window (size B=3):
  ┌───┬───┬───┐
  │ 4 │ 3 │ 2 │  sum = 9          ← built, but NOT checked (bug!)
  └───┴───┴───┘

PHASE 2 — Slide one step at a time:
  Formula: new_sum = old_sum - A[start-1] + A[end]

  Slide 1:  remove A[0]=4, add A[3]=6
  ┌───┬───┬───┐
  │ 3 │ 2 │ 6 │  sum = 9-4+6 = 11  == C? ✅ RETURN 1
  └───┴───┴───┘

ANSWER: 1 ✅

─────────────────────────────────────
KEY FORMULA:
  new_sum = old_sum - A[start-1] + A[end]
                       ↑ leaves       ↑ joins
  start-1 = previous window's left edge (already slid past)
  end     = new element entering from the right
─────────────────────────────────────

WINDOW COUNT: N - B + 1 = 5 - 3 + 1 = 3 total windows
  Phase 1 builds window #1
  While loop checks windows #2, #3 (end < n)
```

---

## ⚠️ All Pitfalls at a Glance

### ❗ Pitfall 1: First Window Not Checked (Main Bug)

```python
# ❌ Code as written — first window built but never compared to C
for i in range(0, B):
    window_sum += A[i]
# Missing: if window_sum == C: return 1
```

### ❗ Pitfall 2: `n==1` Guard is Not Enough

```python
if n == 1 and A[0] == C:
    return 1
```

This only handles the single-element array case. It does NOT fix the first-window bug for n > 1.
For `A=[10,1,2,3], B=1, C=10` — n=4 so the guard doesn't fire.

### ❗ Pitfall 3: `range(0, B-1+1)` vs `range(0, B)`

```python
range(0, B-1+1)   # same as range(0, B) — both correct
                  # B-1+1 written for readability: "0 to B-1 inclusive"
```

### ❗ Pitfall 4: Off-by-One in While Condition

```python
while end < n:    # ✅ CORRECT — stops when end would go out of bounds
while end <= n:   # ❌ WRONG  — A[end] when end=n is IndexError!
```

### ❗ Pitfall 5: Using `A[start]` Instead of `A[start-1]`

```python
window_sum = window_sum - A[start-1] + A[end]   # ✅ removes old left edge
window_sum = window_sum - A[start]   + A[end]   # ❌ removes current left edge (wrong element!)
```

When `start=1, end=3`: the element leaving is `A[0]` = `A[start-1]`, not `A[1]` = `A[start]`.

---

## 🧪 Test It Yourself (Fixed Version)

```python
def solve(A, B, C):
    n = len(A)

    # Build first window
    window_sum = 0
    for i in range(B):
        window_sum += A[i]

    if window_sum == C:      # ← critical fix
        return 1

    # Slide remaining windows
    start, end = 1, B
    while end < n:
        window_sum = window_sum - A[start-1] + A[end]
        if window_sum == C:
            return 1
        start += 1
        end   += 1

    return 0


tests = [
    ([4,3,2,6,1],   3, 11,  1),   # [3,2,6]=11 ✅
    ([4,2,2,5,1],   4,  6,  0),   # no match ✅
    ([5,5,5],       3, 15,  1),   # only 1 window, buggy code fails
    ([1,2,3,4,5],   5, 15,  1),   # K==N, buggy code fails
    ([10,1,2,3],    1, 10,  1),   # K=1, first element is answer
    ([1,2,3,4],     2,  3,  1),   # [1,2]=3
    ([1,2,3,4],     2, 10,  0),   # no window sums to 10
    ([7,7,7,7],     2, 14,  1),   # all windows sum to 14
    ([1,2,3],       2,  6,  0),   # [1,2]=3, [2,3]=5, none=6
]

for A, B, C, expected in tests:
    result = solve(A, B, C)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  A={A}  B={B}  C={C}  → {result}")
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Variable-size Sliding Window** | Window grows/shrinks based on a condition |
| **Maximum Subarray Sum of size K** | Same pattern, tracking max instead of exact match |
| **Longest Subarray with sum ≤ K** | Window that expands and shrinks dynamically |
| **Subarray Sum Equals K** (LeetCode 560) | No fixed length — use prefix sum + hashmap |
| **Two Pointer Technique** | Related approach for sorted arrays |
| **String Sliding Window** | Anagram, permutation problems using same window idea |

---

> ✍️ **The Big Idea:**
> A fixed-size sliding window scans all subarrays of length B in O(N) by reusing
> the previous window's sum. Only **one element leaves** (left edge) and **one element enters**
> (right edge) per slide — so `new_sum = old_sum - outgoing + incoming`.
> The first window must be built separately and **checked separately** — skipping
> this check is the most common bug in sliding window implementations.

---

*Happy Coding! 🚀*
