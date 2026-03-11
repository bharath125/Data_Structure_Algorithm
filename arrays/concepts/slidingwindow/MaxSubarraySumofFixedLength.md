# 🏆 Maximum Subarray Sum of Fixed Length B

> **Difficulty:** Beginner → Intermediate
> **Topic:** Arrays · Fixed-Size Sliding Window · Running Maximum
> **Language:** Python
> **Constraints:** 1 ≤ N ≤ 10⁵ · 1 ≤ A[i] ≤ 10⁶ · 1 ≤ B ≤ N

---

## 📋 Problem Statement

Given an integer array **A** of length **N** and an integer **B**, find the **maximum sum** among all contiguous subarrays of exactly **B** elements.

```
Find: MAX of all window sums
      where every window has exactly B consecutive elements
```

---

## 🌍 Real-World Analogy — Before Any Code

### 🏪 Best Sales Window

A shop records daily sales over 6 days:

```
Day:    1    2    3    4    5    6
Sales: [3,   9,   5,   6,   5,  11]
```

The manager asks:
> *"Which 3-consecutive-day stretch had the highest total sales?"*

A smart employee doesn't add 3 numbers fresh every time. They think:
> *"Yesterday's 3-day total was ₹17. Today I drop Day 1 (₹3) and pick up Day 4 (₹6). New total = 17 - 3 + 6 = ₹20."*

One subtraction, one addition. That's the **Sliding Window** — reuse yesterday's total, adjust at the edges.

---

## 🧩 Understanding the Examples

### Example 1: `A=[6,7,8,2]`, B=2

```
Index:   0    1    2    3
Value: [ 6,   7,   8,   2 ]
```

All windows of exactly B=2 elements:

| Window  | Elements | Sum    |
|:-------:|:--------:|:------:|
| A[0..1] | [6, 7]   | 13     |
| **A[1..2]** | **[7, 8]** | **15** ← MAX |
| A[2..3] | [8, 2]   | 10     |

**Answer = 15** ✅

---

### Example 2: `A=[3,9,5,6,5,11]`, B=3

```
Index:   0    1    2    3    4    5
Value: [ 3,   9,   5,   6,   5,  11 ]
```

All windows of exactly B=3 elements:

| Window  | Elements    | Sum    |
|:-------:|:-----------:|:------:|
| A[0..2] | [3, 9, 5]   | 17     |
| A[1..3] | [9, 5, 6]   | 20     |
| A[2..4] | [5, 6, 5]   | 16     |
| **A[3..5]** | **[6, 5, 11]** | **22** ← MAX |

**Answer = 22** ✅

---

## 💡 The Core Insight — Consecutive Windows Share B-1 Elements

This is the heart of the sliding window technique. Look at two consecutive windows:

```
Window 1:  A[0]  A[1]  A[2]
Window 2:        A[1]  A[2]  A[3]
                 └─────────┘
                 B-1 elements SHARED — already computed!
```

What changed between them?
- `A[0]` **left** the window (fell off the left)
- `A[3]` **entered** the window (joined from the right)

So:
```
window2_sum = window1_sum - A[0] + A[3]
                            ↑ out    ↑ in
```

One subtraction + one addition = **O(1)** per slide instead of re-summing B elements = **O(B)**.

---

## 🔍 The Code — Every Line Explained

### The Single-Element Guard

```python
if n == 1:
    return A[0]
```

> When the array has exactly one element, both B and the answer must be A[0].
> The sliding loop would never run for n=1 (`end=B=1`, `1 < 1` is False),
> but `ans = window_sum = A[0]` would be returned correctly anyway.
> This guard is optional but makes the special case explicit and self-documenting.

---

### Phase 1: Build the First Window

```python
window_sum = 0

for i in range(B-1+1):    # same as range(0, B)
    window_sum += A[i]
```

> Adds up the very first B elements: `A[0] + A[1] + ... + A[B-1]`.
>
> `range(B-1+1)` = `range(B)`. Written as `B-1+1` to make the intent visual:
> *"Loop from index 0 to index B-1 inclusive."*
>
> After this: `window_sum = sum of A[0..B-1]`

---

### Capture the First Window as Initial Best

```python
ans = window_sum
```

> This one line does something critically important:
> it makes the **first window a candidate for the answer**.
>
> `ans` starts as the first window's sum — not 0, not `-infinity`.
> As we slide, `ans` can only grow. If no later window beats it, the first window wins.
>
> 💡 **This is also the fix to a common bug** — in the previous "Subarray with sum C"
> problem, the first window was built but never checked. Here, setting `ans = window_sum`
> immediately after building it ensures it is always included in the comparison.

---

### Phase 2: Slide Across Remaining Windows

