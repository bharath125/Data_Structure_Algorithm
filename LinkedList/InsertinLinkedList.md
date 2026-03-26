# 🔗 Insert a Node in a Linked List

> **Difficulty:** Beginner → Intermediate
> **Topic:** Linked Lists · Node Insertion · Pointer Manipulation
> **Language:** Python
> **Constraints:** 0 ≤ list size ≤ 10⁵ · 1 ≤ B ≤ 10⁹ · 0 ≤ C ≤ 10⁵

---

## 📋 Problem Statement

Given the **head** of a linked list, a **value B**, and a **position C**, insert a new node with value B at index C (0-based).

Special rules:
- **C = 0** → insert at the **head**
- **C ≥ list length** → insert at the **tail**
- Return the head of the modified list

---

## 🧩 Understanding the Problem Constraints — Line by Line

### Constraint 1: `0 <= size of linked list <= 10⁵`

> The list can be **completely empty** (size = 0, `A = None`).
> This must be handled — you can't access `.next` on `None`.
>
> ```
> A = None, B = 5, C = 0
> → The new node becomes the entire list → return newNode
> ```

---

### Constraint 2: `1 <= value of nodes <= 10⁹` and `1 <= B <= 10⁹`

> All values (existing and new) are **positive integers up to one billion**.
> No zeros, no negatives. The new node value B follows the same range.

---

### Constraint 3: `0 <= C <= 10⁵`

> C is the **target index** — always non-negative.
> - `C = 0` → insert before the head (new head)
> - `C = 1` → insert after index 0, before index 1
> - `C ≥ list length` → insert at the tail
>
> C can be up to 100,000, but if the list is shorter, we simply insert at the tail.

---

### Constraint 4: "0-based indexing"

> ```
> List:   [1,  2,  3,  4]
> Index:   0   1   2   3
>
> C=0 → new node becomes index 0 (new head)
> C=1 → new node becomes index 1 (after old head)
> C=2 → new node becomes index 2
> C=9 → list too short → insert at tail
> ```

---

## 🌍 Real-World Analogy — Before Any Code

### 🚂 Inserting a Train Carriage

Imagine a train: `[Car A] → [Car B] → [Car C]`

You want to insert a **new car** after Car B:

**Step 1:** Attach the new car's front coupling to Car C:
```
[New Car] ──front──► [Car C]
```

**Step 2:** Attach Car B's rear coupling to the new car:
```
[Car B] ──rear──► [New Car] ──front──► [Car C]
```

**Why this order?** If you attach Car B to the new car first (Step 2 before Step 1), you lose the connection to Car C forever — it detaches and floats away! Always connect the **new node to its successor before** disconnecting the predecessor.

This exact principle drives the two-line pointer swap at the heart of the algorithm.

---

## 🧩 Four Insertion Scenarios

```
Original list: [1] → [2] → None

C=0: Insert B=3 at HEAD
  [3] → [1] → [2] → None   ← new node becomes the head

C=1: Insert B=3 at INDEX 1
  [1] → [3] → [2] → None   ← new node goes between index 0 and 1

C=2: Insert B=3 at TAIL (index 2 = after last element)
  [1] → [2] → [3] → None   ← new node appended at end

C=5: Insert B=3 BEYOND LENGTH (list only has 2 nodes)
  [1] → [2] → [3] → None   ← treated same as tail insert
```

---

## 🔍 The Code — Every Line Explained

```python
def solve(self, A, B, C):
    newNode = ListNode(B)          # 1. Create the new node
    if A is None:                  # 2. Empty list special case
        return newNode
    if C == 0:                     # 3. Head insertion special case
        newNode.next = A
        head = newNode
        return head
    temp = A                       # 4. Start traversal pointer
    for i in range(0, C-1):        # 5. Walk to node just BEFORE position C
        if temp.next == None:      # 6. Hit the end early (C > length)
            break
        temp = temp.next           # 7. Advance pointer
    if temp == None:               # 8. Safety check (never fires in practice)
        return A
    newNode.next = temp.next       # 9. Connect new node to successor  ← ORDER MATTERS
    temp.next = newNode            # 10. Connect predecessor to new node
    return A                       # 11. Head is unchanged (not a head insertion)
```

---

### `newNode = ListNode(B)`

