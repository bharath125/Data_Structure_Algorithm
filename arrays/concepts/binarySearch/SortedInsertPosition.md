# 📍 Sorted Insert Position — Binary Search

> **Difficulty:** Beginner → Intermediate
> **Topic:** Binary Search · Sorted Arrays · Lower Bound
> **Language:** Python
> **Constraints:** 1 ≤ N ≤ 10⁵ · 1 ≤ A[i] ≤ 10⁵ · Time: **O(log N)**

---

## 📋 Problem Statement

Given a **sorted array** A and a **target** B, return:

| Scenario | Return |
|:---------|:------:|
| B is found in A | index of B |
| B not found, but a larger element exists | index of the **first element ≥ B** |
| B not found, B is larger than all elements | `len(A)` (insert at end) |

```
In all cases: return the index where B either IS or SHOULD BE inserted
              so that the array stays sorted.
```

This is the classic **lower bound** — the leftmost position where B can live.

---

## 🌍 Real-World Analogy — Before Any Code

### 📚 Finding Your Place in a Sorted Bookshelf

Books on a shelf are arranged by ID number: `[1, 3, 5, 6]`

You want to shelve book #5 (or find where #5 belongs if it's missing).

**What would you do physically?**
- Open to the **middle of the shelf** — book #3. Too low, so look right.
- Open to the **middle of the right half** — book #5. Found it! Slot 2.

This is exactly binary search: always cut the remaining options in half.

**If the book isn't there** (say you're shelving book #4):
- After searching, you land on the gap between #3 and #5.
- The answer is the slot where #4 *would go* to keep things sorted.

---

## 🧩 Understanding the Examples

### Example 1: `A=[1,3,5,6]`, B=5 → Answer: `2`

```
Index:   0    1    2    3
Value: [ 1,   3,   5,   6 ]
                   ↑
                  B=5 found here → return index 2
```

---

### Example 2: `A=[1,4,9]`, B=3 → Answer: `1`

```
Index:   0    1    2
Value: [ 1,   4,   9 ]
              ↑
         B=3 not found. First element ≥ 3 is A[1]=4 → return index 1

If we insert 3 here: [1, 3, 4, 9] ← sorted ✅
```

---

### All Four Scenarios Shown:

```
A = [1, 3, 5, 6]

B=5: found at index 2            → return 2   (exact match)
B=2: not found, A[1]=3 is first ≥ 2 → return 1   (insert between)
B=7: not found, nothing ≥ 7     → return 4=N (insert at end)
B=0: not found, A[0]=1 is first ≥ 0 → return 0   (insert at start)
```

---

## 💡 The Key Insight — Binary Search on a Sorted Array

### Why Binary Search Works Here

The array is **sorted**. That means for any target B:

```
A = [1,  3,  5,  6]
     ↑   ↑   ↑   ↑
    <B  <B  =B  >B     (for B=5)

Pattern: [ TOO SMALL ... | VALID (≥ B) ... ]
                         ↑
               This boundary is the answer!
```

The array splits cleanly into two zones:
- **Left zone:** elements `< B`
- **Right zone:** elements `≥ B`

The boundary between them is exactly where B belongs. Binary search finds this boundary in **O(log N)**.

---

## 🔍 The Code — Every Line Explained

```python
def searchInsert(self, A, B):
    N = len(A)
    L = 0       # left boundary of search
    R = N - 1   # right boundary of search
    while L <= R:
        mid = L + (R - L) // 2
        if A[mid] == B:
            return mid
        elif A[mid] < B:
            L = mid + 1
        elif A[mid] > B:
            R = mid - 1
    return L
```

---

### Setting the Search Boundaries

```python
L = 0
R = N - 1
```

> `L` points to the **first** element. `R` points to the **last** element.
> The answer must lie somewhere in this range — or at position N (just past the end).
>
> Together, `[L, R]` defines our **search space** — the set of indices we still need to check.

---

### The Loop Condition

```python
while L <= R:
```

