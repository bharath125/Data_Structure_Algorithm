# 🔍 Smallest Subarray Containing Min & Max

> **Difficulty:** Beginner → Intermediate
> **Topic:** Arrays · Single Pass · Two-Pointer Tracking · Greedy
> **Language:** Python
> **Constraints:** 1 ≤ |A| ≤ 2000

---

## 📋 Problem Statement

Given an array **A**, find the **size of the smallest subarray** that contains at least:
- **One occurrence** of the **maximum** value of the array, AND
- **One occurrence** of the **minimum** value of the array

```
Smallest subarray size = min over all valid windows of (right_index - left_index + 1)
```

---

## 🌍 Real-World Analogy — Before Any Code

### 🌡️ Weather Records

Imagine a city's daily temperature log for a month:

```
Day:   0    1    2    3    4    5    6
Temp: [18,  32,  25,  32,   7,  15,   7]
       ─    MAX  ─    MAX  MIN   ─   MIN
```

A climate researcher asks:
> *"What is the shortest consecutive sequence of days that includes both the hottest day (MAX) AND the coldest day (MIN)?"*

They don't need the full month — just the **tightest window** that captures both extremes.

That's exactly this problem. The answer is the **shortest span** (fewest consecutive elements) that contains at least one MAX and at least one MIN.

---

## 🧩 Understanding the Examples

### Example 1: `A = [1, 3, 2]`

```
Index:   0    1    2
Value: [ 1,   3,   2 ]
        MIN  MAX
```

- **min = 1** at index 0
- **max = 3** at index 1

Possible subarrays containing both:
```
A[0..1] = [1, 3] → size 2  ✅ (contains min=1 and max=3)
A[0..2] = [1, 3, 2] → size 3  ✅ (also valid but larger)
```

**Smallest = 2** ✅

---

### Example 2: `A = [2, 6, 1, 6, 9]`

```
Index:   0    1    2    3    4
Value: [ 2,   6,   1,   6,   9 ]
                  MIN            MAX
```

- **min = 1** only at index 2
- **max = 9** only at index 4

The only valid subarray must include both index 2 and index 4:
```
A[2..4] = [1, 6, 9] → size 3 ✅
```

There's no shorter option because min and max each appear only once.
**Smallest = 3** ✅

---

## 💡 Core Idea — Tracking the Most Recent Positions

### The Key Observation

As we scan left to right, at any point in time we keep track of:
- The index of the **most recently seen** minimum value
- The index of the **most recently seen** maximum value

When **both have been seen**, the subarray between those two most-recent positions is a valid candidate. We record it and keep scanning.

Why "most recent"? Because as we move right, the newer positions are always **closer to each other**, so they produce **smaller** subarrays than older positions.

```
Imagine min at index 2, max at index 7, size=6
Later: new min at index 5, max still at 7, size=3  ← BETTER
Later: new max at index 8, min at 5, size=4
Later: new min at index 6, max at 8, size=3  ← TIED
```

Every time either min or max index updates, we might find a smaller window.

---

## 🔍 The Code — Every Line Explained

```python
low  = min(A)    # Find the global minimum VALUE of the array
high = max(A)    # Find the global maximum VALUE of the array
```

> 💡 `min(A)` and `max(A)` each scan the full array — O(N) each.
> These give us the **target values** to search for, not their positions.

---

```python
min_index = -1   # Position of most recently seen minimum (-1 = not found yet)
max_index = -1   # Position of most recently seen maximum (-1 = not found yet)
ans = float('inf')  # Best (smallest) answer found so far, starts at infinity
```

> `-1` is a **sentinel value** meaning "we haven't seen this yet."
> `float('inf')` is Python's way of representing infinity — any real number is smaller.

---

```python
for i in range(len(A)):
```

> Single left-to-right scan through every element — O(N).

---

```python
    if A[i] == low:
        min_index = i        # Update: this is the newest position of min
    if A[i] == high:
        max_index = i        # Update: this is the newest position of max
```

