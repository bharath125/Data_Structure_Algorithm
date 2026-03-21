# 🏔️ Find a Peak Element — Binary Search

> **Difficulty:** Beginner → Advanced
> **Topic:** Binary Search · Divide & Conquer · Array Topology
> **Language:** Python
> **Constraints:** 1 ≤ N ≤ 10⁵ · 1 ≤ A[i] ≤ 10⁹ · Time: **O(log N)**

---

## 📋 Problem Statement

Given an integer array **A**, find and return a **peak element**.

**Definition of a Peak:**
```
An element A[i] is a PEAK if it is NOT SMALLER than its neighbors.

For inner elements (1 ≤ i ≤ N-2):
    A[i] is a peak  if  A[i] >= A[i-1]  AND  A[i] >= A[i+1]

For the first element (i = 0):
    A[0] is a peak  if  A[0] >= A[1]        (only one neighbor)

For the last element (i = N-1):
    A[N-1] is a peak  if  A[N-1] >= A[N-2]  (only one neighbor)
```

**Guarantees:**
- Exactly **one** peak exists in the array
- Array may contain **duplicate** elements
- Must solve in **O(log N)** time

---

## 🌍 Real-World Analogy — Before Any Code

### 🏔️ Hiking in the Mountains

Imagine you're hiking along a mountain trail and want to reach the **summit** (peak).

You're standing at some point on the trail and can see one step left and one step right.

**What's your strategy?**
- Look left and right
- If the ground **rises to your right** → walk right (the peak is in that direction)
- If the ground **rises to your left** → walk left (the peak is in that direction)
- If you're **higher than both sides** → you're at the peak!

You never need to walk the entire trail. Every step you take **eliminates half the remaining trail**. That's binary search on a mountain.

---

## 🧩 Understanding the Problem Constraints — Line by Line

### Constraint 1: "NOT SMALLER than its neighbors"

```python
A[i] >= A[i-1]   AND   A[i] >= A[i+1]
```

> This uses `>=` not `>`. An element **equal** to its neighbour is still a valid peak.
>
> ```
> A = [3, 3, 3]
>      ↑ peak?    A[0]=3 >= A[1]=3 → YES, A[0] is a peak ✅
>         ↑ peak? A[1]=3 >= A[0]=3 AND A[1]=3 >= A[2]=3 → YES ✅
> ```
>
> The problem says only ONE peak exists, so duplicates at corners are fine.

---

### Constraint 2: "Corner elements have only one neighbour"

```
Index:   0     1     2     3     4
Array: [ 5,   17,  100,   11,   1 ]
         ↑                       ↑
     first element           last element
     only right neighbour    only left neighbour
```

> `A[0]` has no left neighbour — only compare with `A[1]`.
> `A[N-1]` has no right neighbour — only compare with `A[N-2]`.
> The code handles these with explicit checks **before** the binary search loop.

---

### Constraint 3: "Exactly one peak"

> This guarantee is what makes binary search valid here. If multiple peaks existed,
> the algorithm might converge to the wrong one. With exactly one peak, every
> "go right" or "go left" decision is always pointing toward the unique peak.

---

### Constraint 4: "O(log N) time"

> A brute force scan (`A[i] >= A[i-1] and A[i] >= A[i+1]` for every i) = O(N).
> The constraint forces binary search — eliminate half the array each step.

---

## 💡 The Core Insight — Why Binary Search Works Here

At first glance, binary search seems wrong — the array isn't sorted. So why does it work?

**Key observation: At any mid point, one of three things is true:**

```
Case 1: A[mid] >= A[mid-1] AND A[mid] >= A[mid+1]
        → mid IS the peak. Done!

Case 2: A[mid+1] > A[mid]   (right neighbour is larger)
        → The right side is "going uphill"
        → A PEAK MUST EXIST IN THE RIGHT HALF [mid+1 .. R]
        → Move L = mid+1  (safely ignore left half)

Case 3: A[mid-1] > A[mid]   (left neighbour is larger)
        → The left side is "going uphill"
        → A PEAK MUST EXIST IN THE LEFT HALF [L .. mid-1]
        → Move R = mid-1  (safely ignore right half)
```

**Why can we safely ignore the other half?**

Think of it like a slope guarantee:

