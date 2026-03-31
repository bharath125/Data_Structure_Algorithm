# 🗑️ Delete a Node in a Linked List

> **Difficulty:** Beginner → Intermediate
> **Topic:** Linked Lists · Node Deletion · Pointer Manipulation
> **Language:** Python
> **Constraints:** 1 ≤ size ≤ 10⁵ · 1 ≤ node value ≤ 10⁹ · 0 ≤ B < size

---

## 📋 Problem Statement

Given the **head** of a linked list and an integer **B**, delete the node at index B (0-based) and return the head of the modified list.

```
Input:  A = 1 → 2 → 3,  B = 1
Output: 1 → 3              (node at index 1, value=2, deleted)

Input:  A = 4 → 3 → 2 → 1,  B = 0
Output: 3 → 2 → 1          (head deleted, new head = 3)
```

---

## 🧩 Understanding the Problem Constraints — Line by Line

### Constraint 1: `1 <= size of linked list <= 10⁵`

> The list **always has at least one node** — you never receive an empty list.
> No need to guard against `A = None`.
>
> Maximum 100,000 nodes — a single traversal O(B) is well within limits.

---

### Constraint 2: `1 <= value of nodes <= 10⁹`

> All node values are **positive integers up to one billion**.
> No zeros, no negatives. This affects nothing in the deletion logic —
> we delete by **index**, not by value.

---

### Constraint 3: `0 <= B < size of linked list`

> This is the most important constraint. B is always a **valid index**.
>
> ```
> size = 5,  valid B: 0, 1, 2, 3, 4
> B can never be 5 or more → never out of bounds
> ```
>
> **What this guarantees:**
> - When we walk to index B-1 (the predecessor), it always exists
> - `temp.next` (the node to delete) always exists — never `None`
> - `temp.next.next` may be `None` (deleting the last node) — that's fine
>
> Because of this constraint, there's **no need to guard against invalid B**.
> The code can safely access `temp.next` and `temp.next.next` without crashing.

---

### Constraint 4: "0-based indexing"

> ```
> List:   [1,  2,  3,  4,  5]
> Index:   0   1   2   3   4
>
> B=0 → delete node with value 1 (the head)
> B=2 → delete node with value 3
> B=4 → delete node with value 5 (the tail)
> ```

---

## 🌍 Real-World Analogy — Before Any Code

### 🚂 Removing a Train Carriage

Imagine a train: `[Car A] → [Car B] → [Car C] → [Car D]`

You need to remove **Car C** (index 2):

**Before:** `A → B → C → D`

**Step 1:** Find **Car B** — the carriage just before the one to remove.

**Step 2:** Reattach Car B's coupling directly to Car D, **skipping Car C**:
```
[Car A] → [Car B] → [Car D]
                     ↑ jumped over Car C
```

Car C is now disconnected — it floats away (garbage collected). The train is shorter and continuous again.

This is exactly what `temp.next = temp.next.next` does.

---

## 🧩 Two Deletion Scenarios

```
List: [1] → [2] → [3] → None

─────────────────────────────────────────────────
SCENARIO 1: B=0  (Delete the HEAD)
─────────────────────────────────────────────────

  Before:   [1] → [2] → [3] → None
             ↑ head = A

  After:    [2] → [3] → None
             ↑ new head

  Mechanism: A = A.next   (skip the head entirely)
  Return:    A             (new head = old second node)

─────────────────────────────────────────────────
SCENARIO 2: B > 0  (Delete a Middle or Tail Node)
─────────────────────────────────────────────────

  Delete index 1 (value=2):
  Before:   [1] → [2] → [3] → None
             ↑ temp (predecessor at index B-1=0)
                    ↑ node to skip

  After:    [1] → [3] → None
             ↑ temp.next rewired to skip [2]

  Mechanism: temp.next = temp.next.next
  Return:    A (head unchanged)
```

---

## 🔍 The Code — Every Line Explained

```python
def solve(self, A, B):
    if B == 0:                        # 1. Head deletion special case
        A = A.next
        return A
    temp = A                          # 2. Start traversal pointer
    for i in range(B):                # 3. Loop B times (i = 0 to B-1)
        if i == B-1:                  # 4. Are we on the FINAL iteration?
            temp.next = temp.next.next  # 5. Skip the B-th node
            return A                  # 6. Return unchanged head
        temp = temp.next              # 7. Advance toward predecessor
    return A
```

