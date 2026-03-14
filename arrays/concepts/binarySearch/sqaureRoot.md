# 🔍 Square Root of an Integer — Binary Search

> **Difficulty:** Beginner → Intermediate
> **Topic:** Binary Search · Integer Math · Search Space Reduction
> **Language:** Python
> **Constraint:** 0 ≤ A ≤ 10⁹ · Must not use `sqrt()` · Must run in **O(log A)**

---

## 📋 Problem Statement

Given a non-negative integer **A**, return **floor(√A)** — the largest integer whose square does **not exceed** A.

```
floor(√11) = 3   because  3² = 9 ≤ 11  and  4² = 16 > 11
floor(√9)  = 3   because  3² = 9 = 9   (perfect square)
floor(√2)  = 1   because  1² = 1 ≤ 2   and  2² = 4 > 2
```

**The rules:**
- Do **not** use `math.sqrt()` or any built-in square root
- Must run in **O(log A)** — not O(√A) with a linear scan
- `mid * mid` can overflow a 32-bit integer — handle carefully

---

## 🌍 Real-World Analogy — Before Any Code

### 📚 Guessing a Page in a Book

Imagine a book with **1000 pages** (= our search space of 1 to A).
You want to find the last page whose page² ≤ 1000.

**Strategy 1 (Brute force):** Check page 1, page 2, page 3… all the way up. Could take 31 checks.

**Strategy 2 (Binary Search):** Open to the **middle page** (500). Is 500² ≤ 1000? No (250,000 > 1000). So the answer is somewhere in the **first half**. Open to the **middle of that half** (250). Still too big. Keep halving.

Each check **eliminates half** the remaining options. 10 checks cover 1024 possibilities. This is **O(log N)** — the binary search approach.

That's exactly what this algorithm does. Instead of trying 1, 2, 3, … √A (slow), it jumps straight to the middle and slices the search space in half each time.

---

## 🧩 Understanding the Examples

### Example 1: `A = 11`

```
Checking squares:
  1² =  1  ≤ 11 ✅
  2² =  4  ≤ 11 ✅
  3² =  9  ≤ 11 ✅  ← last one that fits
  4² = 16  > 11 ❌

floor(√11) = 3
```

### Example 2: `A = 9`

```
  1² =  1  ≤ 9 ✅
  2² =  4  ≤ 9 ✅
  3² =  9  = 9 ✅  ← perfect square, exactly fits
  4² = 16  > 9 ❌

floor(√9) = 3
```

---

## 💡 Why Binary Search?

### What are we actually searching for?

We want the **largest integer `x`** such that `x² ≤ A`.

Think of all integers from 1 to A, labelled with whether their square fits:

```
For A = 11:

x:    1   2   3   4   5   6   7   8   9   10  11
x²:   1   4   9  16  25  36  49  64  81  100 121
fit?  ✅  ✅  ✅  ❌  ❌  ❌  ❌  ❌  ❌   ❌   ❌
      └────────────────┘└─────────────────────────┘
         TRUE zone           FALSE zone
```

The pattern is always: **a block of ✅s followed by a block of ❌s.** It never alternates. This is the golden property that makes binary search applicable:

> **Binary search works whenever the search space is monotone** — once the condition becomes False, it never becomes True again.

The algorithm searches for the **rightmost ✅** — the last `x` where `x² ≤ A`.

---

## 🔍 The Code — Every Line Explained

```python
def sqrt(self, A):
    L = 1
    R = A
    ans = L
    if A == 0:
        return A
    while L <= R:
        mid = L + (R - L) // 2
        if mid * mid <= A:
            ans = mid
            L = mid + 1
        else:
            R = mid - 1
    return ans
```

---

### Line 1-2: Set the Search Boundaries

```python
L = 1
R = A
```

> **L** = the smallest possible answer (√A ≥ 1 for A ≥ 1)
> **R** = the largest possible answer (√A ≤ A always, since 1²=1 ≤ A for A ≥ 1)
>
> We search for the answer **somewhere in the range [1, A]**.
>
> 💡 A tighter upper bound could be `R = A // 2 + 1` for large A, since
> √A ≤ A/2 when A ≥ 4. But `R = A` is always correct and simpler.

---

### Line 3: Initialise the Answer

```python
ans = L    # starts at 1
```

> `ans` stores the **best valid answer found so far** during the search.
> It's initialised to 1 because for any A ≥ 1, floor(√A) ≥ 1.
>
> Every time we find a `mid` where `mid² ≤ A`, we **update `ans`** because
> that `mid` is a valid floor candidate — and we record it before searching further.

---

