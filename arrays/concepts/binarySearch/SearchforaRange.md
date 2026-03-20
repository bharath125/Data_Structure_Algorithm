# 🎯 First and Last Occurrence — Two Binary Searches

> **Difficulty:** Beginner → Intermediate
> **Topic:** Binary Search · Lower Bound · Upper Bound · Sorted Arrays
> **Language:** Python
> **Constraints:** 1 ≤ N ≤ 10⁶ · 1 ≤ A[i], B ≤ 10⁹ · Time: **O(log N)**

---

## 📋 Problem Statement

Given a **sorted array** A and a **target** B, return `[first_index, last_index]` where B appears.

| Scenario | Return |
|:---------|:------:|
| B exists once | `[i, i]` |
| B exists multiple times | `[leftmost_i, rightmost_i]` |
| B not found | `[-1, -1]` |

```
A = [5, 7, 7, 8, 8, 10],  B = 8
                   ↑  ↑
              first=3  last=4   →  return [3, 4]
```

---

## 🌍 Real-World Analogy — Before Any Code

### 📖 Finding a Word in a Dictionary

Imagine a printed dictionary where the word **"mango"** appears on several consecutive pages (maybe the main entry, plural, origin, etc.).

You want to know: **which is the first page it appears on, and which is the last?**

**Strategy:**
1. Open to the **middle** — too early? Jump right. Too late? Jump left.
2. Once you land on "mango", don't stop — **close the back cover and keep searching leftward** for an even earlier occurrence. That finds the **first** page.
3. Repeat the whole search from scratch, but this time when you find "mango", **close the front cover and search rightward** for an even later occurrence. That finds the **last** page.

Two independent binary searches. Same array, same target, opposite tiebreaking direction. That's exactly this algorithm.

---

## 🧩 Understanding the Examples

### Example 1: `A=[5,7,7,8,8,10]`, B=8

```
Index:   0    1    2    3    4    5
Value: [ 5,   7,   7,   8,   8,  10 ]
                        ↑    ↑
                    first=3  last=4

Return [3, 4] ✅
```

B=8 appears at indices 3 and 4. First = 3, Last = 4.

---

### Example 2: `A=[5,17,100,111]`, B=3

```
Index:   0    1    2    3
Value: [ 5,  17,  100, 111]
  B=3 is not in the array → Return [-1, -1] ✅
```

---

### More Scenarios on One Array:

```
A = [1, 1, 1, 1, 1]  B=1 →  [0, 4]  (appears everywhere)
A = [1, 2, 3, 4, 5]  B=3 →  [2, 2]  (appears exactly once)
A = [8, 8, 8, 8]     B=8 →  [0, 3]  (entire array)
A = [1, 2, 3, 4, 5]  B=6 →  [-1,-1] (not present)
```

---

## 💡 The Core Insight — Two Directed Binary Searches

A naive approach would:
1. Binary search to find **any** index where B appears
2. Walk left to find the first
3. Walk right to find the last

But steps 2 and 3 are **O(N)** in the worst case (e.g., all elements equal to B).

**The O(log N) insight:** Run binary search **twice** — once biased left, once biased right.

```
Standard binary search: when A[mid]==B, STOP and return mid

First occurrence:       when A[mid]==B, SAVE mid, then go LEFT  (maybe there's an earlier one!)
Last  occurrence:       when A[mid]==B, SAVE mid, then go RIGHT (maybe there's a later one!)
```

The only difference between the two searches is **one line** — what happens when you find a match.

---

## 🔍 The Code — Every Line Explained

