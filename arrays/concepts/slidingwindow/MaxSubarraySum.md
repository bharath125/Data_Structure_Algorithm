# 🔥 Maximum Subarray Sum of Size K
### Three Approaches: O(N·K) → O(N) with Space → O(N) with O(1) Space

> **Difficulty:** Beginner → Advanced
> **Topic:** Arrays · Prefix Sum · Sliding Window
> **Language:** Python
> **Array:** `A = [-3, 4, -2, 5, 3, -2, 8, 2, -1, 4]` · **K = 5**

---

## 📋 Problem Statement

Given an integer array **A** of length **N** and an integer **K**, find the **maximum sum** among all contiguous subarrays of length exactly **K**.

```
Every window of exactly K elements:
  A[0..K-1], A[1..K], A[2..K+1], ..., A[N-K..N-1]

Find: MAX of all their sums
```

---

## 🌍 Real-World Analogy — Before Any Code

### 🌡️ Best 5-Day Average Temperature

A weather station records daily temperatures for 10 days:

```
Day:    0    1    2    3    4    5    6    7    8    9
Temp: [-3,   4,  -2,   5,   3,  -2,   8,   2,  -1,   4]
```

A scientist asks: *"Which consecutive 5-day window had the highest total temperature?"*

Three strategies to answer this:
1. **Brute Force** — Add up 5 temperatures fresh for every window
2. **Prefix Sum** — Pre-compute running totals, answer each window instantly
3. **Sliding Window** — Maintain a running sum, just swap one element at a time

All produce the same answer. The difference is **how efficiently** they get there.

---

## 🔢 All Windows for `A = [-3, 4, -2, 5, 3, -2, 8, 2, -1, 4]`, K=5

```
Window [0..4] = [-3,  4, -2,  5,  3]  → sum =  7
Window [1..5] = [ 4, -2,  5,  3, -2]  → sum =  8
Window [2..6] = [-2,  5,  3, -2,  8]  → sum = 12
Window [3..7] = [ 5,  3, -2,  8,  2]  → sum = 16  ← MAXIMUM
Window [4..8] = [ 3, -2,  8,  2, -1]  → sum = 10
Window [5..9] = [-2,  8,  2, -1,  4]  → sum = 11

Answer = 16
```

Total windows = N − K + 1 = 10 − 5 + 1 = **6 windows**

---

---

# 🐢 Approach 1 — Brute Force: O(N·K) Time, O(1) Space

---

## 🔍 The Code

```python
A = [-3, 4, -2, 5, 3, -2, 8, 2, -1, 4]
K = 5
n = len(A)
ans = float('-inf')

s = 0        # start index of current window
e = K - 1    # end index of current window (starts at index 4)

while e < n:                     # loop over all valid windows
    subarraysum = 0
    for i in range(s, e + 1):    # scan K elements inside window
        subarraysum += A[i]
    ans = max(subarraysum, ans)
    s += 1                       # slide start right
    e += 1                       # slide end right

print(ans)   # 16
```

## 🔍 Every Line Explained

```python
s = 0        # First window starts at index 0
e = K - 1    # First window ends at index K-1 (= 4 for K=5)
```
> The first window always spans indices `[0, K-1]`.

```python
while e < n:
```
> Keep looping while the window's **right edge** hasn't gone past the array.
> When `e = N-1` (last valid position), that's the last window.
> When `e = N`, we've gone past → stop.

```python
    for i in range(s, e + 1):
        subarraysum += A[i]
```
> Inner loop: add up all **K elements** inside the current window `[s..e]`.
> This is why the total complexity is O((N-K+1) × K) ≈ O(N·K).

```python
    ans = max(subarraysum, ans)
    s += 1
    e += 1
```
> Update best answer if current window is better.
> Both `s` and `e` advance by 1 together — the window slides right.

## 📊 Full Dry Run