```python
start = 1    # start index of the SECOND window
end   = B    # end   index of the SECOND window

while end < n:
    window_sum = window_sum - A[start-1] + A[end]
    ans = max(window_sum, ans)
    start += 1
    end   += 1
```

> **`start = 1, end = B`:** The second window spans indices `[1, B]`.
> The first window was `[0, B-1]`, so we advance both pointers by 1.
>
> **`while end < n`:** Keep sliding while the right edge hasn't gone past the array.
> When `end = n-1` (last valid index), that's the final window.
> When `end = n`, we've gone out of bounds → stop.
>
> **`window_sum - A[start-1] + A[end]`:**
> - `A[start-1]` = element **leaving** from the left
> - `A[end]` = element **entering** from the right
>
> **Why `A[start-1]` not `A[start]`?**
> At this point, `start` already points to the new window's left edge.
> The element that just fell off was at `start-1` — the previous window's left edge.
>
> **`ans = max(window_sum, ans)`:** After each slide, check if the new window
> beats the current best. `ans` never decreases — it only holds the best seen so far.

---

## 📊 Full Dry Run — Example 1: `A=[6,7,8,2]`, B=2

### Phase 1: First Window

```
i=0: window_sum += A[0]=6  → window_sum = 6
i=1: window_sum += A[1]=7  → window_sum = 13

First window A[0..1] = [6, 7]  sum = 13
ans = 13  ← first window is the current best
```

### Phase 2: Slide

```
n=4, start=1, end=2

══════════════════════════════════════════════════
 Iteration 1:  start=1, end=2
  Remove A[start-1] = A[0] = 6   (leaving from left)
  Add    A[end]     = A[2] = 8   (entering from right)
  window_sum = 13 - 6 + 8 = 15
  Window A[1..2] = [7, 8]
  ans = max(15, 13) = 15  ✅ new best!
  start→2, end→3
══════════════════════════════════════════════════
 Iteration 2:  start=2, end=3
  Remove A[start-1] = A[1] = 7   (leaving from left)
  Add    A[end]     = A[3] = 2   (entering from right)
  window_sum = 15 - 7 + 2 = 10
  Window A[2..3] = [8, 2]
  ans = max(10, 15) = 15  (no change)
  start→3, end→4
══════════════════════════════════════════════════
 end=4, n=4 → 4 < 4 is False → stop

Return ans = 15 ✅
```

---

## 📊 Full Dry Run — Example 2: `A=[3,9,5,6,5,11]`, B=3

### Phase 1: First Window

```
i=0: ws += 3  →  3
i=1: ws += 9  → 12
i=2: ws += 5  → 17

First window A[0..2] = [3, 9, 5]  sum = 17
ans = 17
```

### Phase 2: Slide

```
n=6, start=1, end=3

══════════════════════════════════════════════════════════════
 Iteration 1:  start=1, end=3
  Remove A[0]=3,  Add A[3]=6
  window_sum = 17 - 3 + 6 = 20
  Window A[1..3] = [9, 5, 6]
  ans = max(20, 17) = 20  ✅ new best!
══════════════════════════════════════════════════════════════
 Iteration 2:  start=2, end=4
  Remove A[1]=9,  Add A[4]=5
  window_sum = 20 - 9 + 5 = 16
  Window A[2..4] = [5, 6, 5]
  ans = max(16, 20) = 20  (no change)
══════════════════════════════════════════════════════════════
 Iteration 3:  start=3, end=5
  Remove A[2]=5,  Add A[5]=11
  window_sum = 16 - 5 + 11 = 22
  Window A[3..5] = [6, 5, 11]
  ans = max(22, 20) = 22  ✅ new best!
══════════════════════════════════════════════════════════════
 end=6, n=6 → 6 < 6 is False → stop

Return ans = 22 ✅
```

---

## 🎨 Sliding Window — Visual Animation

```
A = [3,  9,  5,  6,  5,  11],  B = 3

         Window size = 3 (always exactly 3 elements)

Step 0 — First window (built directly, sum captured in ans):
  [▓▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓  ·      ·      ·  ]
     3       9      5
  sum = 17    ans = 17

Step 1 — Slide right (start=1, end=3):
  [  ·    ▓▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓  ·      ·  ]
             9      5      6
  remove 3, add 6 → sum = 17-3+6 = 20    ans = 20 ✅

Step 2 — Slide right (start=2, end=4):
  [  ·      ·    ▓▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓  ·  ]
                    5      6      5
  remove 9, add 5 → sum = 20-9+5 = 16    ans = 20

Step 3 — Slide right (start=3, end=5):
  [  ·      ·      ·    ▓▓▓▓▓  ▓▓▓▓▓  ▓▓▓▓▓]
                           6      5     11
  remove 5, add 11 → sum = 16-5+11 = 22   ans = 22 ✅

end=6, n=6 → STOP

MAXIMUM = 22  (window A[3..5] = [6, 5, 11])
```