```
If A[mid] < A[mid+1]:
  We know A[mid+1] > A[mid].
  Either A[mid+1] is the peak itself,
  or the array continues rising, then must fall at some point.
  Either way, a peak EXISTS in [mid+1, N-1].
  We will NEVER miss the peak by going right.
```

This is the **fundamental theorem** of this algorithm: on any uphill slope, the peak is ahead.

---

## 🔍 The Code — Every Line Explained

```python
def solve(self, A):
    N = len(A)

    # ── Layer 1: Instant-answer cases ───────────────────────────────
    if N == 1: return A[0]
    elif A[0] >= A[1]: return A[0]
    elif A[N-1] >= A[N-2]: return A[N-1]

    # ── Layer 2: Binary search on inner elements only ────────────────
    L = 1
    R = N - 2

    while L <= R:
        mid = L + (R - L) // 2

        if A[mid] >= A[mid-1] and A[mid] >= A[mid+1]:
            return A[mid]          # mid is the peak
        elif A[mid+1] >= A[mid]:
            L = mid + 1            # go right (uphill to the right)
        else:
            R = mid - 1            # go left  (uphill to the left)

    return -1                      # never reached for valid inputs
```

---

### `if N == 1: return A[0]`

```python
if N == 1: return A[0]
```

> **Single element array.** There are no neighbours. By definition, a corner element
> is a peak when it's not smaller than its *existing* neighbours — and it has none.
> So it's automatically a peak.
>
> ```
> A = [42]  →  return 42  ✅
> ```
>
> Without this guard, `A[1]` in the next check would be an `IndexError`.

---

### `elif A[0] >= A[1]: return A[0]`

```python
elif A[0] >= A[1]: return A[0]
```

> **First element is a peak.** The first element only has one neighbour: `A[1]`.
> If `A[0] >= A[1]`, the first element is not smaller than its only neighbour → peak!
>
> ```
> A = [5, 3, 1]   →  A[0]=5 >= A[1]=3  →  return 5  ✅
> A = [3, 3, 1]   →  A[0]=3 >= A[1]=3  →  return 3  ✅  (equal is also peak)
> A = [1, 3, 2]   →  A[0]=1 >= A[1]=3? NO → continue
> ```
>
> This also handles all **strictly decreasing** arrays — the first element is always
> the peak since it's the largest.

---

### `elif A[N-1] >= A[N-2]: return A[N-1]`

```python
elif A[N-1] >= A[N-2]: return A[N-1]
```

> **Last element is a peak.** Mirror of the above. Only neighbour is `A[N-2]`.
>
> ```
> A = [1, 2, 3, 4, 5]  →  A[4]=5 >= A[3]=4  →  return 5  ✅
> A = [1, 3, 5, 5]     →  A[3]=5 >= A[2]=5  →  return 5  ✅  (equal is fine)
> ```
>
> This handles all **strictly increasing** arrays. The last element is always the peak.

---

### `L = 1` and `R = N - 2`

```python
L = 1
R = N - 2
```

> **Why not `L=0, R=N-1`?**
>
> The corner elements `A[0]` and `A[N-1]` were **already checked** and found not to be peaks.
> We know the peak is somewhere in the **interior** — indices 1 through N-2.
>
> More importantly: the peak check `A[mid] >= A[mid-1] AND A[mid] >= A[mid+1]`
> accesses `A[mid-1]` and `A[mid+1]`. If `mid=0`, then `A[mid-1]=A[-1]` in Python
> gives the **last element** — a silent wrong answer! If `mid=N-1`, then `A[mid+1]=A[N]`
> causes an `IndexError`.
>
> Starting at `L=1` and `R=N-2` means `mid` is always in `[1, N-2]`:
> - `mid-1` is always ≥ 0 → safe
> - `mid+1` is always ≤ N-1 → safe

---

### `mid = L + (R - L) // 2`

```python
mid = L + (R - L) // 2
```

> Overflow-safe midpoint. In Python, integers don't overflow, but this formula is
> good practice — in C++/Java, `(L + R) // 2` can overflow when L and R are both large.
>
> `L + (R-L)//2` = L + half-the-gap = midpoint. Always safe.

---

### The Three-Branch Decision