```
n=10, K=5, s=0, e=4, ans=-inf

Pass 1: s=0, e=4 → A[0..4]=[-3,4,-2,5,3]   sum= 7   ans=max(7,-inf)= 7
Pass 2: s=1, e=5 → A[1..5]=[4,-2,5,3,-2]   sum= 8   ans=max(8, 7)=  8
Pass 3: s=2, e=6 → A[2..6]=[-2,5,3,-2,8]   sum=12   ans=max(12,8)= 12
Pass 4: s=3, e=7 → A[3..7]=[5,3,-2,8,2]    sum=16   ans=max(16,12)=16
Pass 5: s=4, e=8 → A[4..8]=[3,-2,8,2,-1]   sum=10   ans=max(10,16)=16
Pass 6: s=5, e=9 → A[5..9]=[-2,8,2,-1,4]   sum=11   ans=max(11,16)=16

e becomes 10 → 10 < 10 is False → loop ends
Result: 16 ✅
```

## ⏱️ Complexity

```
Outer while loop: (N - K + 1) iterations = 6 iterations for N=10, K=5
Inner for loop:   K iterations per window = 5 per window
Total:            (N-K+1) × K ≈ N × K

For N=10^5, K=10^4:  10^5 × 10^4 = 10^9 operations  ⚠️  Slow
```

---

---

# 🚶 Approach 2 — Prefix Sum: O(N) Time, O(N) Space

---

## 💡 Key Insight: Pre-build running totals

The inner loop recomputes the window sum from scratch every time.
Build a **prefix sum array** once in O(N), then answer each window in **O(1)** — one subtraction.

## 🔍 The Code

```python
# Phase 1: Build prefix sum array  →  O(N)
pf_sum = []
total = 0
for i in range(n):
    total += A[i]
    pf_sum.append(total)

# Phase 2: Answer each window in O(1)
ans = float('-inf')
s, e = 0, K - 1

while e < n:
    if s == 0:
        subarraysum = pf_sum[e]
    else:
        subarraysum = pf_sum[e] - pf_sum[s - 1]
    ans = max(subarraysum, ans)
    s += 1
    e += 1

print(ans)   # 16
```

## 📊 Phase 1 — Build Prefix Array

For `A = [-3, 4, -2, 5, 3, -2, 8, 2, -1, 4]`:

| `i` | `A[i]` | Calculation         | `pf_sum[i]` |
|:---:|:------:|:--------------------|:-----------:|
| 0   | -3     | 0 + (-3) = -3       | **-3**      |
| 1   | 4      | -3 + 4 = 1          | **1**       |
| 2   | -2     | 1 + (-2) = -1       | **-1**      |
| 3   | 5      | -1 + 5 = 4          | **4**       |
| 4   | 3      | 4 + 3 = 7           | **7**       |
| 5   | -2     | 7 + (-2) = 5        | **5**       |
| 6   | 8      | 5 + 8 = 13          | **13**      |
| 7   | 2      | 13 + 2 = 15         | **15**      |
| 8   | -1     | 15 + (-1) = 14      | **14**      |
| 9   | 4      | 14 + 4 = 18         | **18**      |

```
pf_sum = [-3, 1, -1, 4, 7, 5, 13, 15, 14, 18]
          ↑   ↑   ↑  ↑  ↑   ↑   ↑   ↑   ↑   ↑
         i=0 i=1 i=2 3  4   5   6   7   8   9
```

`pf_sum[i]` = sum of A[0] + A[1] + … + A[i] (inclusive, same size as A, not padded)

## 📊 Phase 2 — Window Queries

| Window `[s, e]` | Formula                            | Sum | `ans` |
|:---------------:|:-----------------------------------|:---:|:-----:|
| [0, 4]          | `pf[4]` = 7                        | 7   | 7     |
| [1, 5]          | `pf[5] - pf[0]` = 5 - (-3) = **8**| 8   | 8     |
| [2, 6]          | `pf[6] - pf[1]` = 13 - 1 = **12** | 12  | 12    |
| [3, 7]          | `pf[7] - pf[2]` = 15-(-1)= **16** | 16  | 16    |
| [4, 8]          | `pf[8] - pf[3]` = 14 - 4 = **10** | 10  | 16    |
| [5, 9]          | `pf[9] - pf[4]` = 18 - 7 = **11** | 11  | 16    |

**Result: 16** ✅