```python
newNode = ListNode(B)
```

> Creates a brand-new node with value B.
>
> ```
> newNode.val  = B
> newNode.next = None   ← not connected to anything yet
> ```
>
> This is always the first step — you need the node before you can place it anywhere.

---

### `if A is None: return newNode`

```python
if A is None:
    return newNode
```

> Handles the **empty list case**. When `A = None`, there's no existing list.
> The new node becomes both the head and the only node.
>
> ```
> Before: None
> After:  [B] → None     ← newNode is the entire list
> Return: newNode         ← this is the new head
> ```
>
> Without this guard, `A.next` or `A.val` later in the code would crash with `AttributeError`.

---

### Head Insertion (`C == 0`)

```python
if C == 0:
    newNode.next = A
    head = newNode
    return head
```

> When C=0, the new node must become the **new head** — it goes before everything.
>
> ```
> BEFORE:   A → [1] → [2] → None
>
> Step 1: newNode.next = A
>           newNode → [1] → [2] → None
>
> Step 2: head = newNode
>           head → newNode → [1] → [2] → None
>
> AFTER:  [B] → [1] → [2] → None   ← newNode is now the head
> ```
>
> **Why return `head` (not `A`)?** Because the head of the list has **changed**.
> `A` still points to the old first node. We must return the new head (`newNode`).
> For all other insertions, `A` is still the head, so we return `A`.

---

### `temp = A`

```python
temp = A
```

> Sets up a **traversal pointer** that starts at the head.
> `A` stays fixed so we can return it at the end.
> `temp` will walk forward until it reaches the node just **before** position C.

---

### `for i in range(0, C-1):` — Walk to the Node Before C

```python
for i in range(0, C-1):
    if temp.next == None:
        break
    temp = temp.next
```

> **Why `C-1` not `C`?**
>
> To insert at position C, we need to reach the node at position **C-1** — the node
> whose `.next` we're about to change. That's `C-1` advances from the head.
>
> ```
> Insert at C=1 → stop at index 0  → C-1=0 advances → range(0,0) = empty → no movement
> Insert at C=2 → stop at index 1  → C-1=1 advance  → range(0,1) = [0] → 1 step
> Insert at C=3 → stop at index 2  → C-1=2 advances → range(0,2) = [0,1] → 2 steps
> ```
>
> **`if temp.next == None: break`** — Early exit when we hit the tail before reaching C-1.
> This handles "C ≥ list length" by stopping at the last node, making it a tail insertion.
>
> ```
> List=[1,2], C=5:
>   i=0: temp=node(1), temp.next=node(2) → advance → temp=node(2)
>   i=1: temp=node(2), temp.next=None    → BREAK
>   temp = node(2) (last node) → insert after it → tail insertion ✅
> ```

---

### `if temp == None: return A`

```python
if temp == None:
    return A
```

> A defensive safety check. In practice, `temp` can never be `None` here because:
> - We already handled the empty list (`A is None`) earlier
> - The loop's `if temp.next == None: break` stops before `temp` goes `None`
>
> This is a **fallback guard** — it never fires for valid inputs but prevents
> any unexpected crash from edge cases.

---

### The Two-Line Pointer Surgery

```python
newNode.next = temp.next    # Line 9 — connect new node to successor FIRST
temp.next = newNode         # Line 10 — connect predecessor to new node SECOND
```

> **The order is non-negotiable.** Inserting node(3) between node(1) and node(2):
>
> **BEFORE:**
> ```
> temp → [1] → [2] → None
> newNode → [3] → None
> ```
>
> **Line 9: `newNode.next = temp.next`**
> ```
> newNode → [3] → [2] → None   ← [3] now knows where [2] is
> temp    → [1] → [2] → None   ← [1] still connected to [2]
> ```
>
> **Line 10: `temp.next = newNode`**
> ```
> temp → [1] → [3] → [2] → None   ✅ complete chain
> ```
>
> **IF REVERSED:**
> ```
> WRONG Step 1: temp.next = newNode
>   → [1] → [3] → None    ← [2] is LOST FOREVER!
>
> WRONG Step 2: newNode.next = temp.next
>   → [3].next = [3]   ← points to ITSELF (circular loop!) ❌
> ```

---

### `return A`