---

### `if B == 0:` — Head Deletion

```python
if B == 0:
    A = A.next
    return A
```

> Deleting the head is special because the **head pointer itself changes**.
> For all other deletions, the head stays the same and we return `A` unchanged.
>
> ```
> Before: A → [1] → [2] → [3]
>                          (A points to node(1))
>
> A = A.next → A now points to node(2)
>
> After:  A → [2] → [3]
>              ↑ new head
> ```
>
> node(1) is now unreachable — it will be garbage collected.
>
> **Why not handle B=0 in the loop?** Because the loop logic needs a predecessor node
> (`temp` at index B-1). For B=0, there's no predecessor — the head itself is deleted.
> The special case avoids this by directly advancing the head pointer.

---

### `temp = A`

```python
temp = A
```

> Sets up a **traversal pointer** starting at the head.
> `A` stays fixed so we can return it at the end.
> `temp` will walk until it sits at the node **just before** the one to delete (index B-1).

---

### `for i in range(B):`

```python
for i in range(B):
```

> `range(B)` generates: `0, 1, 2, ..., B-1` — exactly **B values**.
>
> The loop runs B times. The **final iteration** (when `i = B-1`) is where the deletion happens.
> The earlier iterations (`i = 0` to `i = B-2`) just advance `temp` toward the predecessor.
>
> ```
> B=1: range(1) → [0]        → 1 iteration  (only final: i=0)
> B=2: range(2) → [0, 1]     → 2 iterations (advance once, then final)
> B=3: range(3) → [0, 1, 2]  → 3 iterations (advance twice, then final)
> ```

---

### `if i == B-1:` — The Final Iteration Detector

```python
if i == B-1:
    temp.next = temp.next.next
    return A
```

> The last value in `range(B)` is always `B-1`.
> So `i == B-1` is `True` only on the **last** loop iteration.
>
> **At this moment**, `temp` has been advanced B-1 times from the head.
> That means `temp` is sitting at **index B-1** — exactly one position before the node to delete.
>
> ```
> temp     is at index B-1   ← predecessor
> temp.next is at index B    ← the node to DELETE
> temp.next.next is at index B+1  ← the successor (or None)
> ```
>
> **`temp.next = temp.next.next`** — the skip operation:
>
> ```
> Before:  temp → [B-1] → [B] → [B+1]
>                          ↑ will be deleted
>
> After:   temp → [B-1] ──────► [B+1]
>                          ↑ [B] is now unreachable → garbage collected
> ```

---

### `temp = temp.next` — Advance During Earlier Iterations

```python
temp = temp.next
```

> This only executes when `i < B-1` (not the final iteration).
> Each execution moves `temp` one node forward.
>
> After `i` iterations (where `i < B-1`): `temp` is at index `i+1`.
> After all B-1 non-final iterations: `temp` is at index `B-1`. ✅

---

### Why the Loop Works: Alternative Mental Model

```
for i in range(B):
    if i == B-1:   ← ONLY on final iteration
        delete here
    else:           ← all other iterations
        advance

This is equivalent to:
  Walk B-1 times to reach the predecessor
  Then delete
```

> Think of `range(B)` as generating B "ticks." The first B-1 ticks advance `temp`.
> The B-th tick (when `i = B-1`) performs the deletion.

---

## 📊 Full Dry Run — Example 1: `A=[1,2,3]`, B=1

**Initial:** temp = node(1), B=1

```
List:   [1] → [2] → [3] → None
Index:   0     1     2
         ↑ temp
```

**Loop: `range(1)` → only `i=0`**

```
i=0:
  i == B-1?  0 == 0?  ✅ YES — final iteration

  temp = node(1)  (at index 0 = B-1)
  temp.next       = node(2)  ← the node to DELETE (index 1 = B)
  temp.next.next  = node(3)  ← the successor

  temp.next = temp.next.next
  → node(1).next = node(3)

  [1] → [3] → None   ✅  (node(2) skipped, garbage collected)

  return A  (head = node(1), unchanged)
```

**Result: `[1, 3]`** ✅

---

## 📊 Full Dry Run — Example 2: `A=[4,3,2,1]`, B=0