### Why `s == 0` Is Special

When `s = 0`, the formula would be `pf_sum[e] - pf_sum[-1]`.
Python's `pf_sum[-1]` silently returns the **last element** (18) — wrong!

```python
# ❌ WRONG (silent Python bug)
subarraysum = pf_sum[e] - pf_sum[s-1]  # pf_sum[-1] = 18 when s=0 ← BUG!

# ✅ CORRECT
if s == 0:
    subarraysum = pf_sum[e]             # no subtraction needed
else:
    subarraysum = pf_sum[e] - pf_sum[s-1]
```

## ⏱️ Complexity

```
Build prefix: O(N)
While loop:   O(N-K+1) iterations × O(1) per iteration = O(N)
Total:        O(N + N) = O(N)  ✅

Space: O(N) for the prefix array
```

---

---

# 🚀 Approach 3 — Sliding Window: O(N) Time, O(1) Space
### *The Optimal Solution*

---

## 💡 The Core Idea

Look at two consecutive windows:

```
Window 1: A[s .. s+K-1]
Window 2: A[s+1 .. s+K]

           ┌──────────────────────────┐
           │  A[s], A[s+1], ..., A[e] │   ← old window
           └──────────────────────────┘
                  ┌──────────────────────────────┐
                  │  A[s+1], ..., A[e], A[e+1]  │   ← new window
                  └──────────────────────────────┘
```

What changed?
- **Removed:** `A[s]` (the element that just left the left edge)
- **Added:** `A[e+1]` (the element that just entered the right edge)
- **Everything in between stays exactly the same!**

So instead of re-summing K elements from scratch:

```
new_sum = old_sum - A[s] + A[e+1]
```

This is the **Sliding Window** formula — one subtraction, one addition = O(1) per window.

---

## 🔍 The Code — Phase by Phase

### Phase 1: Initialise the First Window

```python
subarraysum = 0

for i in range(0, K - 1 + 1):    # range(0, K) → indices 0, 1, 2, 3, 4
    subarraysum += A[i]
```

> The first window `A[0..K-1]` has no "previous window" to derive from.
> We must compute it by direct summation — the only time we do K additions.
> After this, `subarraysum = A[0]+A[1]+A[2]+A[3]+A[4] = -3+4-2+5+3 = 7`

> 🔑 Notice: `range(0, K-1+1)` = `range(0, K)`. The `K-1+1` makes the intent clear:
> "loop from index 0 to the end index K-1, inclusive."

---

### Phase 2: Slide the Window

```python
s = 1   # start index of the SECOND window (not first — already handled)
e = K   # end index of the SECOND window (= index 5 for K=5)

while e < n:
    subarraysum = subarraysum - A[s-1] + A[e]
    ans = max(subarraysum, ans)
    s += 1
    e += 1
```

> At the start of each iteration:
> - `A[s-1]` = the element **leaving** (just fell off the left)
> - `A[e]`   = the element **entering** (just appeared on the right)
>
> **Why `A[s-1]`?** Because the window ending at the previous step included `A[s-1]`.
> Now `s` has moved right — `A[s-1]` is no longer in the window.

> 🔑 **Why no `ans = max(first_window, ans)` before the loop?**
> The code initialises `ans = float('-inf')` but then the loop starts from the
> **second** window only. The **first window's sum is never compared to ans!**
>
> **This is a bug in the given code.** The correct version should set `ans = subarraysum`
> after computing the first window, or compare inside the first-window loop.

---

## 📊 Full Dry Run — Sliding Window