### Line 4-5: Handle Zero Separately

```python
if A == 0:
    return A
```

> `√0 = 0`. Without this guard:
> - `L=1, R=0` → the while loop never starts (`L > R`)
> - `ans = L = 1` would be returned → **wrong!**
>
> So we short-circuit: if A is 0, immediately return 0.

---

### Line 6: The Loop Condition

```python
while L <= R:
```

> The loop runs as long as there's at least one candidate to check.
> `L > R` means the search space is exhausted — every candidate has been
> either confirmed or ruled out. At that point, `ans` holds the best valid answer.

---

### Line 7: Compute the Midpoint (Overflow-Safe)

```python
mid = L + (R - L) // 2
```

> This finds the **middle** of the current search range without overflow.
>
> **Naive version:**
> ```python
> mid = (L + R) // 2   # ❌ potential overflow in C++/Java
> ```
> If `L = 5×10⁸` and `R = 10⁹`, then `L + R = 1.5×10⁹` — fine in Python
> (arbitrary precision), but overflows a 32-bit integer in C++/Java (max ≈ 2.1×10⁹).
>
> **Safe version:**
> ```python
> mid = L + (R - L) // 2  # ✅ (R-L) is at most 10^9, never overflows
> ```
>
> Mathematically: `L + (R-L)/2 = L/2 + R/2 = (L+R)/2` — same result, safer arithmetic.

---

### Lines 8-10: The Core Decision

```python
if mid * mid <= A:
    ans = mid
    L = mid + 1
```

> **Condition:** Is `mid` a valid floor candidate? Is `mid² ≤ A`?
>
> **If YES (mid² ≤ A):**
> - `mid` is a valid answer (not too big)
> - **Save it:** `ans = mid` — this might be the final answer
> - **Search right:** `L = mid + 1` — try to find something **bigger** (we want the largest valid x)
>
> The key insight: when `mid² ≤ A`, we don't stop. We record `mid` as the current best
> and push the left boundary past it to look for an even better (larger) answer.

---

### Lines 11-12: Eliminate Too-Large Half

```python
else:
    R = mid - 1
```

> **If NO (mid² > A):**
> - `mid` is too large — its square exceeds A, so it can't be floor(√A)
> - Anything **≥ mid** is also too large (since squares grow with x)
> - **Search left:** `R = mid - 1` — discard `mid` and everything to its right

---

### Line 13: Return the Best Valid Answer

```python
return ans
```

> When `L > R`, the search space is empty — no more candidates.
> `ans` holds the last `mid` for which `mid² ≤ A` — the **rightmost valid point**,
> which is exactly `floor(√A)`.

---

## 📊 Full Dry Run — `sqrt(11)`

**Initial:** L=1, R=11, ans=1

```
Search space visualised:
  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
   L                               R
```

---

**Step 1:**
```
  mid = 1 + (11-1)//2 = 1 + 5 = 6
  mid² = 6×6 = 36
  36 ≤ 11? ❌ NO → mid is too big
  R = mid-1 = 5

  Eliminated:  [·  ·  ·  ·  ·  ✗  ✗  ✗  ✗   ✗   ✗]
                                ↑  ← all ≥ 6 ruled out
  Remaining:   [1, 2, 3, 4, 5]
                L           R
```

---

**Step 2:**
```
  mid = 1 + (5-1)//2 = 1 + 2 = 3
  mid² = 3×3 = 9
  9 ≤ 11? ✅ YES → valid candidate!
  ans = 3
  L = mid+1 = 4

  Found:       ans = 3 (saved!)
  Eliminated:  [✗  ✗  ✗  ·  ·  ✗  ✗  ✗  ✗   ✗   ✗]
                         ↑ ← all ≤ 3 also ruled out (already accounted for)
  Remaining:   [4, 5]
                L   R
```

---

**Step 3:**
```
  mid = 4 + (5-4)//2 = 4 + 0 = 4
  mid² = 4×4 = 16
  16 ≤ 11? ❌ NO → mid is too big
  R = mid-1 = 3

  Eliminated:  [·  ·  ·  ✗  ✗  ✗  ✗  ✗  ✗   ✗   ✗]
  Remaining:   none — L=4, R=3 → L > R → STOP
```

**Return ans = 3** ✅

---

## 📊 Full Dry Run — `sqrt(9)` (Perfect Square)

**Initial:** L=1, R=9, ans=1