---

## 🔑 How `ans = window_sum` Solves the Classic Bug

Compare this code with a common mistake from similar problems:

```python
# ❌ BUGGY PATTERN (from "Subarray with sum C" problem):
window_sum = 0
for i in range(B):
    window_sum += A[i]
# first window built but ans never set to it!
ans = float('-inf')   # or ans = 0  ← first window missed!
start = 1; end = B
while end < n:
    window_sum = window_sum - A[start-1] + A[end]
    ans = max(window_sum, ans)   # only checks windows 2, 3, ...
    ...

# ❌ Fails when the first window has the maximum sum!
# e.g. A=[9,1,1,1], B=2 → first window [9,1]=10 is max, returns 2 instead
```

```python
# ✅ THIS CODE'S CORRECT PATTERN:
window_sum = 0
for i in range(B):
    window_sum += A[i]
ans = window_sum     # ← first window captured immediately!
start = 1; end = B
while end < n:
    window_sum = window_sum - A[start-1] + A[end]
    ans = max(window_sum, ans)   # checks ALL windows including first
    ...

# ✅ Correct even when first window is the answer.
```

> The single line `ans = window_sum` placed **between Phase 1 and Phase 2**
> is what makes this code correct. It costs nothing — one assignment —
> but guarantees the first window is always a valid candidate.

---

## 🔢 How Many Windows Are There?

```
Total windows = N - B + 1

N=4, B=2: 4-2+1 = 3 windows  [6,7], [7,8], [8,2]
N=6, B=3: 6-3+1 = 4 windows  [3,9,5], [9,5,6], [5,6,5], [6,5,11]
N=5, B=5: 5-5+1 = 1 window   (entire array — only one window)
N=5, B=1: 5-1+1 = 5 windows  (every single element is a window)
```

The code processes:
- **1 window** in Phase 1 (the first one, directly summed)
- **N-B windows** in Phase 2 (while loop runs N-B times)
- **Total: N-B+1** windows — every possible window, nothing skipped ✅

---

## ⏱️ Complexity Analysis

| Phase              | Operation                  | Time      |
|:-------------------|:---------------------------|:---------:|
| Build first window | B additions                | O(B)      |
| Slide N-B windows  | 1 subtract + 1 add each    | O(N-B)    |
| **Total Time**     | O(B + N-B) = O(N)          | **O(N)**  |
| **Space**          | 3 variables: ws, ans, i    | **O(1)**  |

### Why O(N) crushes O(N·B):

```
N = 10^5, B = 5×10^4 (half the array)

O(N·B) brute:  10^5 × 5×10^4 = 5×10^9 ops  ❌  ~50 seconds
O(N) sliding:  10^5            = 10^5 ops   ✅  instant
```

---

## ⚠️ Pitfalls & Edge Cases

### ❗ Pitfall 1: `ans` Initialised Too Late

```python
# ❌ WRONG — first window missed
window_sum = sum(A[:B])
start, end = 1, B
ans = float('-inf')     # ← should be ans = window_sum!
while end < n:
    ...

# Fails: A=[9,1,1,1], B=2 → [9,1]=10 is max, but code returns 2
```

```python
# ✅ CORRECT — capture first window before entering loop
window_sum = sum(A[:B])
ans = window_sum        # ← first window is a valid candidate
start, end = 1, B
while end < n:
    ...
```

---

### ❗ Pitfall 2: `A[start]` vs `A[start-1]`

```python
window_sum = window_sum - A[start-1] + A[end]   # ✅ removes old left edge
window_sum = window_sum - A[start]   + A[end]   # ❌ removes current left (off by 1)
```

When `start=1, end=2`: the element leaving is `A[0]` = `A[start-1]`, not `A[1]` = `A[start]`.

```
Before slide:  [A[0], A[1], A[2],  A[3]  ...]
                └──── old window ────┘
                       └──── new window ────┘

Element leaving = A[0] = A[start-1]   ← previous left edge
Element joining = A[3] = A[end]       ← new right edge
```

---

### ❗ Pitfall 3: While Condition Off-By-One

```python
while end < n:    # ✅ CORRECT — A[end] exists when end = n-1
while end <= n:   # ❌ WRONG  — A[n] is IndexError!
```

---

### ❗ Edge Case: K = N (Single Window)