```python
if A[mid] >= A[mid-1] and A[mid] >= A[mid+1]:
    return A[mid]          # ← PEAK FOUND
elif A[mid+1] >= A[mid]:
    L = mid + 1            # ← right neighbour is bigger: go RIGHT
else:
    R = mid - 1            # ← left neighbour is bigger: go LEFT
```

**Branch 1 — Peak found:**
> `mid` is larger than or equal to both neighbours. This is the peak. Return immediately.

**Branch 2 — Right is uphill:**
> `A[mid+1] >= A[mid]`. The terrain rises to the right. The peak lies somewhere in `[mid+1, R]`.
> Discard `[L, mid]` by moving `L = mid+1`.
>
> **Why is this safe?** The corner check already proved `A[N-1]` is not a peak.
> So the array must "come down" somewhere after `mid+1`. That coming-down point is the peak.

**Branch 3 — Left is uphill (else):**
> `A[mid-1] > A[mid]` (the only remaining case after branches 1 and 2).
> The terrain rises to the left. The peak lies in `[L, mid-1]`.
> Discard `[mid, R]` by moving `R = mid-1`.

---

### `return -1`

```python
return -1
```

> **Defensive programming.** The problem guarantees a peak exists.
> Given the corner checks and binary search, the loop will **always** return
> before reaching this line. The `-1` is a safety net — it is never executed
> for valid inputs, but keeps the function syntactically correct.

---

## 📊 Full Dry Run — Example 1: `A=[1,2,3,4,5]`

```
N=5

Check 1: N==1? NO
Check 2: A[0]=1 >= A[1]=2? NO (1 < 2, so first element is not a peak)
Check 3: A[4]=5 >= A[3]=4? YES ✅ → return 5
```

**Answer: 5** ✅ — handled entirely by the corner checks, binary search never runs!

---

## 📊 Full Dry Run — Example 2: `A=[5,17,100,11]`

```
N=4

Check 1: N==1? NO
Check 2: A[0]=5 >= A[1]=17? NO
Check 3: A[3]=11 >= A[2]=100? NO
Binary search: L=1, R=2
```

```
Array:   [  5,   17,  100,   11  ]
Index:      0     1     2     3
                  L     R
```

**Step 1:**
```
mid = 1 + (2-1)//2 = 1
A[1] = 17

A[mid-1]=A[0]=5    A[mid]=17    A[mid+1]=A[2]=100

Peak? 17>=5 AND 17>=100? NO (17 < 100)
Right uphill? A[2]=100 >= A[1]=17? YES ✅
→ L = mid+1 = 2

Array:   [  5,   ✗,   100,   11  ]
                       L  R
              (left half eliminated)
```

**Step 2:**
```
mid = 2 + (2-2)//2 = 2
A[2] = 100

A[mid-1]=A[1]=17    A[mid]=100    A[mid+1]=A[3]=11

Peak? 100>=17 AND 100>=11? YES ✅ → return 100
```

**Answer: 100** ✅

---

## 📊 Full Dry Run — `A=[1,3,2]` (Peak in the Middle)

```
N=3

Check 1: N==1? NO
Check 2: A[0]=1 >= A[1]=3? NO
Check 3: A[2]=2 >= A[1]=3? NO
Binary search: L=1, R=1
```

```
Step 1:
  mid = 1+(1-1)//2 = 1
  A[0]=1, A[1]=3, A[2]=2
  3>=1 AND 3>=2? YES ✅ → return 3
```

**Answer: 3** ✅ — single binary search step finds it immediately.

---

## 📊 Dry Run — `A=[3,2,1]` (Strictly Decreasing)

```
Check 1: N==1? NO
Check 2: A[0]=3 >= A[1]=2? YES ✅ → return 3
```

**Answer: 3** ✅ — first element is the peak, handled by the corner check.

---

## 📊 Dry Run — `A=[5,5,5,5]` (All Duplicates)

```
Check 1: N==1? NO
Check 2: A[0]=5 >= A[1]=5? YES ✅ → return 5  (equal counts as peak!)
```

**Answer: 5** ✅

---

## 🎨 Visual — Why Going Uphill Always Leads to the Peak