```python
return A
```

> For all non-head insertions, the original head `A` is unchanged.
> The insertion happened in the middle or at the tail — `A` still correctly
> points to the first node.

---

## 📊 Full Dry Run — Example 1: `A=[1,2]`, B=3, C=0 (Head Insert)

```
newNode = node(3), newNode.next = None

A is None? No
C == 0? ✅ YES

  Step 1: newNode.next = A
  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ val = 3  │────►│ val = 1  │────►│ val = 2  │────► None
  │ (newNode)│     │          │     │          │
  └──────────┘     └──────────┘     └──────────┘
       ↑ new head

  return newNode

Result: [3] → [1] → [2] → None  ✅
```

---

## 📊 Full Dry Run — Example 2: `A=[1,2]`, B=3, C=1 (Middle Insert)

```
newNode = node(3)
A is None? No | C==0? No
temp = node(1)

Loop: range(0, C-1) = range(0, 0) = []  ← empty, no iterations!
temp stays at node(1) (index 0)

temp == None? No
```

**Step 9:** `newNode.next = temp.next`
```
  newNode → [3] → [2] → None
  [1] → [2] → None             ← temp still connected to [2]
```

**Step 10:** `temp.next = newNode`
```
  [1] → [3] → [2] → None  ✅
```

```
return A = node(1)
Result: [1] → [3] → [2]  ✅
```

---

## 📊 Dry Run — C=2 (Tail Insert for 2-Node List)

`A=[1,2]`, B=3, C=2

```
temp = node(1)
Loop: range(0, 1) → runs once for i=0

  i=0: temp.next=node(2) ≠ None → temp = node(2)

temp = node(2) [the last node], temp.next = None

  newNode.next = None      →  node(3) → None
  node(2).next = node(3)   →  [1] → [2] → [3] → None

Result: [1] → [2] → [3]  ✅
```

---

## 📊 Dry Run — C=5 (Beyond Length → Tail)

`A=[1,2]`, B=3, C=5

```
temp = node(1)
Loop: range(0, 4) → i=0,1,2,3 planned

  i=0: temp=node(1), temp.next=node(2) → advance → temp=node(2)
  i=1: temp=node(2), temp.next=None    → BREAK (early exit!)

(iterations i=2 and i=3 never run)

temp = node(2) — same result as C=2 from here

  newNode.next = None
  node(2).next = node(3)

Result: [1] → [2] → [3]  ✅
```

---

## 🎨 Visual Summary — All Four Cases

```
Original list: [1] → [2] → None

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CASE 1: C=0 (Head Insert)
  [3] ──────────────► [1] → [2] → None
   ↑ new head          ↑ old head
  newNode.next = A → return newNode

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CASE 2: C=1 (Insert After Index 0)
  [1] → [3] → [2] → None
   ↑ temp   ↑ newNode
  range(0,0) → empty loop, temp stays at head
  newNode.next=[2], then [1].next=newNode

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CASE 3: C=2 (Tail Insert)
  [1] → [2] → [3] → None
         ↑ temp    ↑ newNode
  range(0,1) → 1 step, temp advances to node(2)
  newNode.next=None, then [2].next=newNode

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CASE 4: C=5 (Beyond End → Same as Tail)
  break fires at i=1 when temp.next=None
  temp = last node → identical to CASE 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔑 The Golden Rule of Pointer Surgery

```
✅ CORRECT ORDER:
  1. newNode.next = temp.next    ← save the successor link FIRST
  2. temp.next = newNode         ← then redirect the predecessor

❌ WRONG ORDER:
  1. temp.next = newNode         ← successor link is LOST
  2. newNode.next = temp.next    ← temp.next is now newNode → circular!
```

Memory trick: **"Save the future before changing the past."**

---

## 🔢 Why `range(0, C-1)` — The Insertion Point

```
To insert at index C, temp must land at index C-1:

  C=1 → land at index 0 → 0 advances → range(0, 0) → empty
  C=2 → land at index 1 → 1 advance  → range(0, 1)
  C=3 → land at index 2 → 2 advances → range(0, 2)
  C=k → land at index k-1 → k-1 advances → range(0, k-1) ✅