> The loop continues as long as there's **at least one candidate** remaining.
>
> - `L < R`: multiple candidates left
> - `L == R`: exactly one candidate left — still worth checking
> - `L > R`: search space exhausted — B was not found, return L

---

### The Overflow-Safe Midpoint

```python
mid = L + (R - L) // 2
```

> Always picks the **middle index** of the current search window.
>
> **Why not `(L + R) // 2`?**
> In C++/Java, if L and R are both near 10⁵, `L + R` approaches 2×10⁵ — fine.
> But the habit matters: for larger problems `(L + R)` overflows 32-bit integers.
> `L + (R-L)//2` is always equivalent and never overflows.
>
> ```
> L=0, R=3:  mid = 0 + (3-0)//2 = 0 + 1 = 1
> L=2, R=3:  mid = 2 + (3-2)//2 = 2 + 0 = 2
> L=2, R=2:  mid = 2 + (2-2)//2 = 2 + 0 = 2
> ```

---

### Branch 1: Exact Match

```python
if A[mid] == B:
    return mid
```

> We found B at index `mid`. Return immediately.
> No need to search further — there's only one correct index for an exact match
> in a sorted array with distinct elements.

---

### Branch 2: Mid is Too Small

```python
elif A[mid] < B:
    L = mid + 1
```

> `A[mid]` is **less than** B. Since the array is sorted, everything from
> index 0 to `mid` is also ≤ B. We can safely **discard the left half** including `mid`.
>
> Moving `L = mid + 1` eliminates `mid` and everything to its left.

```
Before:  [1,  3,  5,  6]        B=5
          L   ↑        R
             mid=1, A[1]=3 < 5
After:   [·   ·   5,  6]
                  L       R      (left half discarded)
```

---

### Branch 3: Mid is Too Large

```python
elif A[mid] > B:
    R = mid - 1
```

> `A[mid]` is **greater than** B. Since the array is sorted, everything from
> `mid` to the end is also ≥ B — but we want the **leftmost** such element,
> so we keep searching left.
>
> Moving `R = mid - 1` eliminates `mid` and everything to its right.

```
Before:  [1,  4,  9]             B=3
          L   ↑    R
             mid=1, A[1]=4 > 3
After:   [1,  ·   ·]
          L  R                   (right half discarded)
```

---

### The Final Return — Why `L`?

```python
return L
```

> When the loop ends, `L > R`. This means B was **not found**.
>
> But here's the magic: **`L` is always the correct insert position.**
>
> **Why?** Think about what happened during the search:
> - Every time `A[mid] < B`, we moved `L` rightward — eliminating elements too small.
> - Every time `A[mid] > B`, we moved `R` leftward — eliminating elements too large.
>
> When the loop ends:
> ```
> Everything at index < L  has value < B   (L was pushed past them)
> Everything at index > R  has value > B   (R was pushed past them)
> Since L = R+1:  A[L-1] < B < A[L]
>                           ↑
>                    L is the gap where B belongs!
> ```
>
> Three cases are handled automatically:
> - **B fits in the middle:** `A[L-1] < B < A[L]` → insert at L
> - **B is beyond the end:** L advances all the way to N → return N
> - **B is before the start:** R retreats to -1, L stays at 0 → return 0

---

## 📊 Full Dry Run — Example 1: `A=[1,3,5,6]`, B=5

**Initial:** L=0, R=3

```
Array:   [  1,    3,    5,    6  ]
Index:      0     1     2     3
            L                 R
```

**Step 1:**
```
mid = 0 + (3-0)//2 = 1
A[1] = 3
3 < 5? ✅ YES → L = mid+1 = 2

Array:   [  ✗,    ✗,    5,    6  ]
                         L     R
             (left half discarded — all too small)
```

**Step 2:**
```
mid = 2 + (3-2)//2 = 2
A[2] = 5
5 == 5? ✅ EXACT MATCH → return 2
```

**Answer: 2** ✅

---

## 📊 Full Dry Run — Example 2: `A=[1,4,9]`, B=3

**Initial:** L=0, R=2

```
Array:   [  1,    4,    9  ]
Index:      0     1     2
            L           R
```