```python
def searchRange(self, A, B):
    N = len(A)

    # ── SEARCH 1: Find FIRST occurrence ─────────────────────────────────
    L = 0
    R = N - 1
    first_occ = -1                    # assume B is not found

    while L <= R:
        mid = L + (R - L) // 2
        if A[mid] == B:
            first_occ = mid           # found a match — save it
            R = mid - 1               # but keep searching LEFT for an earlier one
        elif A[mid] < B:
            L = mid + 1               # B is to the right
        else:
            R = mid - 1               # B is to the left

    # ── SEARCH 2: Find LAST occurrence ──────────────────────────────────
    Lo = 0
    Ro = N - 1
    sec_occ = -1                      # assume B is not found

    while Lo <= Ro:
        mid = Lo + (Ro - Lo) // 2
        if A[mid] == B:
            sec_occ = mid             # found a match — save it
            Lo = mid + 1              # but keep searching RIGHT for a later one
        elif A[mid] < B:
            Lo = mid + 1              # B is to the right
        else:
            Ro = mid - 1              # B is to the left

    return [first_occ, sec_occ]
```

---

### `first_occ = -1` and `sec_occ = -1`

```python
first_occ = -1
sec_occ   = -1
```

> Both start at `-1` — the sentinel meaning "B has not been found yet."
> If neither search ever hits `A[mid] == B`, both remain `-1` and we return `[-1, -1]`.
> This elegantly handles the "not found" case with no extra code.

---

### The Midpoint Formula

```python
mid = L + (R - L) // 2
```

> Overflow-safe midpoint. `(L + R) // 2` is equivalent but can overflow in C++/Java
> when `L` and `R` are near `10⁹`. `L + (R-L)//2` never overflows because `R-L ≤ N`.
> In Python there's no overflow, but the habit is good practice.

---

### Search 1 — The First Occurrence Branch

```python
if A[mid] == B:
    first_occ = mid    # ← save this match
    R = mid - 1        # ← keep hunting LEFT
```

> This is the heart of the first-occurrence logic.
>
> When we find B at `mid`, we don't stop. We record it and ask:
> *"Could there be an even earlier copy of B to the left of mid?"*
>
> By setting `R = mid - 1`, we shrink the search space to `[L, mid-1]` —
> everything to the left of where we just found B.
> If an earlier copy exists, we'll find it. If not, `first_occ` keeps
> the best (leftmost) answer seen so far.

```
A = [5, 7, 7, 8, 8, 10],  B=8

Found at mid=4 → save first_occ=4, search [L..3]
Found at mid=3 → save first_occ=3, search [L..2]
  3 < 3? False → stop
Answer: first_occ = 3  ✅ (leftmost 8)
```

---

### Search 2 — The Last Occurrence Branch

```python
if A[mid] == B:
    sec_occ = mid      # ← save this match
    Lo = mid + 1       # ← keep hunting RIGHT
```

> Mirror of the first search. When we find B at `mid`, we record it and ask:
> *"Could there be an even later copy of B to the right of mid?"*
>
> By setting `Lo = mid + 1`, we search `[mid+1, Ro]` — everything to the right.
> If a later copy exists, we'll find it. If not, `sec_occ` holds the rightmost answer.

```
A = [5, 7, 7, 8, 8, 10],  B=8

Found at mid=4 → save sec_occ=4, search [5..Ro]
  A[5]=10 > 8 → Ro=4
  Lo=5 > Ro=4 → stop
Answer: sec_occ = 4  ✅ (rightmost 8)
```

---

### The One-Line Difference

```
             A[mid] == B  →  what happens next?
             ───────────────────────────────────
First occ:   first_occ = mid  |  R  = mid - 1   (go LEFT)
Last  occ:   sec_occ   = mid  |  Lo = mid + 1   (go RIGHT)
```

Everything else in the two loops is **identical**. The entire algorithm's logic lives in this one directional choice.

---

## 📊 Full Dry Run — Example 1: `A=[5,7,7,8,8,10]`, B=8

### Search 1: First Occurrence

**Initial:** L=0, R=5, first_occ=-1

```
Array:   [  5,    7,    7,    8,    8,   10  ]
Index:      0     1     2     3     4     5
            L                             R
```

**Step 1:**
```
mid = 0 + (5-0)//2 = 2
A[2] = 7
7 < 8 → B is to the right → L = mid+1 = 3

Eliminated: [  ✗,    ✗,    ✗,    8,    8,   10  ]
                                  L              R
```