| Step | L | R | `mid` | `mid²` | `≤ 9?` | Action            | `ans` |
|:----:|:-:|:-:|:-----:|:------:|:------:|:------------------|:-----:|
| 1    | 1 | 9 | 5     | 25     | ❌     | R = 4             | 1     |
| 2    | 1 | 4 | 2     | 4      | ✅     | ans=2, L=3        | 2     |
| 3    | 3 | 4 | 3     | 9      | ✅     | ans=3, L=4        | **3** |
| 4    | 4 | 4 | 4     | 16     | ❌     | R=3               | 3     |

L=4 > R=3 → **Return 3** ✅

> Notice at Step 3: `mid²= 9 = A` exactly. The condition is `≤` not `<`,
> so a perfect square **is accepted** as a valid candidate and saved as `ans`.

---

## 📊 Full Dry Run — `sqrt(2)` (Small, No Perfect Square)

**Initial:** L=1, R=2, ans=1

| Step | L | R | `mid` | `mid²` | `≤ 2?` | Action     | `ans` |
|:----:|:-:|:-:|:-----:|:------:|:------:|:-----------|:-----:|
| 1    | 1 | 2 | 1     | 1      | ✅     | ans=1, L=2 | **1** |
| 2    | 2 | 2 | 2     | 4      | ❌     | R=1        | 1     |

L=2 > R=1 → **Return 1** ✅

---

## 🗺️ The Search in Action — Visualised

```
Searching for floor(√11) in range [1..11]:

  Numbers:  1   2   3   4   5   6   7   8   9  10  11
  x²:       1   4   9  16  25  36  49  64  81 100 121
  Valid?:   ✅  ✅  ✅  ❌  ❌  ❌  ❌  ❌  ❌  ❌  ❌
            └───────────┘└─────────────────────────────┘
               KEEP zone           DISCARD zone

We want: the RIGHTMOST ✅

STEP 1: Check middle = 6.   6²=36 > 11 ❌  →  discard 6..11
  [✅  ✅  ✅  ❌  ❌  ✗   ✗   ✗   ✗   ✗   ✗]

STEP 2: Check middle = 3.   3²= 9 ≤ 11 ✅  →  save ans=3, try right of 3
  [✗   ✗   ✅  ❌  ❌  ✗   ✗   ✗   ✗   ✗   ✗]
               ↑ saved

STEP 3: Check middle = 4.   4²=16 > 11 ❌  →  discard 4..5
  [✗   ✗   ✅  ✗   ✗   ✗   ✗   ✗   ✗   ✗   ✗]

Search space empty. ans = 3. ✅
```

---

## ⚙️ Why `mid * mid <= A` and Not `mid <= sqrt(A)`?

```python
# ❌ FORBIDDEN — uses sqrt() which we're told not to use
if mid <= math.sqrt(A):

# ❌ FLOATING POINT BUG — sqrt(9.0) might return 2.9999... due to FP errors
if mid <= A ** 0.5:

# ✅ CORRECT — pure integer arithmetic, no floating point, no library
if mid * mid <= A:
```

Integer multiplication is exact. Floating-point square roots introduce rounding
errors that can cause off-by-one mistakes on perfect squares.

---

## ⚠️ The Overflow Warning — Why It Matters

The problem says: *"The value of A×A can cross the range of Integer."*

```
A     = 10⁹   (max input)
√A    ≈ 31,623
mid   could be up to 10⁹ (at the start, R = A)
mid²  could be up to (10⁹)² = 10¹⁸
```

| Language | Int Size   | Max Value    | Overflow? |
|:---------|:----------:|:------------:|:---------:|
| Python   | Unlimited  | ∞            | ✅ Never  |
| C++/Java | `int` = 32-bit | ~2.1 × 10⁹ | ❌ YES!  |
| C++/Java | `long long` = 64-bit | ~9.2 × 10¹⁸ | ✅ Safe |

**In C++/Java**, `mid * mid` must be cast to `long long`:
```cpp
if ((long long)mid * mid <= A)   // C++
```

**In Python**, integers grow automatically — no overflow ever.

---

## ⏱️ Complexity Analysis

| Aspect      | Value           | Reason                                    |
|:------------|:---------------:|:------------------------------------------|
| Time        | **O(log A)**    | Search space halves every iteration       |
| Space       | **O(1)**        | Only 4 variables: L, R, mid, ans          |

### How many steps does it take?

```
A = 10⁹

Linear scan (O(√A)):  √(10⁹) ≈ 31,623 steps   ← slow
Binary search (O(log A)): log₂(10⁹) ≈ 30 steps ← instant

30 steps vs 31,623 steps — 1000× faster!
```

Each iteration: L and R get closer by at least 1 (since `mid` is discarded in both branches).
The gap `R - L` halves (approximately) each step → at most ⌈log₂(A)⌉ steps.

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: Using `<` Instead of `<=` in the Condition