```
B == 0? ✅ YES

  A = A.next  →  A now points to node(3)
  return A

Result: [3, 2, 1]  ✅
```

---

## 📊 Full Dry Run — `A=[1,2,3]`, B=2 (Delete Last Node)

**Loop: `range(2)` → i=0, i=1**

| `i` | `i == B-1?` | Action                   | `temp` after        |
|:---:|:-----------:|:-------------------------|:--------------------|
| 0   | 0==1? ❌    | `temp = temp.next`       | node(2) at index 1  |
| 1   | 1==1? ✅    | `temp.next = temp.next.next` → `None` | done |

```
temp = node(2)
temp.next = node(3)
temp.next.next = None  ← deleting the last node

After:  node(2).next = None
        [1] → [2] → None   ✅  (node(3) removed)

return A (head = node(1), unchanged)
Result: [1, 2]  ✅
```

---

## 📊 Full Dry Run — `A=[1,2,3,4,5]`, B=3 (Middle Delete)

**Loop: `range(3)` → i=0, i=1, i=2**

| `i` | `i == B-1?` | Action                     | `temp` position    |
|:---:|:-----------:|:---------------------------|:-------------------|
| 0   | 0==2? ❌    | `temp = temp.next` → node(2) | index 1            |
| 1   | 1==2? ❌    | `temp = temp.next` → node(3) | index 2            |
| 2   | 2==2? ✅    | `temp.next = temp.next.next` | deletes node(4)    |

```
temp = node(3) at index 2 = B-1
temp.next       = node(4)  ← DELETE
temp.next.next  = node(5)  ← successor

node(3).next = node(5)
[1] → [2] → [3] → [5] → None  ✅

Result: [1, 2, 3, 5]  ✅
```

---

## 🎨 Visual — The Skip Operation

```
BEFORE DELETION (delete index B=2, value=3):

  [1]  →  [2]  →  [3]  →  [4]  → None
   0        1       2       3
                    ↑
                 DELETE

  temp is at index 1 (= B-1 = predecessor)

  temp        →  node(2)
  temp.next   →  node(3)   ← to be deleted
  temp.next.next → node(4) ← successor

──────────────────────────────────────────────

STEP: temp.next = temp.next.next

  [1]  →  [2]  ──────────►  [4]  → None
   0        1       ✗        3
                    ↑
              node(3) skipped!
              No pointer → garbage collected

AFTER:

  [1]  →  [2]  →  [4]  → None  ✅
```

---

## 🔑 The Core Deletion Formula

```
To delete index B:

  1. Walk to the PREDECESSOR at index B-1
     (the node whose .next points to the node we want gone)

  2. Rewire:
     predecessor.next = predecessor.next.next
                              ↑ skip over the deleted node

  ┌───────────────────────────────────────────────────────────┐
  │  predecessor.next     = node to DELETE                    │
  │  predecessor.next.next = node AFTER deleted node          │
  │                                                           │
  │  temp.next = temp.next.next  ← one line does it all ✅    │
  └───────────────────────────────────────────────────────────┘
```

---

## 🆚 Deletion vs Insertion — Side by Side

| Aspect | Insertion | Deletion |
|:-------|:----------|:---------|
| Two pointer lines | `newNode.next = temp.next` then `temp.next = newNode` | `temp.next = temp.next.next` (one line) |
| Head special case | `newNode.next = A; return newNode` | `A = A.next; return A` |
| Walk to | Index C-1 (before insertion point) | Index B-1 (before node to delete) |
| Loop count | `range(C-1)` | `range(B)` with check `i == B-1` |
| What returns | New head (if C=0) or old A | New head (if B=0) or old A |

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: Using `range(B-1)` Instead of `range(B)` with `i == B-1`

```python
# Alternative (cleaner) approach that's equivalent:
temp = A
for i in range(B-1):         # walk B-1 steps to reach predecessor
    temp = temp.next
temp.next = temp.next.next   # skip the B-th node
return A
```

> The code in this solution uses `range(B)` with an `if i == B-1` check instead,
> achieving the same result. Both are correct; the `range(B-1)` version is arguably
> more readable.

---

### ❗ Pitfall 2: Forgetting the B=0 Special Case