**Step 2:**
```
mid = 3 + (5-3)//2 = 4
A[4] = 8
8 == 8 ✅ → first_occ = 4, R = mid-1 = 3  (search left!)

Saved:     first_occ = 4 (for now)
Remaining: [  ✗,    ✗,    ✗,    8,    ✗,    ✗  ]
                                  L  R
```

**Step 3:**
```
mid = 3 + (3-3)//2 = 3
A[3] = 8
8 == 8 ✅ → first_occ = 3, R = mid-1 = 2  (search left again!)

Saved:     first_occ = 3 (updated — found an earlier one!)
```

**L=3 > R=2 → loop ends → first_occ = 3** ✅

---

### Search 2: Last Occurrence

**Initial:** Lo=0, Ro=5, sec_occ=-1

**Step 1:**
```
mid = 0 + (5-0)//2 = 2
A[2] = 7 < 8 → Lo = 3
```

**Step 2:**
```
mid = 3 + (5-3)//2 = 4
A[4] = 8 == 8 ✅ → sec_occ = 4, Lo = mid+1 = 5  (search right!)

Saved:     sec_occ = 4
Remaining: [  ✗,    ✗,    ✗,    ✗,    ✗,   10  ]
                                              Lo Ro
```

**Step 3:**
```
mid = 5 + (5-5)//2 = 5
A[5] = 10 > 8 → Ro = mid-1 = 4
```

**Lo=5 > Ro=4 → loop ends → sec_occ = 4** ✅

**Return: [3, 4]** ✅

---

## 📊 Full Dry Run — Example 2: `A=[5,17,100,111]`, B=3 (Not Found)

### Search 1: First Occurrence

| Step | L | R  | `mid` | `A[mid]` | Comparison | Action    |
|:----:|:-:|:--:|:-----:|:--------:|:----------:|:----------|
| 1    | 0 | 3  | 1     | 17       | 17 > 3     | R = 0     |
| 2    | 0 | 0  | 0     | 5        | 5 > 3      | R = -1    |

L=0 > R=-1 → **first_occ = -1** (never updated)

> Both steps hit the `else` branch (too large) — B=3 is smaller than everything.
> `first_occ` was never set → stays at -1. Same result for `sec_occ`.

**Return: [-1, -1]** ✅

---

## 📊 Dry Run — All Same: `A=[1,1,1,1,1]`, B=1

### Search 1: First Occurrence

```
Array:   [1,  1,  1,  1,  1]   idx: 0 1 2 3 4

Step 1: L=0, R=4, mid=2, A[2]=1 == 1 ✅ → first_occ=2, R=1
Step 2: L=0, R=1, mid=0, A[0]=1 == 1 ✅ → first_occ=0, R=-1

L=0 > R=-1 → first_occ = 0  ✅ (leftmost)
```

### Search 2: Last Occurrence

```
Step 1: Lo=0, Ro=4, mid=2, A[2]=1 == 1 ✅ → sec_occ=2, Lo=3
Step 2: Lo=3, Ro=4, mid=3, A[3]=1 == 1 ✅ → sec_occ=3, Lo=4
Step 3: Lo=4, Ro=4, mid=4, A[4]=1 == 1 ✅ → sec_occ=4, Lo=5

Lo=5 > Ro=4 → sec_occ = 4  ✅ (rightmost)
```

**Return: [0, 4]** ✅

---

## 🎨 Visual — The Two Searches Side by Side

