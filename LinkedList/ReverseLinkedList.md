# 🔄 Reverse a Linked List — In-Place, One-Pas

> **Difficulty:** Beginner → Intermediate
> **Topic:** Linked Lists · Pointer Manipulation · In-Place Reversal
> **Language:** Python
> **Constraints:** 1 ≤ length ≤ 10⁵ · 32-bit integer values · **In-place · One-pass**

---

## 📋 Problem Statement

Given the **head** of a singly linked list, reverse all the links so that the last node becomes the new head and all `.next` pointers point in the opposite direction.

```
Before: 1 → 2 → 3 → 4 → 5 → None
After:  5 → 4 → 3 → 2 → 1 → None
        ↑
     new head (return this)
```

**Constraints:** Do it **in-place** (no extra list/array) and in a **single pass** (visit each node exactly once).

---

## 🧩 Understanding the Problem Constraints — Line by Line

### Constraint 1: `1 <= Length of linked list <= 10⁵`

> The list always has **at least one node** — `A` is never `None`.
> Single-node lists are valid input and must be handled.
> Maximum 100,000 nodes — a single O(N) pass is perfect.

---

### Constraint 2: "Value of each node is within the range of a 32-bit integer"

> Node values can range from **-2,147,483,648 to 2,147,483,647**.
> This includes negatives and zero — unlike previous problems.
> The reversal logic doesn't care about values — it only rewires `.next` pointers.

---

### Constraint 3: "In-place"

> You must **not** create a new linked list or use an array to store values
> and rebuild. Every node already in the list must be reused.
>
> ```python
> # ❌ NOT in-place — creates new nodes or uses extra memory
> vals = [node.val for all nodes]  # O(N) space
> rebuild list from reversed vals
>
> # ✅ In-place — rewires existing nodes' .next pointers
> curr.next = prev   # no new nodes, just redirecting arrows
> ```

---

### Constraint 4: "One-pass"

> Visit each node **exactly once**. No second traversal to find lengths,
> no counting nodes first, no recursion that implicitly revisits nodes.
> The while loop visits each node once and reverses its arrow immediately.

---

## 🌍 Real-World Analogy — Before Any Code

### 🚂 Reversing a Train

Imagine a train where each carriage has a **coupling** connecting to the next one:

```
[1] → [2] → [3] → [4] → [5] → (buffer stop)
```

You want to reverse the train:

```
(buffer stop) ← [1] ← [2] ← [3] ← [4] ← [5]
```

Which reads forward as: `[5] → [4] → [3] → [2] → [1] → None`

**How?** Walk along the train. At each carriage:
1. **Remember** where the next carriage is (before detaching)
2. **Detach** the forward coupling and **reattach** it backward (to where you came from)
3. **Move forward** to the carriage you remembered

After visiting every carriage, the whole train is reversed.

---

## 💡 The Core Idea — Reverse Each Arrow One by One

Original:  `1 → 2 → 3 → 4 → 5 → None`

We need: `None ← 1 ← 2 ← 3 ← 4 ← 5`

Each arrow (`→`) must become (`←`). We do this **one arrow at a time**, left to right.

```
Step 1: reverse arrow on node 1
  None ← 1  |  2 → 3 → 4 → 5 → None

Step 2: reverse arrow on node 2
  None ← 1 ← 2  |  3 → 4 → 5 → None

Step 3: reverse arrow on node 3
  None ← 1 ← 2 ← 3  |  4 → 5 → None

... and so on until all arrows are reversed.
```