```python
# ❌ WRONG — for B=0, there's no predecessor to walk to
temp = A
for i in range(B):    # range(0) → empty loop, temp never moves
    ...
temp.next = temp.next.next  # temp is at head, deletes node at index 1! Wrong ❌

# ✅ CORRECT — handle head deletion separately
if B == 0:
    return A.next
```

---

### ❗ Pitfall 3: Trying to Delete by Setting `temp = temp.next` at the Node

```python
# ❌ WRONG — this doesn't actually remove the node from the chain
temp = walk_to_index_B(A, B)
temp = temp.next   # temp now points past the node, but the chain is UNCHANGED!

# The predecessor still points to the "deleted" node — nothing changed in the list.
# You must rewire the PREDECESSOR's .next pointer, not move your local variable.

# ✅ CORRECT — rewire via the predecessor
temp = walk_to_index_B_minus_1(A, B)  # stop at B-1
temp.next = temp.next.next            # predecessor skips over B ✅
```

---

### ❗ Pitfall 4: Accessing `temp.next.next` When `temp.next` is the Last Node

```python
# This is actually SAFE here because temp.next.next = None is valid Python
# (assigning None to temp.next means temp becomes the new tail)

temp.next = temp.next.next
# If temp.next.next is None → temp.next = None → temp is the new tail ✅
```

> The constraint `B < size` guarantees `temp.next` is never `None` at this point.
> `temp.next.next` being `None` is perfectly fine — it just means we're deleting the tail.

---

### ❗ Pitfall 5: Not Returning the New Head After B=0

```python
# ❌ WRONG — forgets to return the new head
if B == 0:
    A = A.next
# Returns nothing (None in Python) or falls through to wrong return

# ✅ CORRECT
if B == 0:
    A = A.next
    return A       # ← essential! return new head
```

---

## ⏱️ Complexity Analysis

| Aspect  | Value     | Reason                                           |
|:--------|:---------:|:-------------------------------------------------|
| Time    | **O(B)**  | Walk at most B steps to find the predecessor    |
| Space   | **O(1)**  | One pointer variable `temp`, no extra allocation |

```
B = 10⁵ → at most 100,000 steps → fast ✅
Deletion itself: O(1) — just one pointer reassignment
```

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

def list_to_arr(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def solve(A, B):
    if B == 0:
        return A.next
    temp = A
    for i in range(B):
        if i == B-1:
            temp.next = temp.next.next
            return A
        temp = temp.next
    return A


tests = [
    ([1,2,3],   1, [1,3],   "delete middle"),
    ([4,3,2,1], 0, [3,2,1], "delete head"),
    ([1,2,3],   0, [2,3],   "delete head of 3-node"),
    ([1,2,3],   2, [1,2],   "delete tail"),
    ([1],       0, [],      "delete only node"),
    ([1,2],     1, [1],     "delete tail of 2-node"),
    ([1,2,3,4,5], 3, [1,2,3,5], "delete index 3"),
    ([1,2,3,4,5], 0, [2,3,4,5], "delete head of 5-node"),
    ([1,2,3,4,5], 4, [1,2,3,4], "delete tail of 5-node"),
]

for vals, B, expected, desc in tests:
    result  = solve(make_list(vals), B)
    got     = list_to_arr(result) if result else []
    status  = "✅" if got == expected else f"❌ expected {expected}"
    print(f"{status}  {desc:30s}  A={vals}  B={B}  → {got}")
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Insert in Linked List** | Mirror: add a new node instead of removing one |
| **Delete Nth Node from End** | Two-pointer technique to find B from the tail |
| **Remove Duplicates from Sorted List** | Delete while traversing — same skip pattern |
| **Reverse a Linked List** | Rewiring all `.next` pointers in reverse |
| **Linked List Cycle Detection** | Floyd's fast/slow pointer algorithm |
| **Doubly Linked List Deletion** | Also wire `.prev` pointer of successor |

---

> ✍️ **The Big Idea:**
> Deleting a node from a linked list doesn't require touching the node being deleted.
> Instead, find its **predecessor** (the node at index B-1) and make it "skip over"
> the target: `predecessor.next = predecessor.next.next`.
> The deleted node becomes unreachable and is garbage collected automatically.
> Head deletion (B=0) is a special case because there's no predecessor —
> the head pointer itself advances forward.
> The constraint `B < size` guarantees the target always exists,
> so no bounds checking is needed inside the deletion step.

---

*Happy Coding! 🚀*