```
A = [5,  7,  7,  8,  8,  10],  B=8
idx:  0   1   2   3   4    5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEARCH 1: First Occurrence (bias LEFT on match)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: mid=2 (=7) < 8 → move L right
  [✗, ✗, ✗,  8,  8, 10]
              L          R

Step 2: mid=4 (=8) MATCH → save 4, shrink RIGHT (R=3)
  [✗, ✗, ✗, [8], ✗,  ✗]
              L  R
         ← searching leftward for earlier 8

Step 3: mid=3 (=8) MATCH → save 3, shrink RIGHT (R=2)
  [✗, ✗, ✗, [8], ✗,  ✗]
           R  L       ← L > R, stop

first_occ = 3  ✅


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEARCH 2: Last Occurrence (bias RIGHT on match)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: mid=2 (=7) < 8 → move Lo right
  [✗, ✗, ✗,  8,  8, 10]
              Lo         Ro

Step 2: mid=4 (=8) MATCH → save 4, grow LEFT (Lo=5)
  [✗, ✗, ✗,  ✗, [8], ✗]
                      Lo Ro
         searching rightward for later 8 →

Step 3: mid=5 (=10) > 8 → move Ro left (Ro=4)
  [✗, ✗, ✗,  ✗,  ✗,  ✗]
                   Ro  Lo ← Lo > Ro, stop

sec_occ = 4  ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Answer: [3, 4]
```

---

## 🔑 The Three-Branch Decision Table

Both searches share the same logic for `<` and `>`. Only `==` differs:

| Condition     | First Occurrence          | Last Occurrence           |
|:------------- |:--------------------------|:--------------------------|
| `A[mid] == B` | save `mid`, go **left** (`R=mid-1`) | save `mid`, go **right** (`Lo=mid+1`) |
| `A[mid] < B`  | go right (`L=mid+1`)      | go right (`Lo=mid+1`)     |
| `A[mid] > B`  | go left (`R=mid-1`)       | go left (`Ro=mid-1`)      |

---

## ⏱️ Complexity Analysis

| Aspect  | Value          | Reason                                         |
|:--------|:--------------:|:-----------------------------------------------|
| Time    | **O(log N)**   | Two independent binary searches, each O(log N) |
| Space   | **O(1)**       | Six variables total: L, R, Lo, Ro, first_occ, sec_occ |

```
N = 10⁶

Linear scan: up to 10⁶ steps  ❌
Two binary searches: 2 × log₂(10⁶) ≈ 2 × 20 = 40 steps  ✅

25,000× faster!
```

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: Stopping Early When a Match Is Found

The most common mistake — treating this like a standard binary search:

```python
# ❌ WRONG — standard binary search stops at first match
if A[mid] == B:
    return mid   # gives some occurrence, not necessarily first or last!
```

```python
# ✅ CORRECT for first occurrence — save and go LEFT
if A[mid] == B:
    first_occ = mid
    R = mid - 1    # ← don't stop! look for earlier

# ✅ CORRECT for last occurrence — save and go RIGHT
if A[mid] == B:
    sec_occ = mid
    Lo = mid + 1   # ← don't stop! look for later
```

For `A=[7,8,8,8,10], B=8`: a standard search might return index 2 (middle 8), but correct answers are first=1, last=3.

---

### ❗ Pitfall 2: Swapping the Direction in One of the Searches

```python
# ❌ WRONG first occurrence (goes RIGHT — finds last instead!)
if A[mid] == B:
    first_occ = mid
    L = mid + 1   # ← this searches right, finding the LAST occurrence!

# ❌ WRONG last occurrence (goes LEFT — finds first instead!)
if A[mid] == B:
    sec_occ = mid
    R = mid - 1   # ← this searches left, finding the FIRST occurrence!
```

Memory trick:
- **First** → `R = mid - 1` (R moves **left**)
- **Last** → `Lo = mid + 1` (Lo moves **right**)

---

### ❗ Pitfall 3: Reusing `L` and `R` Without Resetting

```python
# ❌ WRONG — second search inherits exhausted L and R from first search!
while L <= R:      # first search
    ...
# L and R are now in invalid state (L > R)

while L <= R:      # second search — loop never runs!
    ...
```

```python
# ✅ CORRECT — use fresh variables (Lo, Ro) for the second search
Lo = 0
Ro = N - 1
```

---

### ❗ Pitfall 4: Initialising `first_occ = 0` Instead of `-1`

```python
first_occ = 0   # ❌ WRONG — index 0 is a valid answer!
                #            Can't distinguish "found at 0" from "not found"

first_occ = -1  # ✅ CORRECT — -1 is never a valid array index
```

---

### ❗ Pitfall 5: Returning `[first_occ, first_occ]` When Not Found