```

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: Wrong Pointer Surgery Order

```python
# ❌ WRONG — successor lost forever!
temp.next = newNode         # [1]→[3], [2] is now unreachable
newNode.next = temp.next    # newNode.next = newNode (circular!)

# ✅ CORRECT
newNode.next = temp.next    # save [2] first
temp.next = newNode         # then redirect [1]→[3]→[2] ✅
```

---

### ❗ Pitfall 2: `range(0, C)` Instead of `range(0, C-1)`

```python
# ❌ WRONG — walks one step too far, inserts AFTER C not AT C
for i in range(0, C):
    temp = temp.next

# ✅ CORRECT — stops one before C
for i in range(0, C-1):
    if temp.next == None: break
    temp = temp.next
```

---

### ❗ Pitfall 3: Returning `A` After Head Insertion

```python
# ❌ WRONG — returns old head, new head is unreachable!
if C == 0:
    newNode.next = A
    return A          # A is the OLD head — new head (newNode) is lost

# ✅ CORRECT
if C == 0:
    newNode.next = A
    return newNode    # return the NEW head
```

---

### ❗ Pitfall 4: Not Handling Empty List

```python
# ❌ CRASH — A is None, loop tries A.next → AttributeError
temp = A
for i in range(0, C-1):
    temp = temp.next  # None.next → crash!

# ✅ Guard early
if A is None:
    return newNode
```

---

### ❗ Pitfall 5: Missing the Early Break

```python
# ❌ CRASH when C > list length
for i in range(0, C-1):
    temp = temp.next  # temp becomes None, next iteration crashes

# ✅ Break when tail is reached
for i in range(0, C-1):
    if temp.next == None:
        break          # stop at last node → tail insertion
    temp = temp.next
```

---

## ⏱️ Complexity Analysis

| Aspect  | Value     | Reason                                          |
|:--------|:---------:|:------------------------------------------------|
| Time    | **O(C)**  | Walk at most C-1 steps to find insertion point |
| Space   | **O(1)**  | One new node + one pointer variable             |

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
    cur = head
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

def solve(A, B, C):
    newNode = ListNode(B)
    if A is None:
        return newNode
    if C == 0:
        newNode.next = A
        return newNode
    temp = A
    for i in range(0, C-1):
        if temp.next == None:
            break
        temp = temp.next
    if temp == None:
        return A
    newNode.next = temp.next
    temp.next = newNode
    return A


tests = [
    ([1,2],   3, 0, [3,1,2],   "insert at head"),
    ([1,2],   3, 1, [1,3,2],   "insert at index 1"),
    ([1,2],   3, 2, [1,2,3],   "insert at tail"),
    ([1,2],   3, 5, [1,2,3],   "C beyond length → tail"),
    ([1,2,3], 9, 1, [1,9,2,3], "insert in 3-node list"),
    ([],      5, 0, [5],        "empty list"),
    ([1],     2, 0, [2,1],      "single node, head insert"),
    ([1],     2, 1, [1,2],      "single node, tail insert"),
]

for vals, B, C, expected, desc in tests:
    result = solve(make_list(vals) if vals else None, B, C)
    got    = list_to_arr(result)
    status = "✅" if got == expected else f"❌ expected {expected}"
    print(f"{status}  {desc:35s}  → {got}")
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Delete a Node** | Mirror of insert: rewire `.next` to skip a node |
| **Reverse a Linked List** | Rewire all `.next` pointers in reverse |
| **Insert at Sorted Position** | Find the right spot by value, then same pointer surgery |
| **Doubly Linked List Insert** | Same idea, also wire `.prev` pointers |
| **Stack using Linked List** | Push = insert at head, Pop = remove from head |
| **Merge Two Sorted Lists** | Interleave `.next` pointers across two lists |

---

> ✍️ **The Big Idea:**
> Inserting into a linked list requires three distinct cases: empty list, head, and middle/tail.
> The head case returns a new head pointer. Middle/tail insertion uses the
> **two-line pointer surgery**: save the successor link first (`newNode.next = temp.next`),
> then redirect the predecessor (`temp.next = newNode`). Order is critical.
> The loop walks to index `C-1` (not `C`) because we need the node **before**
> the insertion point. An early `break` when `temp.next == None` naturally
> handles the "C beyond length → tail insert" case.

---

*Happy Coding! 🚀*