```python
A = [1, 2, 3],  B = 3
→ Only one window: A[0..2] = [1,2,3], sum = 6
→ Phase 1 builds it, ans = 6
→ Phase 2: end=3, n=3 → 3 < 3 is False → loop never runs
→ Return 6  ✅
```

This works because `ans = window_sum` captures the only window before the loop starts.

---

### ❗ Edge Case: K = 1 (Every Element Is a Window)

```python
A = [3, 1, 4, 1, 5],  B = 1
→ Windows: [3],[1],[4],[1],[5] — sums = 3,1,4,1,5
→ Answer = 5
→ Phase 1: window_sum = A[0] = 3, ans = 3
→ Phase 2 slides through A[1],A[2],A[3],A[4] updating ans
→ Returns 5  ✅
```

---

## 🗺️ Complete Visual Summary

```
PROBLEM: Find maximum sum window of size B=2 in A=[6,7,8,2]

STEP 1 — Build first window:
  ┌───┬───┐
  │ 6 │ 7 │  sum = 13    ans = 13
  └───┴───┘

STEP 2 — Slide: remove A[0]=6, add A[2]=8
      ┌───┬───┐
      │ 7 │ 8 │  sum = 13-6+8 = 15    ans = max(15,13) = 15  ✅
      └───┴───┘

STEP 3 — Slide: remove A[1]=7, add A[3]=2
            ┌───┬───┐
            │ 8 │ 2 │  sum = 15-7+2 = 10    ans = max(10,15) = 15
            └───┴───┘

end=4 = n → STOP

ANSWER: 15  (window [7,8] at A[1..2])

─────────────────────────────────────────────────────────
FORMULA RECAP:
  Phase 1: window_sum = A[0]+A[1]+...+A[B-1]   (direct sum)
           ans = window_sum                      (first window captured!)
  Phase 2: window_sum = window_sum - A[start-1] + A[end]
           ans = max(window_sum, ans)            (track best)
           start++, end++

KEY:   ans = window_sum  between phases = the essential correctness guarantee
─────────────────────────────────────────────────────────
```

---

## 🆚 This Problem vs "Subarray with Sum C"

| Aspect             | Sum == C (previous)        | Maximum Sum (this problem)     |
|:-------------------|:---------------------------|:-------------------------------|
| Goal               | Does target exist? (1/0)   | What's the largest sum?        |
| `ans` initialised  | nothing (check with `==`)  | `ans = window_sum` (first window) |
| First window check | ❌ Bug — often missed       | ✅ `ans = window_sum` fixes it  |
| Loop action        | `return 1` if match        | `ans = max(window_sum, ans)`   |
| Return             | `return 0` (not found)     | `return ans`                   |

---

## 🧪 Test It Yourself

```python
def solve(A, B):
    n = len(A)

    # Build first window
    window_sum = 0
    for i in range(B):
        window_sum += A[i]

    ans = window_sum   # ← first window is always a candidate

    # Slide remaining windows
    start, end = 1, B
    while end < n:
        window_sum = window_sum - A[start-1] + A[end]
        ans = max(window_sum, ans)
        start += 1
        end   += 1

    return ans


tests = [
    ([6,7,8,2],        2, 15),   # [7,8]=15
    ([3,9,5,6,5,11],   3, 22),   # [6,5,11]=22
    ([1,2,3],          3,  6),   # K==N, only 1 window
    ([3,1,4,1,5],      1,  5),   # K==1, max element
    ([4,4,4,4],        2,  8),   # all equal
    ([9,1,1,1,1],      2, 10),   # first window is max — common bug case!
    ([1,1,1,1,9],      2, 10),   # last window is max
    ([1,2,3,4,5],      3, 12),   # [3,4,5]=12
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
| **Variable-size Sliding Window** | Window grows/shrinks dynamically based on a condition |
| **Subarray with Sum == C** | Same window, but search for exact match instead of max |
| **Minimum Subarray Sum of size K** | Replace `max` with `min` — identical structure |
| **Longest Subarray with Sum ≤ K** | Window resizes; two-pointer approach |
| **Kadane's Algorithm** | Maximum subarray of **any** length — O(N) with DP |
| **Maximum Sum Rectangle** | 2D version using prefix sums + Kadane's |

---

> ✍️ **The Big Idea:**
> A fixed-size sliding window processes all N-B+1 windows of length B in O(N) total.
> The magic formula `new_sum = old_sum - outgoing + incoming` reuses the previous
> window's work — only two elements change per slide, so each slide is O(1).
> The only "gotcha" is capturing the **first window** before the loop starts.
> Setting `ans = window_sum` right after Phase 1 costs nothing and guarantees
> the first window is always considered — this one line is what separates
> a correct implementation from a subtly broken one.

---

*Happy Coding! 🚀*