```
A = [-3, 4, -2, 5, 3, -2, 8, 2, -1, 4]
K = 5, n = 10

PHASE 1 — First window A[0..4]:
  i=0: subarraysum = 0 + (-3) = -3
  i=1: subarraysum = -3 + 4   =  1
  i=2: subarraysum = 1 + (-2) = -1
  i=3: subarraysum = -1 + 5   =  4
  i=4: subarraysum = 4 + 3    =  7
  First window sum = 7   ← A[0..4] = [-3,4,-2,5,3]

PHASE 2 — Slide (s starts at 1, e starts at 5):

  s=1, e=5:
    remove A[s-1]=A[0]=-3
    add    A[e]  =A[5]=-2
    sum = 7 - (-3) + (-2) = 7 + 3 - 2 = 8
    window A[1..5] = [4,-2,5,3,-2]  ✅ 4-2+5+3-2=8
    ans = max(8, -inf) = 8

  s=2, e=6:
    remove A[s-1]=A[1]=4
    add    A[e]  =A[6]=8
    sum = 8 - 4 + 8 = 12
    window A[2..6] = [-2,5,3,-2,8]  ✅ -2+5+3-2+8=12
    ans = max(12, 8) = 12

  s=3, e=7:
    remove A[s-1]=A[2]=-2
    add    A[e]  =A[7]=2
    sum = 12 - (-2) + 2 = 12 + 2 + 2 = 16
    window A[3..7] = [5,3,-2,8,2]   ✅ 5+3-2+8+2=16
    ans = max(16, 12) = 16

  s=4, e=8:
    remove A[s-1]=A[3]=5
    add    A[e]  =A[8]=-1
    sum = 16 - 5 + (-1) = 10
    window A[4..8] = [3,-2,8,2,-1]  ✅ 3-2+8+2-1=10
    ans = max(10, 16) = 16

  s=5, e=9:
    remove A[s-1]=A[4]=3
    add    A[e]  =A[9]=4
    sum = 10 - 3 + 4 = 11
    window A[5..9] = [-2,8,2,-1,4]  ✅ -2+8+2-1+4=11
    ans = max(11, 16) = 16

  s=6, e=10 → 10 < 10 is False → STOP

Result: 16 ✅
```

---

## 🎨 Sliding Window — Visual Animation

```
A = [-3,  4, -2,  5,  3, -2,  8,  2, -1,  4]
idx:  0   1   2   3   4   5   6   7   8   9

Window 1:  [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓]                    sum =  7
           -3   4  -2   5   3

Window 2:       [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓]               sum =  8
                 4  -2   5   3  -2
                ←remove -3, add -2→

Window 3:            [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓]          sum = 12
                     -2   5   3  -2   8
                    ←remove 4, add 8→

Window 4:                 [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓]     sum = 16  ← MAX
                           5   3  -2   8   2
                          ←remove -2, add 2→

Window 5:                      [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] sum = 10
                                3  -2   8   2  -1

Window 6:                           [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] sum = 11
                                   -2   8   2  -1   4

MAXIMUM = 16  (Window 4: A[3..7])
```

---

## 🗺️ Complete Comparison

```
FORMULA: new_window_sum = old_window_sum - A[outgoing] + A[incoming]
         └────────────────────────────────────────────────────────────┘
                  Only 1 subtraction + 1 addition per window!

INDICES at each step:
  outgoing element = A[s-1]   ← element just before the new start
  incoming element = A[e]     ← new element at the right edge

EXAMPLE at step s=3, e=7:
  old sum (window [2..6]) = 12
  outgoing = A[s-1] = A[2] = -2   (was left edge of old window)
  incoming = A[e]   = A[7] =  2   (is right edge of new window)
  new sum  = 12 - (-2) + 2 = 16   ← window [3..7] ✅
```

---

## ⏱️ Complexity of All Three Approaches

| Approach       | Time           | Space | Key Operation        |
|:---------------|:--------------:|:-----:|:---------------------|
| Brute Force    | **O(N·K)**     | O(1)  | Re-sum K elements every window |
| Prefix Sum     | **O(N)**       | O(N)  | Build once, subtract once per window |
| Sliding Window | **O(N)**       | **O(1)** | Remove 1, add 1 per window |

### Speed at Scale (N=10⁵, K=10⁴)

```
O(N·K):        10^5 × 10^4 = 10^9  ⚠️  ~10 seconds
O(N) prefix:   10^5         = 10^5  ✅  instant (but uses O(N) space)
O(N) sliding:  10^5         = 10^5  ✅  instant + O(1) space  🏆
```

---

## ⚠️ Edge Cases & Pitfalls

### ❗ Pitfall 1: First Window Not Compared to `ans` (Bug in Given Code)