> Two **independent** checks — an element could be both min AND max (when all elements are equal).
> Using `if` (not `elif`) ensures both checks always run.

---

```python
    if min_index != -1 and max_index != -1:
        size = abs(max_index - min_index) + 1
        ans  = min(ans, size)
```

> Only compute a window size after **both** min and max have been seen at least once.
> `abs(max_index - min_index)` = distance between positions (order doesn't matter).
> `+ 1` converts from "distance between endpoints" to "number of elements" (0-indexed fix).
> `min(ans, size)` keeps track of the best (smallest) window seen so far.

---

```python
if min_index == max_index:
    return 1
return ans
```

> **Special case:** When min == max (all elements identical, or single element), both pointers
> land on the same index. The subarray containing that one element has size 1.

---

## 📊 The `+1` Explained — Why Not Just Subtract?

This trips up many beginners. Here's the intuition:

```
Array:   [A, B, C, D, E]
Index:     0  1  2  3  4

Distance from index 1 to index 3 = 3 - 1 = 2 (gap)
Number of elements from index 1 to index 3 = 3 (B, C, D)

So: elements = distance + 1 = 2 + 1 = 3 ✅
```

Think of it like counting fence posts vs. fence gaps:

```
|  gap  |  gap  |  gap  |
●────────●────────●────────●
0        1        2        3

4 posts, 3 gaps.  posts = gaps + 1
```

Same logic: `size = (R - L) + 1` always.

---

## 📊 Full Dry Run — Example 1: `A = [1, 3, 2]`

```
low = 1,  high = 3
min_index = -1,  max_index = -1,  ans = inf
```

| `i` | `A[i]` | Min seen? | Max seen? | `min_index` | `max_index` | Both found? | `size` | `ans` |
|:---:|:------:|:---------:|:---------:|:-----------:|:-----------:|:-----------:|:------:|:-----:|
| 0   | 1      | ✅ = low  | ❌        | **0**       | -1          | ❌          | —      | inf   |
| 1   | 3      | ❌        | ✅ = high | 0           | **1**       | ✅          | \|1-0\|+1=**2** | **2** |
| 2   | 2      | ❌        | ❌        | 0           | 1           | ✅          | \|1-0\|+1=**2** | 2     |

```
min_index(0) ≠ max_index(1)  →  return ans = 2
```

**Visual:**
```
A:  [ [1,  3]  2 ]
       ↑   ↑
      MIN MAX
      i=0  i=1
   size = |1-0|+1 = 2 ✅
```

---

## 📊 Full Dry Run — Example 2: `A = [2, 6, 1, 6, 9]`

```
low = 1,  high = 9
min_index = -1,  max_index = -1,  ans = inf
```

| `i` | `A[i]` | Min? | Max? | `min_idx` | `max_idx` | Both? | `size`         | `ans` |
|:---:|:------:|:----:|:----:|:---------:|:---------:|:-----:|:---------------|:-----:|
| 0   | 2      | ❌   | ❌   | -1        | -1        | ❌    | —              | inf   |
| 1   | 6      | ❌   | ❌   | -1        | -1        | ❌    | —              | inf   |
| 2   | 1      | ✅   | ❌   | **2**     | -1        | ❌    | —              | inf   |
| 3   | 6      | ❌   | ❌   | 2         | -1        | ❌    | —              | inf   |
| 4   | 9      | ❌   | ✅   | 2         | **4**     | ✅    | \|4-2\|+1=**3** | **3** |

```
min_index(2) ≠ max_index(4)  →  return ans = 3
```

**Visual:**
```
A:  [ 2,  6, [1,  6,  9] ]
              ↑        ↑
             MIN      MAX
            i=2       i=4
   size = |4-2|+1 = 3 ✅
```

---

## 📊 Dry Run — Repeated Min/Max: `A = [1, 9, 1, 9, 1]`

This shows why updating to the **most recent** position matters.

```
low = 1,  high = 9
```

| `i` | `A[i]` | `min_idx` | `max_idx` | `size`         | `ans` | Window             |
|:---:|:------:|:---------:|:---------:|:--------------|:-----:|:-------------------|
| 0   | 1      | **0**     | -1        | —              | inf   | —                  |
| 1   | 9      | 0         | **1**     | \|1-0\|+1=**2** | **2** | A[0..1]=[1,9]      |
| 2   | 1      | **2**     | 1         | \|2-1\|+1=**2** | 2     | A[1..2]=[9,1]      |
| 3   | 9      | 2         | **3**     | \|3-2\|+1=**2** | 2     | A[2..3]=[1,9]      |
| 4   | 1      | **4**     | 3         | \|4-3\|+1=**2** | 2     | A[3..4]=[9,1]      |

> 🔑 Each time either index updates to a newer position, the two indices become
> **closer** or equal — producing a window that's smaller or the same size.
> The answer never gets worse!

**Answer = 2** ✅

---

## 📊 Dry Run — Mixed Directions: `A = [9, 1, 5, 9, 1]`

Shows that `abs()` handles both orderings (min before max, max before min).

```
low=1, high=9
```

| `i` | `A[i]` | `min_idx` | `max_idx` | `size`         | `ans` | Subarray       |
|:---:|:------:|:---------:|:---------:|:--------------|:-----:|:---------------|
| 0   | 9      | -1        | **0**     | —              | inf   | —              |
| 1   | 1      | **1**     | 0         | \|1-0\|+1=**2** | **2** | A[0..1]=[9,1]  |
| 2   | 5      | 1         | 0         | \|1-0\|+1=**2** | 2     | A[0..1]=[9,1]  |
| 3   | 9      | 1         | **3**     | \|3-1\|+1=**3** | 2     | 3 > 2 → skip   |
| 4   | 1      | **4**     | 3         | \|4-3\|+1=**2** | 2     | A[3..4]=[9,1]  |

**Answer = 2** ✅ — `abs()` correctly handles max-before-min and min-before-max.

---

## 🗺️ Complete Visual Summary

```
ALGORITHM OVERVIEW:

Step 1: Find global min and max values  (O(N) each)
Step 2: Scan left to right, always tracking the MOST RECENT position
        of min and max seen so far
Step 3: Whenever BOTH have been seen, compute window size and update best answer

KEY IDEA:
  As we scan →, updating to newer positions shrinks or maintains the window.
  Each update gives us a fresh candidate for a smaller subarray.

  OLD:  [... MIN .............. MAX ...]   ← big gap
             ↑                  ↑
  NEW:  [... MIN ...... MIN ... MAX ...]   ← min moved closer!
                        ↑       ↑
  NEWER:[... MIN ...... MIN ... MAX ... MAX ...]  ← max moved right, bigger gap again
                        ↑               ↑
  → We take the minimum over ALL such windows seen during the scan.

FORMULA:
  size = abs(max_index - min_index) + 1
         └─ distance between positions ─┘   └─ convert to element count ─┘

SPECIAL CASE:
  min == max (all elements equal, or single element)
  → min_index == max_index → size = 1
```

---

## ⚠️ Edge Cases & Pitfalls

### ❗ Edge Case 1: Single Element

```python
A = [5]
low = 5, high = 5  # min == max!

i=0: A[0]=5 → min_index=0, max_index=0 (SAME index!)
  size = |0-0|+1 = 1

min_index == max_index → return 1  ✅
```

---

### ❗ Edge Case 2: All Elements Equal

```python
A = [3, 3, 3]
low = 3, high = 3  # min == max again

Every element updates BOTH min_index and max_index to the same i.
At every step, min_index == max_index → the `return 1` guard fires.
```

> ⚠️ **Why the `return 1` guard is needed:**
> Without it, `ans` would be computed as `|2-2|+1 = 1` anyway,
> but the guard makes the intent explicit and handles the case safely.

---

### ❗ Edge Case 3: Min and Max Adjacent

```python
A = [1, 9]
low=1, high=9

i=0: min_index=0, max_index=-1 → not both found
i=1: min_index=0, max_index=1  → size = |1-0|+1 = 2
Return 2 ✅  (the smallest possible window of size 2)
```

---

### ❗ Pitfall: Using `elif` Instead of Two `if` Statements

```python
# ❌ WRONG — if min==max, only min_index gets updated!
if A[i] == low:
    min_index = i
elif A[i] == high:
    max_index = i

# ✅ CORRECT — both checks always run
if A[i] == low:
    min_index = i
if A[i] == high:
    max_index = i
```

When `low == high` (all elements equal), every element satisfies both conditions.
`elif` would skip the `high` update — causing `max_index` to never update.

---

### ❗ Pitfall: Forgetting `+1`

```python
size = abs(max_index - min_index)      # ❌ counts gaps, not elements
size = abs(max_index - min_index) + 1  # ✅ counts elements
```

For indices 0 and 1: gap = 1, but elements = 2 (both A[0] and A[1]).

---

### ❗ Pitfall: `float('inf')` as Initial `ans`

What if you initialise `ans = 0` or `ans = len(A)`?

```python
ans = 0        # ❌ — min() would always stay at 0, nothing updates correctly
ans = len(A)   # ⚠️  — technically fine (answer can't exceed array length)
               #        but float('inf') is cleaner and more conventional
ans = float('inf')  # ✅ — guarantees the first valid size always updates ans
```

---

## ⏱️ Complexity Analysis

| Operation         | Cost   | Why                                              |
|:------------------|:------:|:-------------------------------------------------|
| `min(A)`          | O(N)   | Full scan to find minimum                        |
| `max(A)`          | O(N)   | Full scan to find maximum                        |
| Main `for` loop   | O(N)   | Single left-to-right scan                        |
| Each iteration    | O(1)   | Just comparisons and arithmetic                  |
| **Total Time**    | **O(N)** | Three O(N) passes = O(3N) = O(N)              |
| **Space**         | **O(1)** | Only 4 variables: low, high, min_index, max_index |

---

## 🧪 Test It Yourself

```python
def solve(A):
    low  = min(A)
    high = max(A)
    min_index = -1
    max_index = -1
    ans = float('inf')
    for i in range(len(A)):
        if A[i] == low:
            min_index = i
        if A[i] == high:
            max_index = i
        if min_index != -1 and max_index != -1:
            size = abs(max_index - min_index) + 1
            ans  = min(ans, size)
    if min_index == max_index:
        return 1
    return ans


tests = [
    ([1, 3, 2],          2),   # min=1@0, max=3@1 → window=[1,3]
    ([2, 6, 1, 6, 9],    3),   # min=1@2, max=9@4 → window=[1,6,9]
    ([5],                1),   # single element
    ([1, 1, 1],          1),   # all same
    ([1, 9, 1, 9, 1],    2),   # alternating, always adjacent pairs
    ([9, 1, 5, 9, 1],    2),   # max before min, still finds size 2
    ([1, 2, 3, 4, 5],    5),   # min at start, max at end, full array
    ([5, 4, 3, 2, 1],    5),   # max at start, min at end, full array
    ([3, 1, 4, 1, 5, 9], 2),   # 1 at idx1, 9 at idx5 → best is A[4..5]=[5,9]? No. min=1,max=9
]

for A, expected in tests:
    result = solve(A)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  A={A}  → {result}")
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Sliding Window** | Fixed/variable window problems over arrays |
| **Two Pointer Technique** | Efficient range tracking without nested loops |
| **Kadane's Algorithm** | Another single-pass greedy scan over an array |
| **Smallest Window with K distinct elements** | Extension of this window concept |
| **Segment Tree (range min/max)** | Answer min/max queries dynamically with updates |

---

> ✍️ **The Big Idea:**
> Instead of checking every possible subarray (O(N²)), make a single left-to-right pass,
> always remembering the **most recently seen** positions of both min and max.
> As you scan rightward, the two pointer positions naturally converge — each update
> either shrinks the window or gives a fresh candidate. Track the minimum window size
> seen throughout. Three O(N) passes total → **O(N) overall**.

---

*Happy Coding! 🚀*