```
Imagine the array values as a landscape:

A = [1, 3, 5, 4, 2]    ← mountain shape

        5         ← PEAK
       / \
      3   4
     /     \
    1       2

mid=2 (val=5): 5>=3 AND 5>=4 → PEAK! ✅

─────────────────────────────────────────────────────

A = [1, 2, 5, 3, 4]    ← peak at index 2, uphill on right at start

        5
       / \
      2   3   4  ← still going up at end
     /           
    1            

mid=2 (val=5): 5>=2 AND 5>=3 → PEAK! ✅

─────────────────────────────────────────────────────

A = [1, 2, 3, 4, 5]    ← strictly increasing

                5   ← PEAK (corner)
              /
            4
          /
        3
      /
    2
  /
1

Check A[N-1]=5 >= A[N-2]=4 → YES → return 5  (before binary search runs) ✅

─────────────────────────────────────────────────────

THE GUARANTEE:
  If A[mid] < A[mid+1]:
  The slope is GOING UP to the right.
  Since the array ends at a finite point, it MUST come down somewhere.
  That "coming down" point is the peak.
  So: peak EXISTS in [mid+1, N-1].  Safe to go right.
```

---

## 🔑 The Three Checks — When Each Fires

| Check | Condition | Meaning | Action |
|:------|:----------|:--------|:-------|
| `N==1` | Single element | Trivially a peak | Return `A[0]` |
| `A[0]>=A[1]` | First ≥ second | First element is a peak | Return `A[0]` |
| `A[N-1]>=A[N-2]` | Last ≥ second-to-last | Last element is a peak | Return `A[N-1]` |
| `A[mid]>=both` | Mid ≥ both neighbours | Mid is the peak | Return `A[mid]` |
| `A[mid+1]>=A[mid]` | Right uphill | Peak is to the right | `L = mid+1` |
| else | Left uphill | Peak is to the left | `R = mid-1` |

---

## ⏱️ Complexity Analysis

| Aspect  | Value          | Reason                                        |
|:--------|:--------------:|:----------------------------------------------|
| Time    | **O(log N)**   | Search space halves every iteration           |
| Space   | **O(1)**       | Only 4 variables: N, L, R, mid                |

```
N = 100,000

Brute force O(N):   100,000 comparisons
Binary search O(log N): log₂(100,000) ≈ 17 comparisons

~6,000× faster!
```

---

## ⚠️ Common Pitfalls & Edge Cases

### ❗ Pitfall 1: Using `L=0, R=N-1` Without Corner Guards

```python
# ❌ WRONG — mid can become 0 or N-1, causing index errors or Python's -1 bug
L, R = 0, N-1
while L <= R:
    mid = L + (R-L)//2
    if A[mid] >= A[mid-1] and ...   # mid=0 → A[-1] = last element! Silent bug!
```

```python
# ✅ CORRECT — handle corners first, search only inner elements
if A[0] >= A[1]: return A[0]       # corner guard
if A[N-1] >= A[N-2]: return A[N-1] # corner guard
L, R = 1, N-2                       # safe: mid-1 >= 0, mid+1 <= N-1 always
```

---

### ❗ Pitfall 2: Using `>` Instead of `>=` for the Peak Check

```python
# ❌ WRONG — misses peaks with equal neighbours
if A[mid] > A[mid-1] and A[mid] > A[mid+1]:

# Test: A=[3,3,3] → no element satisfies strict >, returns -1 ❌
```

```python
# ✅ CORRECT — equal neighbours are also valid
if A[mid] >= A[mid-1] and A[mid] >= A[mid+1]:
```

---

### ❗ Pitfall 3: Using `>` Instead of `>=` in the Direction Check

```python
# ❌ WRONG — if A[mid+1] == A[mid], neither branch fires for direction!
elif A[mid+1] > A[mid]:
    L = mid + 1
else:
    R = mid - 1

# If A[mid+1]==A[mid] and the peak condition also fails → infinite loop or wrong result!
```

```python
# ✅ CORRECT — >= ensures one branch always fires when peak isn't found
elif A[mid+1] >= A[mid]:
    L = mid + 1
else:
    R = mid - 1
```

---

### ❗ Pitfall 4: Forgetting the `N==1` Guard

```python
# Without N==1 guard:
if A[0] >= A[1]   # IndexError when N=1! A[1] doesn't exist
```