We need **three pointers** to do this safely:
- `prev` — where the current node should now point TO (its new `.next`)
- `curr` — the node we're currently reversing
- `nextNode` — saved copy of where `curr` used to point (so we don't lose the rest of the list)

---

## 🔍 The Code — Every Line Explained

```python
def reverseList(self, A):
    prev = None                         # 1. Previous node (starts as None)
    curr = A                            # 2. Current node (starts at head)

    if curr.next == None:               # 3. Single node early return
        return A

    while curr != None:                 # 4. Process every node
        nextNode = curr.next            # 5. Save the forward link FIRST
        curr.next = prev                # 6. Reverse: point current node backward
        prev = curr                     # 7. Advance prev to current node
        curr = nextNode                 # 8. Advance curr to saved next node

    A = prev                            # 9. prev is now the new head
    return A                            # 10. Return new head
```

---

### `prev = None`

```python
prev = None
```

> `prev` tracks the **last processed node** — the node that `curr` should point to
> after reversal. Starts as `None` because the first node (currently the head)
> will become the **tail** after reversal, and the tail must point to `None`.
>
> ```
> Original head node (1) becomes the tail → its .next must be None
> So prev=None means "point backward to nothing" for node(1) ✅
> ```

---

### `curr = A`

```python
curr = A
```

> `curr` is the **node currently being processed** — the one whose arrow we're reversing.
> Starts at the head and advances forward each iteration.

---

### `if curr.next == None: return A`

```python
if curr.next == None:
    return A
```

> **Single-node optimisation.** If the list has only one node, there's nothing to reverse
> — return it immediately.
>
> **Is this necessary for correctness?** No. Without it, the while loop would run once:
> `nextNode=None, curr.next=None (was already None), prev=node, curr=None → return node` ✅
>
> It's an **early return for clarity and speed**, not a bug fix.

---

### `while curr != None:`

```python
while curr != None:
```

> Keep processing nodes until `curr` has gone past the last node.
> After the final node is processed, `curr = nextNode = None`, and the loop stops.
> At that point, `prev` points to what was the last node — the new head.

---

### `nextNode = curr.next` — The Most Critical Line

```python
nextNode = curr.next
```

> **Save the forward link BEFORE reversing it.**
>
> On the very next line, we're about to **overwrite `curr.next`**.
> If we don't save `curr.next` first, we lose our path forward through the list forever.
>
> ```
> ❌ WITHOUT SAVING nextNode:
>   curr.next = prev        ← curr.next now points BACKWARD
>   curr = curr.next        ← follows the NEW backward pointer!
>   → We move backward, not forward — infinite loop or wrong result!
>
> ✅ WITH SAVING nextNode:
>   nextNode = curr.next    ← save the forward path
>   curr.next = prev        ← safely overwrite curr.next
>   curr = nextNode         ← follow the saved path forward ✅
> ```

Think of it like saving a bookmark before turning the page.

---

### `curr.next = prev` — The Reversal

```python
curr.next = prev
```

> This is the actual reversal — it **flips the arrow** on `curr`.
>
> ```
> Before: ... ← prev  curr → nextNode → ...
>                      ↑ curr.next points RIGHT
>
> After:  ... ← prev ← curr  nextNode → ...
>                      ↑ curr.next now points LEFT (to prev)
> ```
>
> For the first node (when `prev = None`):
> `curr.next = None` → node 1 becomes the new tail pointing to `None` ✅

---

### `prev = curr`

```python
prev = curr
```

> **Advance `prev`** to the current node. Now `prev` points to the node we just reversed.
> When we process the next node, it will need to point back to `curr` (now the new `prev`).

---

### `curr = nextNode`

```python
curr = nextNode
```

> **Advance `curr`** to the next unprocessed node (which we saved earlier).
> The while loop continues with this node in the next iteration.

---

### `A = prev` and `return A`

```python
A = prev
return A
```

> When the loop ends (`curr = None`), `prev` is sitting on the **last node of the original list** —
> which is now the **new head** of the reversed list.
>
> We update `A` and return it as the new head.

---

## 📊 The Four Steps Per Iteration — Summary

Every single iteration of the while loop does exactly **four things** in order:

```
┌───────────────────────────────────────────────────────────────┐
│ Step A: nextNode = curr.next   → SAVE the forward link        │
│ Step B: curr.next = prev       → REVERSE the current arrow    │
│ Step C: prev = curr            → ADVANCE prev one step right  │
│ Step D: curr = nextNode        → ADVANCE curr one step right  │
└───────────────────────────────────────────────────────────────┘
```

Repeat until `curr = None`.

---

## 📊 Full Dry Run — `A = [1, 2, 3, 4, 5]`

**Initial:** `prev = None`, `curr = node(1)`

---

**Iteration 1:**
```
State:    prev=None   curr=1   curr.next=2

A: nextNode = curr.next = 2     ← save forward path to node(2)
B: curr.next = prev = None      ← node(1) now points to None (becomes tail!)
C: prev = curr = node(1)        ← prev moves to node(1)
D: curr = nextNode = node(2)    ← curr moves to node(2)

Reversed so far:  None ← [1]      Remaining: [2] → [3] → [4] → [5] → None
```

---

**Iteration 2:**
```
State:    prev=1   curr=2   curr.next=3

A: nextNode = 3
B: curr.next = prev = node(1)    ← node(2) now points to node(1)
C: prev = node(2)
D: curr = node(3)

Reversed so far:  None ← [1] ← [2]      Remaining: [3] → [4] → [5] → None
```

---

**Iteration 3:**
```
State:    prev=2   curr=3   curr.next=4

A: nextNode = 4
B: curr.next = node(2)           ← node(3) → node(2)
C: prev = node(3)
D: curr = node(4)

Reversed so far:  None ← [1] ← [2] ← [3]      Remaining: [4] → [5] → None
```

---

**Iteration 4:**
```
State:    prev=3   curr=4   curr.next=5

A: nextNode = 5
B: curr.next = node(3)           ← node(4) → node(3)
C: prev = node(4)
D: curr = node(5)

Reversed so far:  None ← [1] ← [2] ← [3] ← [4]      Remaining: [5] → None
```

---

**Iteration 5:**
```
State:    prev=4   curr=5   curr.next=None

A: nextNode = None
B: curr.next = node(4)           ← node(5) → node(4)
C: prev = node(5)
D: curr = None

Reversed so far:  None ← [1] ← [2] ← [3] ← [4] ← [5]
```

---

**Loop ends:** `curr = None`

```
A = prev = node(5)  ← new head!
return node(5)

Final: 5 → 4 → 3 → 2 → 1 → None  ✅
```

---

## 📊 Concise Table — `A = [1, 2, 3]`

| Step | `prev` | `curr` | `nextNode` | `curr.next` set to | Effect |
|:----:|:------:|:------:|:----------:|:------------------:|:-------|
| Init | None   | 1      | —          | —                  | Start  |
| 1    | None   | 1      | 2          | None               | 1→None |
| 2    | 1      | 2      | 3          | 1                  | 2→1    |
| 3    | 2      | 3      | None       | 2                  | 3→2    |
| End  | **3**  | None   | —          | —                  | return 3 |

**Result:** `3 → 2 → 1 → None` ✅

---

## 🎨 Visual — Arrow Reversal Progress

```
ORIGINAL:
  1 → 2 → 3 → 4 → 5 → None

AFTER ITERATION 1 (processed node 1):
  None ← 1  |  2 → 3 → 4 → 5 → None
              ↑
         barrier between reversed (left) and unreversed (right)

AFTER ITERATION 2 (processed node 2):
  None ← 1 ← 2  |  3 → 4 → 5 → None

AFTER ITERATION 3:
  None ← 1 ← 2 ← 3  |  4 → 5 → None

AFTER ITERATION 4:
  None ← 1 ← 2 ← 3 ← 4  |  5 → None

AFTER ITERATION 5:
  None ← 1 ← 2 ← 3 ← 4 ← 5

READ FORWARD (from prev=5):
  5 → 4 → 3 → 2 → 1 → None  ✅

─────────────────────────────────────────────────────
AT EVERY MOMENT:
  prev → [reversed chain] → None
  curr → [unreversed chain] → None
─────────────────────────────────────────────────────
```

---

## 🔑 Why The Order of the Four Lines Matters

The four lines inside the while loop **must be in this exact order:**

```python
nextNode = curr.next    # MUST be first  — saves forward link before it's overwritten
curr.next = prev        # reversal step
prev = curr             # MUST be after curr.next is set — prev now holds the reversed node
curr = nextNode         # MUST be last   — uses saved nextNode to advance
```

**What breaks if you swap them:**

```python
# ❌ SWAP lines 1 and 2:
curr.next = prev        # curr.next overwritten!
nextNode = curr.next    # nextNode = prev (we just set this!) — forward path LOST

# ❌ SWAP lines 3 and 4:
curr = nextNode         # curr advances first
prev = curr             # prev = new curr (wrong! should be old curr)
```

---

## 🗺️ Three-Pointer State Machine

```
At the start of each iteration, the three pointers always satisfy:

  ... [fully reversed] ← prev    curr → [unreversed] ...

  - Everything LEFT of prev (including prev) has its arrow reversed
  - Everything RIGHT of curr (including curr) still has its arrow unreversed
  - nextNode is used temporarily to bridge the gap

After the last iteration:
  prev = last original node = new head
  curr = None (past the end)
```

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: Forgetting to Save `nextNode` Before Reversing

```python
# ❌ WRONG ORDER — forward link lost before saving!
curr.next = prev        # overwrites curr.next
curr = curr.next        # curr.next is now prev → moves BACKWARD!

# ✅ CORRECT — save first, then overwrite
nextNode = curr.next    # save before overwriting
curr.next = prev        # now safe to reverse
curr = nextNode         # advance using saved link
```

---

### ❗ Pitfall 2: Returning `A` Instead of `prev`

```python
# After the loop, A still points to the ORIGINAL head (now the tail)
# ❌ WRONG
return A       # returns old head (now tail) → wrong!

# ✅ CORRECT
A = prev
return A       # prev points to the new head (old tail) ✅
```

---

### ❗ Pitfall 3: Using `while curr.next != None` Instead of `while curr != None`

```python
# ❌ WRONG — stops one node early (last node never processed)
while curr.next != None:
    ...
# Last node's arrow never gets reversed → still points forward!

# ✅ CORRECT — process EVERY node including the last one
while curr != None:
    ...
```

---

### ❗ Pitfall 4: Not Updating Both `prev` and `curr` at the End

```python
# ❌ WRONG — forgetting to advance curr means infinite loop
nextNode = curr.next
curr.next = prev
prev = curr
# curr = nextNode   ← MISSING → curr never moves → infinite loop!

# ✅ CORRECT — all four assignments every iteration
nextNode = curr.next
curr.next = prev
prev = curr
curr = nextNode
```

---

## ⏱️ Complexity Analysis

| Aspect  | Value     | Reason                                           |
|:--------|:---------:|:-------------------------------------------------|
| Time    | **O(N)**  | Each node visited exactly once (one-pass)        |
| Space   | **O(1)**  | Three pointer variables: `prev`, `curr`, `nextNode` |

```
N = 100,000 → 100,000 iterations → instant ✅
No new nodes created, no arrays allocated → truly in-place
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

def reverseList(A):
    prev = None
    curr = A
    if curr.next == None:
        return A
    while curr != None:
        nextNode  = curr.next
        curr.next = prev
        prev      = curr
        curr      = nextNode
    return prev   # simplified: A = prev; return A


tests = [
    ([1,2,3,4,5], [5,4,3,2,1], "standard 5-node"),
    ([3],         [3],         "single node"),
    ([1,2],       [2,1],       "two nodes"),
    ([1,2,3],     [3,2,1],     "three nodes"),
    ([5,4,3,2,1], [1,2,3,4,5], "already reversed"),
    ([-1,-2,-3],  [-3,-2,-1],  "negative values"),
]

for vals, expected, desc in tests:
    result = reverseList(make_list(vals))
    got    = list_to_arr(result)
    status = "✅" if got == expected else f"❌ expected {expected}"
    print(f"{status}  {desc:25s}  → {got}")
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Reverse Linked List II** | Reverse only a subrange [left, right] |
| **Palindrome Linked List** | Reverse second half and compare with first |
| **Reorder List** | Reverse second half, then interleave with first |
| **Recursive Reversal** | Same logic using the call stack instead of explicit pointers |
| **Doubly Linked List Reversal** | Also swap `.prev` and `.next` on each node |
| **K-Group Reversal** | Reverse every K nodes at a time |

---

> ✍️ **The Big Idea:**
> Reversing a linked list in-place means changing every node's `.next` to point
> **backward** instead of forward. Three pointers do the job:
> `prev` (reversed chain's front), `curr` (node being processed), `nextNode` (saved forward path).
> The single critical rule: **save `nextNode` before overwriting `curr.next`** —
> otherwise you lose your path through the rest of the list.
> After the loop, `prev` is the new head — it points to what was the original last node,
> which now leads a fully reversed chain back to `None`.

---

*Happy Coding! 🚀*
