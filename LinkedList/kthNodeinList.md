# 🔗 Kth Node in a Linked List — Index-Based Access

> **Difficulty:** Absolute Beginner → Comfortable
> **Topic:** Linked Lists · Traversal · 0-Based Indexing · Bounds Checking
> **Language:** Python
> **Constraint:** k ≤ 10⁶

---

## 📋 Problem Statement

Given the **head** of a singly linked list and an integer **B** (the target index), return the **value** at the B-th node using **0-based indexing**.

If B is out of bounds (beyond the last node), return **-1**.

```
A = 1 → 3 → 5 → 7 → 9
         ↑ index 0
             ↑ index 1
                 ↑ index 2  ← B=2 → return 5
                     ↑ index 3
                         ↑ index 4
```

---

## 🧩 Understanding the Problem Constraints — Line by Line

### Constraint 1: `k <= 10⁶`

> **B** can be as large as one million. This is the index we want to access.
>
> This constraint tells us:
> - We might need to walk up to 10⁶ steps through the list
> - The list itself could have any number of nodes — the problem doesn't explicitly bound it
> - If the list is shorter than B+1 nodes, we must detect that and return -1 safely
>
> ```
> B = 1,000,000  and  list has 5 nodes
> → B is way beyond the list → return -1
> ```

---

### Constraint 2: "0-based indexing"

> Index 0 = the **first** node (the head itself).
> Index 1 = the **second** node.
> Index B = the **(B+1)th** node.
>
> ```
> List:   [1,  3,  5,  7,  9]
> Index:   0   1   2   3   4
>
> B=0 → return 1  (the head)
> B=2 → return 5  (3rd element)
> B=4 → return 9  (last element)
> B=5 → return -1 (doesn't exist)
> ```
>
> 0-based indexing is standard in Python arrays (`arr[0]` = first element).
> The same idea applies here — index 0 is the head.

---

### Constraint 3: "Return -1 if out of bounds"

> If B ≥ length of the list, the node doesn't exist.
> Instead of crashing, we must **gracefully return -1** as a signal that the index is invalid.
>
> ```
> List has N nodes → valid indices are 0 to N-1
> B = N or larger → out of bounds → return -1
> ```

---

## 🌍 Real-World Analogy — Before Any Code

### 🚂 Train Car Numbering

A train has carriages numbered from 0. Each carriage has a door connecting to the next one:

```
[Car 0: val=1]  →  [Car 1: val=3]  →  [Car 2: val=5]  →  [Car 3: val=7]  →  [Car 4: val=9]  → 🚫
```

You board at Car 0 (the head). To reach Car 2 (B=2), you walk through **2 doors**:
```
Car 0 →(door 1)→ Car 1 →(door 2)→ Car 2 ✅
```

If someone asks for Car 7 but the train only has 5 cars (0–4), you reach the end and find nothing → return -1.

---

## 💡 The Core Idea — Walk B Steps from the Head

Unlike an array where `arr[B]` is instant (O(1)), a linked list has **no random access**. You must walk from the head, one node at a time, counting steps.

```
To reach index B, advance the pointer exactly B times:

  Start:   temp → node(index 0)
  Step 1:  temp → node(index 1)   ← temp = temp.next
  Step 2:  temp → node(index 2)   ← temp = temp.next
  ...
  Step B:  temp → node(index B)   ← temp = temp.next
  Done:    return temp.val
```