Always check `N==1` first — it's the base case that makes all subsequent checks safe.

---

### ❗ Edge Case: Two-Element Array

```python
A = [3, 1]   # N=2
→ A[0]=3 >= A[1]=1 → return 3 ✅

A = [1, 3]   # N=2
→ A[0]=1 >= A[1]=3? NO
→ A[1]=3 >= A[0]=1? YES → return 3 ✅
```

Both cases handled by corner checks. Binary search never runs (L=1, R=0 → L>R).

---

## 🧪 Test It Yourself

```python
def solve(A):
    N = len(A)
    # Corner cases
    if N == 1: return A[0]
    if A[0] >= A[1]: return A[0]
    if A[N-1] >= A[N-2]: return A[N-1]
    # Binary search on inner elements
    L, R = 1, N-2
    while L <= R:
        mid = L + (R - L) // 2
        if A[mid] >= A[mid-1] and A[mid] >= A[mid+1]:
            return A[mid]
        elif A[mid+1] >= A[mid]:
            L = mid + 1
        else:
            R = mid - 1
    return -1   # never reached for valid inputs


tests = [
    ([1,2,3,4,5],    5,   "increasing → last element"),
    ([5,17,100,11],  100, "peak in middle"),
    ([1],            1,   "single element"),
    ([3,1],          3,   "two elements, first is peak"),
    ([1,3],          3,   "two elements, last is peak"),
    ([1,3,2],        3,   "peak in middle"),
    ([5,5,5,5],      5,   "all duplicates"),
    ([1,2,1],        2,   "simple mountain"),
    ([3,2,1],        3,   "decreasing → first is peak"),
    ([1,3,5,4,2],    5,   "mountain, binary search finds middle"),
]

for A, expected, desc in tests:
    result = solve(A)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  {desc}  A={A}  → {result}")
```

---

## 🗺️ Complete Visual Summary

```
ALGORITHM FLOW:

Input: A, N = len(A)

    ┌─────────────────────────────────────────────────┐
    │  Layer 1: Instant Answers (O(1))                │
    │                                                 │
    │  N==1?          → return A[0]                   │
    │  A[0]>=A[1]?    → return A[0]  (left corner)   │
    │  A[N-1]>=A[N-2]?→ return A[N-1] (right corner) │
    └────────────────────────┬────────────────────────┘
                             │ All corners checked — peak is INSIDE
                             ▼
    ┌─────────────────────────────────────────────────┐
    │  Layer 2: Binary Search on [1, N-2]  (O(log N))│
    │                                                 │
    │  mid = midpoint of [L, R]                       │
    │                                                 │
    │  A[mid]>=both neighbours? → PEAK! return A[mid] │
    │                                                 │
    │  A[mid+1]>=A[mid]?        → go RIGHT (L=mid+1) │
    │  else                     → go LEFT  (R=mid-1) │
    │                                                 │
    │  Repeat until L > R                             │
    └─────────────────────────────────────────────────┘

KEY INSIGHT:
  Moving toward the HIGHER neighbour always leads to the peak.
  On an uphill slope, the peak is ahead.
  On a downhill slope, the peak is behind.
  Binary search exploits this to eliminate half the array each step.
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Binary Search on Answer** | Same "eliminate half" idea with a custom condition |
| **Sorted Insert Position** | Binary search for a boundary in a sorted array |
| **First and Last Occurrence** | Binary search biased left or right on match |
| **Find Minimum in Rotated Array** | Binary search on a "broken" monotone array |
| **Mountain Array** | Related: finding the peak index of a bitonic array |
| **Divide & Conquer** | Peak finding is a classic D&C problem at O(log N) |

---

> ✍️ **The Big Idea:**
> Binary search doesn't need a sorted array — it needs a **decision rule**
> that reliably eliminates half the remaining candidates.
> Here, the rule is: "Move toward the higher neighbour."
> On any slope, the peak lies in the direction of the higher side.
> The three corner checks (N=1, first element, last element) handle all edge
> cases before binary search starts, ensuring `mid-1` and `mid+1` are always
> valid indices inside the loop. Together, the algorithm finds the peak in at most
> ⌈log₂(N)⌉ steps — regardless of where the peak is.

---

*Happy Coding! 🚀*