```python
if mid * mid < A:   # ❌ WRONG for perfect squares
    ans = mid
    L = mid + 1
```

For `A = 9`, when `mid = 3`:  `3*3 = 9`. With `< A`: `9 < 9` is False → `R = 2` → `ans` never gets 3 → returns 2 instead of 3. ❌

```python
if mid * mid <= A:  # ✅ CORRECT — includes perfect squares
```

---

### ❗ Pitfall 2: Returning `mid` Instead of `ans`

```python
# ❌ WRONG — mid's final value is meaningless at loop end
while L <= R:
    mid = L + (R-L)//2
    if mid*mid <= A:
        L = mid + 1
    else:
        R = mid - 1
return mid   # ← mid is whatever it was on the LAST iteration, could be wrong
```

After the loop, `L > R`. The final `mid` value is the last one tested — which could have failed the condition. `ans` is explicitly updated **only when the condition passes**, making it the correct answer.

```python
# ✅ CORRECT — ans tracks the last successful mid
if mid * mid <= A:
    ans = mid     # ← save it here
    L = mid + 1
...
return ans
```

---

### ❗ Pitfall 3: Forgetting the `A == 0` Edge Case

```python
L = 1
R = A = 0    # R = 0
ans = L = 1  # ans = 1

while L <= R:   # 1 <= 0? False → loop never runs
    ...
return ans      # returns 1 ← WRONG! sqrt(0) should be 0
```

The zero guard prevents this:

```python
if A == 0:
    return A    # return 0 immediately ✅
```

---

### ❗ Pitfall 4: Setting `L = 0` Instead of `L = 1`

```python
L = 0   # ❌ causes mid=0 on first iteration for small A
        #    0*0=0 ≤ A → ans=0, L=1 (correct answer missed if 0 is recorded)
```

Since `√A ≥ 1` for all `A ≥ 1`, starting `L = 1` is both safe and correct.
With `L = 0`, the algorithm still works in Python but performs an unnecessary extra check.

---

## 🧪 Test It Yourself

```python
def sqrt(A):
    if A == 0:
        return 0
    L, R, ans = 1, A, 1
    while L <= R:
        mid = L + (R - L) // 2
        if mid * mid <= A:
            ans = mid
            L = mid + 1
        else:
            R = mid - 1
    return ans


import math

tests = [0, 1, 2, 3, 4, 8, 9, 10, 11, 15, 16, 24, 25, 99, 100, 10**9]

for A in tests:
    result   = sqrt(A)
    expected = int(math.isqrt(A))   # Python's built-in (for verification only)
    status   = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  floor(√{A}) = {result}")
```

---

## 🆚 Binary Search vs Linear Scan

```python
# ❌ Linear scan — O(√A) time
def sqrt_linear(A):
    x = 0
    while (x + 1) * (x + 1) <= A:
        x += 1
    return x

# ✅ Binary search — O(log A) time (this solution)
def sqrt_binary(A):
    if A == 0: return 0
    L, R, ans = 1, A, 1
    while L <= R:
        mid = L + (R-L)//2
        if mid*mid <= A:
            ans = mid; L = mid+1
        else:
            R = mid-1
    return ans
```

| A      | Linear steps | Binary steps |
|:------:|:------------:|:------------:|
| 100    | 10           | 7            |
| 10,000 | 100          | 14           |
| 10⁶    | 1,000        | 20           |
| 10⁹    | 31,623       | 30           |

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Binary Search on Answer** | Same pattern: search for the largest x satisfying f(x) ≤ target |
| **First Bad Version** | Binary search for leftmost False (mirror of this problem) |
| **Search in Rotated Array** | Binary search on non-trivially monotone spaces |
| **Koko Eating Bananas** | Binary search on answer with a custom check function |
| **Newton's Method** | Mathematical O(log log A) approach to √A (faster but complex) |
| **Integer Exponentiation** | Fast power: x^n in O(log n) using the same halving idea |

---

> ✍️ **The Big Idea:**
> Binary search isn't just for finding an element in a sorted array.
> Whenever your answer lies on a **monotone number line** — where values below
> a threshold are all valid and above are all invalid — binary search finds
> the exact boundary in O(log N) steps.
> Here, the question is: *"Is x too big to be √A?"* — answered by `x² > A`.
> The boundary between "valid" (x² ≤ A) and "invalid" (x² > A) is exactly floor(√A).
> We search for the **rightmost valid point** by saving `ans = mid` every time
> the condition passes, and pushing `L = mid+1` to keep hunting for something larger.

---

*Happy Coding! 🚀*