If both searches find nothing, both return -1 independently → `[-1, -1]`.
No special case needed. The initialisation `first_occ = sec_occ = -1` handles it automatically.

---

## 🧪 Test It Yourself

```python
def searchRange(A, B):
    N = len(A)

    # Search 1: First occurrence
    L, R, first_occ = 0, N-1, -1
    while L <= R:
        mid = L + (R - L) // 2
        if A[mid] == B:
            first_occ = mid
            R = mid - 1        # go LEFT for earlier match
        elif A[mid] < B:
            L = mid + 1
        else:
            R = mid - 1

    # Search 2: Last occurrence
    Lo, Ro, sec_occ = 0, N-1, -1
    while Lo <= Ro:
        mid = Lo + (Ro - Lo) // 2
        if A[mid] == B:
            sec_occ = mid
            Lo = mid + 1       # go RIGHT for later match
        elif A[mid] < B:
            Lo = mid + 1
        else:
            Ro = mid - 1

    return [first_occ, sec_occ]


tests = [
    ([5,7,7,8,8,10], 8,  [3,4]),   # standard case
    ([5,17,100,111], 3,  [-1,-1]), # not found
    ([1,1,1,1,1],    1,  [0,4]),   # all same
    ([1,2,3,4,5],    3,  [2,2]),   # single occurrence
    ([8,8,8,8],      8,  [0,3]),   # all target
    ([1,2,3,4,5],    6,  [-1,-1]), # greater than all
    ([1],            1,  [0,0]),   # single element, match
    ([1],            2,  [-1,-1]), # single element, no match
    ([1,1],          1,  [0,1]),   # two elements, both match
    ([1,3],          2,  [-1,-1]), # between two elements
]

for A, B, expected in tests:
    result = searchRange(A, B)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  A={A}  B={B}  → {result}")
```

---

## 🗺️ Complete Visual Summary

```
ALGORITHM:
  Run two binary searches on the SAME sorted array.
  Both use standard binary search logic for < and >.
  The ONLY difference is what happens on a MATCH:

  ┌─────────────────────┬──────────────────────────────────────────┐
  │  FIRST OCCURRENCE   │  LAST OCCURRENCE                         │
  │  (go LEFT on match) │  (go RIGHT on match)                     │
  ├─────────────────────┼──────────────────────────────────────────┤
  │  first_occ = mid    │  sec_occ = mid                           │
  │  R = mid - 1   ←←   │  Lo = mid + 1   →→                      │
  └─────────────────────┴──────────────────────────────────────────┘

  KEY:  Save the answer, then keep searching in the opposite direction
        to see if an even better (earlier/later) match exists.

EXAMPLE SUMMARY:
  A = [5, 7, 7, 8, 8, 10]   B = 8

  First search finds:  8 at idx 4 → keeps going LEFT → finds 8 at idx 3 → stops
  Second search finds: 8 at idx 4 → keeps going RIGHT → finds 10 (>8) → stops

  first_occ = 3   sec_occ = 4   →   return [3, 4] ✅
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Sorted Insert Position** | Binary search returning the insert index — same structure |
| **Count of Element in Sorted Array** | `last_occ - first_occ + 1` using this exact solution |
| **Lower Bound / Upper Bound (C++ STL)** | `lower_bound()` = first occurrence; `upper_bound()-1` = last |
| **Search in Rotated Array** | Binary search where the sorted property is broken once |
| **Peak Element** | Binary search on a non-monotone condition |
| **Kth Smallest in Sorted Matrix** | Binary search on answer combined with count |

---

> ✍️ **The Big Idea:**
> When binary search finds a match, it usually stops. But for range queries
> (first and last position), you can't stop — you need to keep going in a
> specific direction to find the **boundary** of the match zone.
> The key is to **save the match** and **continue searching** in the target direction.
> Two searches, opposite biases, same O(log N) cost each.
> The `== -1` initialisation elegantly handles the "not found" case —
> no special checks needed at the end.

---

*Happy Coding! 🚀*