**Step 1:**
```
mid = 0 + (2-0)//2 = 1
A[1] = 4
4 > 3? ✅ YES → R = mid-1 = 0

Array:   [  1,    ✗,    ✗  ]
            L  R
             (right half discarded — all too large)
```

**Step 2:**
```
mid = 0 + (0-0)//2 = 0
A[0] = 1
1 < 3? ✅ YES → L = mid+1 = 1

Array:   [  ✗,    ✗,    ✗  ]
               L  (L=1)
             R=-… wait: R=0
```

**L=1 > R=0 → loop ends → return L = 1**

```
Verify: A[0]=1 < B=3 < A[1]=4  → insert at index 1 ✅
If inserted: [1, 3, 4, 9]  ← sorted ✅
```

---

## 📊 Dry Run — B=7 (Beyond All Elements)

`A=[1,3,5,6]`, B=7

| Step | L | R | `mid` | `A[mid]` | Comparison  | Action    |
|:----:|:-:|:-:|:-----:|:--------:|:-----------:|:----------|
| 1    | 0 | 3 | 1     | 3        | 3 < 7       | L = 2     |
| 2    | 2 | 3 | 2     | 5        | 5 < 7       | L = 3     |
| 3    | 3 | 3 | 3     | 6        | 6 < 7       | L = 4     |

L=4 > R=3 → **return L=4 = N** (insert at end)

```
Verify: [1, 3, 5, 6, 7]  ← sorted ✅
```

---

## 📊 Dry Run — B=0 (Before All Elements)

`A=[1,3,5,6]`, B=0

| Step | L | R  | `mid` | `A[mid]` | Comparison | Action    |
|:----:|:-:|:--:|:-----:|:--------:|:----------:|:----------|
| 1    | 0 | 3  | 1     | 3        | 3 > 0      | R = 0     |
| 2    | 0 | 0  | 0     | 1        | 1 > 0      | R = -1    |

L=0 > R=-1 → **return L=0** (insert at start)

```
Verify: [0, 1, 3, 5, 6]  ← sorted ✅
```

---

## 🗺️ Visual — How L and R Close In

```
A = [1,  3,  5,  6],  B = 5

Start:
  idx:  0    1    2    3
  val: [1,   3,   5,   6]
        L              R

Step 1: mid=1, A[1]=3 < 5 → L moves right
  idx:  0    1    2    3
  val: [✗,   ✗,   5,   6]
                  L    R
       ← discarded →

Step 2: mid=2, A[2]=5 == 5 → FOUND!
  idx:  0    1    2    3
  val: [✗,   ✗,  [5],  6]
                  ↑
               return 2
```

```
A = [1,  4,  9],  B = 3

Start:
  idx:  0    1    2
  val: [1,   4,   9]
        L         R

Step 1: mid=1, A[1]=4 > 3 → R moves left
  idx:  0    1    2
  val: [1,   ✗,   ✗]
        L  R
            ← discarded →

Step 2: mid=0, A[0]=1 < 3 → L moves right
  idx:  0    1    2
  val: [✗,   ✗,   ✗]
            L
         R (=-1 conceptually)
       ← discarded →

L=1 > R=0 → return L=1
  Insert here: [1, (3), 4, 9]  ✅
```

---

## 🔑 The Proof: Why `return L` is Always Correct

When the while loop ends (`L > R`), the following is guaranteed:

```
All elements at indices 0 .. L-1  are  < B    (L was pushed past them)
All elements at indices L .. N-1  are  > B    (R was pushed past them)
                                  ↑
                      L is the insertion point!
```

This holds in all cases:

| Case              | Final State    | Return | Why Correct                        |
|:------------------|:---------------|:------:|:-----------------------------------|
| B found           | early return   | `mid`  | Exact match                        |
| B in middle       | L crossed R    | `L`    | `A[L-1]<B<A[L]`                    |
| B before start    | R went to -1   | `0`    | `A[0]>B`, L stayed at 0            |
| B after end       | L went to N    | `N`    | All elements `<B`, L pushed to end |

---

## ⏱️ Complexity Analysis