```python
# ❌ BUG — ans stays float('-inf'), first window NEVER compared!
ans = float('-inf')
subarraysum = 0
for i in range(0, K):
    subarraysum += A[i]

# loop starts from s=1 — ans is only updated from window 2 onward
# If the first window is the maximum, it's missed!

# ✅ FIX — set ans after computing first window
subarraysum = 0
for i in range(0, K):
    subarraysum += A[i]
ans = subarraysum   # ← capture first window's sum
```

For the given array, the bug doesn't matter because window 4 is the max.
But for `A = [9, 1, 1, 1, 1]`, K=2 → first window [9,1]=10 is the answer,
and the buggy code would miss it!

---

### ❗ Pitfall 2: Sliding Window Formula Index — `A[s-1]` Not `A[s]`

```python
# ❌ WRONG — removes current start instead of the element that LEFT
subarraysum = subarraysum - A[s] + A[e]

# ✅ CORRECT — removes the element from the PREVIOUS window's left edge
subarraysum = subarraysum - A[s-1] + A[e]
```

At step where `s=2, e=6`: the element leaving is `A[1]=4` (the old start), which is `A[s-1]`.

---

### ❗ Pitfall 3: Prefix Sum `pf_sum[-1]` Bug

```python
# ❌ When s=0: pf_sum[s-1] = pf_sum[-1] = 18 (last element) — WRONG!
subarraysum = pf_sum[e] - pf_sum[s-1]

# ✅ Guard against it:
if s == 0:
    subarraysum = pf_sum[e]
else:
    subarraysum = pf_sum[e] - pf_sum[s-1]
```

---

### ❗ Edge Case: K = N (entire array is the only window)

```python
A = [1, 2, 3, 4, 5], K = 5
→ Only one window: [1,2,3,4,5], sum = 15
→ First window IS the answer → bug in approach 3 would break this!
```

---

### ❗ Edge Case: All Negative Numbers

```python
A = [-5, -1, -3, -2], K = 2
→ Windows: [-5,-1]=-6, [-1,-3]=-4, [-3,-2]=-5
→ Answer: -4  (least negative, still correct)
→ Initialising ans = float('-inf') handles this correctly ✅
```

---

## 🧪 Test It Yourself

```python
def max_subarray_sum_k(A, K):
    n = len(A)

    # Phase 1: first window
    sub = sum(A[:K])
    ans = sub          # ← fix: capture first window!

    # Phase 2: slide
    s, e = 1, K
    while e < n:
        sub = sub - A[s-1] + A[e]
        ans = max(ans, sub)
        s += 1; e += 1

    return ans


tests = [
    ([-3,4,-2,5,3,-2,8,2,-1,4], 5, 16),  # main example
    ([1,2,3,4,5],                3, 12),  # [3,4,5]
    ([-1,-2,-3,-4],              2, -3),  # [-1,-2]
    ([5],                        1,  5),  # single element
    ([1,2,3,4,5],                5, 15),  # K==N
    ([9,1,1,1,1],                2, 10), # first window is max
]

for A, K, expected in tests:
    result = max_subarray_sum_k(A, K)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  A={A}, K={K}  → {result}")
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Prefix Sum (basic)** | Powers Approach 2 here |
| **Variable-size Sliding Window** | Window grows/shrinks based on a condition |
| **Kadane's Algorithm** | Maximum subarray of any length (not fixed K) |
| **Minimum window substring** | Sliding window on strings |
| **Sum of all subarrays** | Contribution technique — different angle |
| **Two Pointer Technique** | Related concept for sorted arrays |

---

> ✍️ **The Big Idea:**
> Brute force re-computes the entire window from scratch each slide → O(N·K).
> Prefix sum pre-builds running totals and answers each window in O(1) → O(N) time but O(N) space.
> Sliding window observes that consecutive windows **share K-1 elements** —
> only one element enters and one leaves per slide.
> So `new_sum = old_sum - outgoing + incoming` → O(1) per slide, O(N) total, O(1) space.
> This "reuse the overlap" idea is the core of the Sliding Window pattern.

---

*Happy Coding! 🚀*