If at any point `temp` becomes `None` (we've gone past the last node), the index is out of bounds.

---

## 🔍 The Code — Every Line Explained

```python
def solve(self, A, B):
    temp = A
    for i in range(0, B):
        if temp != None:
            temp = temp.next
    if temp == None:
        return -1
    else:
        return temp.val
```

---

### `temp = A`

```python
temp = A
```

> `A` is the head node. We never move `A` directly — it's our permanent entry point.
> `temp` is a **traveller pointer** that starts at the head and walks forward.
>
> ```
> Before loop:  temp → node(1) → node(3) → node(5) → ...
>               A    → node(1)                           ← A stays fixed
> ```
>
> This is the universal linked list traversal pattern. Always create a separate pointer
> (`temp`, `current`, `node`, etc.) to walk the list — never move the head pointer itself.

---

### `for i in range(0, B):`

```python
for i in range(0, B):
```

> Runs **exactly B times** — once for each step we need to advance.
>
> `range(0, B)` generates `[0, 1, 2, ..., B-1]` — that's B values → B iterations.
>
> **Why B iterations for index B?**
>
> ```
> Index 0: we're already there  → 0 advances needed
> Index 1: 1 advance from head  → 1 iteration
> Index 2: 2 advances from head → 2 iterations
> Index B: B advances from head → B iterations
> ```
>
> Special case: when `B = 0`, `range(0, 0)` is empty → loop body never runs.
> `temp` stays at the head, and we return `A.val` directly. ✅

---

### `if temp != None:`

```python
    if temp != None:
        temp = temp.next
```

> **The safety guard.** Before advancing `temp`, we verify it's not `None`.
>
> **Why is this necessary?** If `B` is larger than the list length, `temp` will reach `None`
> before the loop finishes. Without this guard, `temp.next` on a `None` object would crash:
>
> ```python
> temp = None
> temp = temp.next   # ❌ AttributeError: 'NoneType' object has no attribute 'next'
> ```
>
> With the guard:
> ```python
> if temp != None:     # False when temp is None
>     temp = temp.next # ← skipped! temp stays None safely
> ```
>
> The loop continues running (the `for` loop can't be stopped mid-run without `break`),
> but the body safely does nothing when `temp` is already `None`.
>
> After the loop, `temp == None` signals out-of-bounds.

---

### `if temp == None: return -1`

```python
if temp == None:
    return -1
```

> After all B iterations, if `temp` is `None`, it means we walked off the end of the list.
> The index B is out of bounds → return the sentinel value **-1**.
>
> Two ways `temp` can be `None` here:
> 1. B equals the list length exactly (walked to one past the last node)
> 2. B is greater than the list length (multiple steps past the end)
>
> Both cases are handled identically: `temp` is `None`, return `-1`.

---

### `else: return temp.val`

```python
else:
    return temp.val
```

> `temp` is not `None`, meaning after B advances we're sitting on a valid node.
> `.val` reads the integer value stored in that node.
>
> This is the answer — the value at index B.

---

## 📊 Full Dry Run — `A=[1,3,5,7,9]`, B=2

**Memory structure:**
```
A: [1]→[3]→[5]→[7]→[9]→None
    0   1   2   3   4    (indices)
```

**Initial state:** `temp → node(1)` ← (index 0)

```
Goal: walk 2 steps to reach index 2
```

| Iteration | `i` | `temp != None?` | Action            | `temp` after     |
|:---------:|:---:|:---------------:|:------------------|:-----------------|
| —         | —   | —               | start: temp=node(1) | node(1) [idx 0] |
| 1         | 0   | ✅ True          | `temp = temp.next`| node(3) [idx 1] |
| 2         | 1   | ✅ True          | `temp = temp.next`| node(5) [idx 2] |

Loop ends (range(0,2) exhausted after i=0,1)

```
temp = node(5)
temp == None? NO
return temp.val = 5 ✅
```

---

## 📊 Dry Run — B=0 (Return Head Value)

**`range(0, 0)` generates an empty sequence → loop body never runs!**

```
temp → node(1)   ← unchanged after loop

temp == None? NO
return temp.val = 1 ✅
```

> Index 0 = the head. Zero advances needed. The loop is a no-op.

---

## 📊 Dry Run — B=4 (Last Node)

| `i` | `temp` before | Action              | `temp` after |
|:---:|:-------------:|:--------------------|:-------------|
| 0   | node(1)       | temp = temp.next    | node(3)      |
| 1   | node(3)       | temp = temp.next    | node(5)      |
| 2   | node(5)       | temp = temp.next    | node(7)      |
| 3   | node(7)       | temp = temp.next    | node(9)      |

```
temp = node(9)
temp == None? NO
return temp.val = 9 ✅
```

---

## 📊 Dry Run — B=5 (Out of Bounds)

List has 5 nodes (indices 0–4). B=5 is one past the end.

| `i` | `temp` before | `temp != None?` | Action              | `temp` after |
|:---:|:-------------:|:---------------:|:--------------------|:-------------|
| 0   | node(1)       | ✅              | temp = temp.next    | node(3)      |
| 1   | node(3)       | ✅              | temp = temp.next    | node(5)      |
| 2   | node(5)       | ✅              | temp = temp.next    | node(7)      |
| 3   | node(7)       | ✅              | temp = temp.next    | node(9)      |
| 4   | node(9)       | ✅              | temp = temp.next    | **None**     |

```
Loop ends (i went from 0 to 4, that's 5 iterations for B=5)
temp = None
temp == None? YES
return -1 ✅
```

---

## 📊 Dry Run — B=10 (Way Out of Bounds)

List has 5 nodes. B=10 means 10 iterations, but the list runs out at i=4.

| `i` | `temp != None?` | Action              | `temp` after |
|:---:|:---------------:|:--------------------|:-------------|
| 0–3 | ✅              | temp = temp.next    | walking...   |
| 4   | ✅              | temp = temp.next    | **None**     |
| 5   | ❌ False        | *skipped*           | None (stays) |
| 6   | ❌ False        | *skipped*           | None (stays) |
| 7–9 | ❌ False        | *skipped*           | None (stays) |

```
After loop: temp = None
return -1 ✅
```

> The guard `if temp != None` prevents a crash when the loop keeps running
> after `temp` has already gone `None`. The body is simply skipped for those
> extra iterations.

---

## 🗺️ Complete Visual Summary

```
LINKED LIST:  1 → 3 → 5 → 7 → 9 → None
INDEX:        0   1   2   3   4

INPUT: B = 2

STEP 1 — Start at head:
  temp → [1]  (index 0)
           A stays here permanently

STEP 2 — Advance B=2 times:
  i=0:  temp = temp.next → [3]  (index 1)
  i=1:  temp = temp.next → [5]  (index 2)

STEP 3 — Check and return:
  temp → [5] (not None)
  return temp.val = 5 ✅

─────────────────────────────────────────────

WHAT IF B = 5?

  i=0: [1]→[3]
  i=1: [3]→[5]
  i=2: [5]→[7]
  i=3: [7]→[9]
  i=4: [9]→None

  temp = None → return -1 ✅

─────────────────────────────────────────────

FORMULA:
  temp starts at index 0
  After B iterations of temp = temp.next → temp is at index B
  If temp is None at any point → out of bounds → -1
```

---

## 🔑 0-Based Indexing — Why B Advances = Index B

This is the core counting logic. Let's prove it once and for all:

```
Index  Advances needed    Path
─────  ───────────────    ────────────────────────────────
  0         0            head               ← already there
  1         1            head → node(1)
  2         2            head → node(1) → node(2)
  3         3            head → node(1) → node(2) → node(3)
  B         B            head → ... → node(B)
```

`range(0, B)` gives exactly B iterations → exactly B advances → lands on index B. ✅

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: Missing the `if temp != None` Guard

```python
# ❌ CRASHES when B > list length
for i in range(0, B):
    temp = temp.next       # When temp is None: AttributeError!

# At i=5 (for a list of 5 nodes): temp=None, then temp.next → CRASH
```

```python
# ✅ CORRECT — guard before accessing .next
for i in range(0, B):
    if temp != None:
        temp = temp.next   # only advance if we haven't fallen off the end
```

---

### ❗ Pitfall 2: Using `range(0, B+1)` — Off by One

```python
# ❌ WRONG — advances B+1 times, lands on index B+1
for i in range(0, B+1):
    if temp != None:
        temp = temp.next

# B=2 on [1,3,5,7,9]: advances 3 times → lands on 7, returns 7 ❌ (should be 5)
```

```python
# ✅ CORRECT — advances exactly B times, lands on index B
for i in range(0, B):
    if temp != None:
        temp = temp.next
```

---

### ❗ Pitfall 3: Moving `A` Instead of `temp`

```python
# ❌ DESTROYS the head reference — can't restart or use A again
for i in range(0, B):
    if A != None:
        A = A.next    # ← A now points somewhere in the middle!

# ✅ CORRECT — keep A intact, walk with temp
temp = A
for i in range(0, B):
    if temp != None:
        temp = temp.next
```

---

### ❗ Pitfall 4: Forgetting 0-Based Indexing

```python
# ❌ If you think B=2 means "2nd element" (1-based):
# you'd use range(0, B-1) → only 1 advance → returns 3 instead of 5

# ✅ B=2 means INDEX 2 (0-based) = 3rd element = advance 2 times
for i in range(0, B):   # B iterations for index B
    ...
```

---

### ❗ Pitfall 5: Not Handling B=0

```python
# B=0 → range(0,0) is empty → loop never runs
# temp stays at head → return A.val ✅

# Works automatically — no special case needed!
```

---

## ⏱️ Complexity Analysis

| Aspect  | Value     | Reason                                         |
|:--------|:---------:|:-----------------------------------------------|
| Time    | **O(B)**  | Walk at most B steps through the list          |
| Space   | **O(1)**  | Only one pointer variable `temp`               |

```
B = 10⁶ → at most 1,000,000 steps → acceptable for linked list access ✅
```

> Unlike arrays where `arr[B]` is O(1), linked list access is O(B) — there's no way
> to "jump" to index B without walking from the head.

---

## 🧪 Test It Yourself

```python
class ListNode:
    def __init__(self, x):
        self.val  = x
        self.next = None

def make_list(vals):
    if not vals: return None
    head = ListNode(vals[0])
    cur  = head
    for v in vals[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head

def solve(A, B):
    temp = A
    for i in range(0, B):
        if temp != None:
            temp = temp.next
    if temp == None:
        return -1
    else:
        return temp.val


tests = [
    ([1,3,5,7,9], 2,  5,   "middle element"),
    ([1,3,5,7,9], 0,  1,   "head (B=0)"),
    ([1,3,5,7,9], 4,  9,   "last element"),
    ([1,3,5,7,9], 5,  -1,  "one past end"),
    ([1,3,5,7,9], 10, -1,  "way past end"),
    ([42],        0,  42,  "single node, B=0"),
    ([42],        1,  -1,  "single node, B=1"),
    ([1, 2],      1,  2,   "two nodes, last"),
]

for vals, B, expected, desc in tests:
    result = solve(make_list(vals), B)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  {desc:30s}  A={vals}  B={B}  → {result}")
```

---

## 🆚 Linked List vs Array: Why Access Differs

```
Array  A = [1, 3, 5, 7, 9]
            ↑           ↑
         index 0     index 4

A[2] = 5   ← instant! O(1) — memory address = base + 2 × element_size

──────────────────────────────────────────────────────────────────

Linked List  1 → 3 → 5 → 7 → 9 → None

No "index" — nodes are scattered in memory, connected only by .next pointers.
To get index 2: start at head, follow .next twice. O(B) always.
```

| Operation       | Array   | Linked List |
|:----------------|:-------:|:-----------:|
| Access index B  | **O(1)**| O(B)        |
| Insert at front | O(N)    | **O(1)**    |
| Insert at back  | O(1)*   | O(N)        |
| Delete a node   | O(N)    | **O(1)**†   |

> † O(1) if you already have a pointer to the node

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Print Linked List** | Same traversal, collect all values |
| **Length of Linked List** | Traverse and count — same loop structure |
| **Find Middle Node** | Fast/slow pointer — avoids counting length first |
| **Reverse a Linked List** | Traversal + pointer rewiring |
| **Nth Node from End** | Two-pointer: one leads by N steps |
| **Doubly Linked List** | Each node has both `.next` and `.prev` |

---

> ✍️ **The Big Idea:**
> Unlike arrays, linked lists don't support index-based access.
> The only path to index B is to walk from the head, advancing one node
> at a time, exactly B times. The loop `for i in range(0, B)` does exactly that.
> The safety guard `if temp != None` prevents crashes when B exceeds the list length —
> instead of crashing, `temp` stays `None` and we return `-1` cleanly.
> Zero-based indexing means index B requires exactly B pointer advances.

---

*Happy Coding! 🚀*