| Aspect  | Value        | Reason                                      |
|:--------|:------------:|:--------------------------------------------|
| Time    | **O(log N)** | Search space halves every iteration         |
| Space   | **O(1)**     | Only 3 variables: L, R, mid                 |

```
N = 100,000

Linear scan O(N): up to 100,000 comparisons
Binary search O(log N): at most log₂(100,000) ≈ 17 comparisons

17 vs 100,000 — binary search is ~6,000× faster!
```

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: `while L < R` Instead of `while L <= R`

```python
while L < R:   # ❌ WRONG — misses when exactly one element remains
```

When `L == R`, there's one element left — it might be the answer or the insert point.
Using `<` skips this check, causing off-by-one errors.

```python
while L <= R:  # ✅ CORRECT — checks the single remaining element
```

---

### ❗ Pitfall 2: `return R` or `return mid` Instead of `return L`

```python
return R     # ❌ WRONG — R ends at L-1 (one behind the insert point)
return mid   # ❌ WRONG — mid's final value is unpredictable
return L     # ✅ CORRECT — L is exactly the insert position
```

When the loop ends, `R = L - 1`. Returning R gives the index just **before** the insert point — off by one.

---

### ❗ Pitfall 3: Using `>` Instead of `>=` in the Condition

```python
if A[mid] < B:
    L = mid + 1
else:          # ← catches both == and > in one branch
    R = mid - 1
```

This works, but then you never have an early return for exact matches. The algorithm still returns the correct index via `return L`, but is slightly less efficient (always runs to completion even when B is found).

The explicit three-branch version (`==`, `<`, `>`) with early return is cleaner and exits faster on a hit.

---

### ❗ Pitfall 4: Returning `N+1` for "Not Found" Instead of `N`

The problem says: if B is larger than all elements, return `len(A)` (position N, 0-indexed).

```python
return L   # ✅ When B > all elements, L naturally reaches N (= len(A))
```

This is automatically correct — no special case needed.

---

## 🧪 Test It Yourself

```python
def searchInsert(A, B):
    N = len(A)
    L = 0
    R = N - 1
    while L <= R:
        mid = L + (R - L) // 2
        if A[mid] == B:
            return mid
        elif A[mid] < B:
            L = mid + 1
        else:
            R = mid - 1
    return L


tests = [
    ([1,3,5,6],  5, 2),   # exact match in middle
    ([1,4,9],    3, 1),   # insert between elements
    ([1,3,5,6],  2, 1),   # insert between 1 and 3
    ([1,3,5,6],  7, 4),   # insert at end (return N)
    ([1,3,5,6],  0, 0),   # insert at start
    ([1,3,5,6],  1, 0),   # exact match at index 0
    ([1,3,5,6],  6, 3),   # exact match at last index
    ([1],        1, 0),   # single element, match
    ([1],        2, 1),   # single element, insert after
    ([1],        0, 0),   # single element, insert before
]

for A, B, expected in tests:
    result = searchInsert(A, B)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  A={A}  B={B}  → {result}")
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Binary Search (classic)** | Find exact element in sorted array — same structure |
| **Square Root (floor)** | Binary search on answer with a mathematical condition |
| **First Bad Version** | Find leftmost True in a True/False sorted sequence |
| **Search in Rotated Array** | Binary search where the monotone property is broken once |
| **Find First and Last Position** | Two binary searches: lower bound + upper bound |
| **Lower / Upper Bound (C++ STL)** | `lower_bound()` does exactly what this function does |

---

> ✍️ **The Big Idea:**
> Binary search isn't only for finding exact values. It's a general tool for
> locating a **boundary** in any sorted or monotone sequence.
> Here, the boundary separates "too small" from "big enough."
> The three-branch logic — equal (return immediately), too small (go right),
> too big (go left) — progressively narrows the search space.
> When the space is empty (`L > R`), `L` is sitting precisely at the
> insertion point: everything to its left is `< B`, everything to its right is `> B`.
> No special cases needed for any scenario — `return L` handles them all.

---

*Happy Coding! 🚀*
