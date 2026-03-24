# 🔗 Print a Linked List — Node by Node

> **Difficulty:** Absolute Beginner → Comfortable
> **Topic:** Linked Lists · Traversal · String Formatting
> **Language:** Python
> **Constraints:** 1 ≤ size ≤ 10⁵ · 1 ≤ node value ≤ 10⁹

---

## 📋 Problem Statement

Given the **head node** of a singly linked list, print all node values in order, separated by spaces. The last value must also be followed by a space, and a newline must come at the very end.

```
Input:  1 → 2 → 3 → None
Output: "1 2 3 \n"
         ↑       ↑  ↑
     space-sep  trailing space + newline
```

---

## 🧩 Understanding the Problem Constraints — Line by Line

### Constraint 1: `1 <= size of linked list <= 10⁵`

> The list always has **at least one node** — you never receive an empty list (`A = None`).
> So there's no need to guard against a null head.
>
> Maximum 100,000 nodes — the solution must be efficient. A simple single traversal
> O(N) is perfect.

---

### Constraint 2: `1 <= value of nodes <= 10⁹`

> All values are **positive integers** and can be as large as one billion.
> This means:
> - No negative numbers, no zeros — purely positive
> - Values can be multi-digit (up to 10 digits long)
> - Storing them as strings for printing is safe and straightforward

---

### Output Rule: Trailing space + newline

> The problem says: *"The last node value must also be succeeded by a space."*
> This is unusual — most problems don't want a trailing space.
> Here it's **explicitly required**.
>
> `print(" ".join(values) + " ")` produces:
> ```
> "1 2 3 \n"
>         ↑ trailing space (manual: + " ")
>               ↑ newline (automatic from print())
> ```

---

## 🌍 Real-World Analogy — Before Any Code

### 🚂 Train Carriages

A linked list is like a **train**. Each carriage (node) holds:
- A **passenger** (the value)
- A **door to the next carriage** (the `.next` pointer)

```
[Carriage 1 | door→] → [Carriage 2 | door→] → [Carriage 3 | door→None]
    val=1                   val=2                   val=3
```

To list all passengers, you:
1. Start at Carriage 1 (the head)
2. Note the passenger
3. Walk through the door to Carriage 2
4. Repeat until there's no next door (`next = None`)

That walking process = **linked list traversal**. The code does exactly this.

---

## 🧱 What Is a Linked List? — For Absolute Beginners

### The `ListNode` Class

```python
class ListNode:
    def __init__(self, x):
        self.val  = x     # the data stored in this node
        self.next = None  # pointer to the next node (starts as None)
```

Every node is a small object with exactly **two things**:
- `val` — the number it holds
- `next` — a reference (pointer) to the next node, or `None` if it's the last

---

### How a Linked List Looks in Memory

```
A = 1 → 2 → 3

In memory:

┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  val  =  1   │     │  val  =  2   │     │  val  =  3   │
│  next = ──── │ ──► │  next = ──── │ ──► │  next = None │
└──────────────┘     └──────────────┘     └──────────────┘
      ↑
    head (A)
```

The **head** `A` gives you the first node. To reach node 2, you follow `A.next`.
To reach node 3, you follow `A.next.next`. There's **no way to jump directly** to a middle node — you must walk from the start.

---

### Linked List vs Array

| Feature            | Array                  | Linked List              |
|:-------------------|:----------------------:|:------------------------:|
| Access by index    | O(1) — `arr[3]`        | O(N) — must walk to it   |
| Insert at front    | O(N) — shift all       | O(1) — rewire pointer    |
| Memory layout      | Contiguous block       | Scattered, connected     |
| Know the length?   | Yes — `len(arr)`       | No — must count by walking |

---

## 🔍 The Code — Every Line Explained

```python
class Solution:
    def solve(self, A):
        values  = []            # Step 1: prepare an empty collection
        current = A             # Step 2: start at the head

        while current:          # Step 3: keep going until the end
            values.append(str(current.val))   # Step 4: collect each value
            current = current.next            # Step 5: move to next node

        print(" ".join(values) + " ")         # Step 6: format and print
```

---

### `values = []`

```python
values = []
```

> An empty Python list that will accumulate all node values **as strings**.
>
> Why collect first, then print? Because `" ".join(values)` needs the full list
> at once to insert spaces correctly — we can't know how many spaces to add
> until we know how many values there are.
>
> Think of it as **gathering all passengers' names** before announcing them on a PA system.

---

### `current = A`

```python
current = A
```

> `A` is the **head node** — the entry point of the linked list.
> We never move `A` itself (we'd lose the reference to the start).
> Instead, we create a **separate pointer** `current` that we advance through the list.
>
> This is the standard traversal pattern:
> ```
> current = head
> while current:
>     ... do something with current ...
>     current = current.next
> ```
>
> `A` stays fixed. `current` walks.

---

### `while current:`

```python
while current:
```

> In Python, any object is "truthy" and `None` is "falsy."
>
> ```
> current = some_node  → truthy → loop continues
> current = None       → falsy  → loop stops
> ```
>
> So `while current:` means "keep looping while we haven't reached the end."
> The last node has `next = None`, so after processing it, `current = current.next = None`,
> and the loop stops naturally on the next check.
>
> This is equivalent to writing `while current is not None:` — just more concise.

---

### `values.append(str(current.val))`

```python
values.append(str(current.val))
```

> Two things happening here:

**`current.val`** — reads the integer stored in the current node.

**`str(...)`** — converts the integer to a string.

> ```python
> current.val = 1000000000   # an integer
> str(current.val) = "1000000000"   # a string
> ```
>
> Why convert? Because `" ".join()` requires **all elements to be strings**.
> Passing integers directly causes a `TypeError`:
> ```python
> " ".join([1, 2, 3])       # ❌ TypeError: sequence item 0: expected str instance, int found
> " ".join(["1","2","3"])   # ✅ "1 2 3"
> ```

**`.append(...)`** — adds the string to the end of the `values` list.

> ```
> After node 1: values = ['1']
> After node 2: values = ['1', '2']
> After node 3: values = ['1', '2', '3']
> ```

---

### `current = current.next`

```python
current = current.next
```

> **The most important line in any linked list traversal.**
>
> This advances `current` from the current node to the next one.
>
> ```
> Before: current → node(1) → node(2) → node(3) → None
> After:  current           → node(2) → node(3) → None
> ```
>
> Without this line, `current` would stay on node 1 forever:
> ```python
> # ❌ MISSING current = current.next → Infinite Loop!
> while current:
>     values.append(str(current.val))
>     # current never moves → same node every iteration → loop never ends
> ```
>
> When `current` is on the **last node**, `current.next = None`.
> After this line executes, `current = None`, and `while current:` becomes
> `while None:` → False → loop exits. ✅

---

### `print(" ".join(values) + " ")`

```python
print(" ".join(values) + " ")
```

> Three operations chained together:

**`" ".join(values)`** — joins all strings in the list with a single space between them.

> ```python
> values = ['1', '2', '3']
> " ".join(values) = "1 2 3"
>                    ↑ ↑ ↑
>                    space inserted between each pair
> ```
>
> `join` puts the separator **between** elements only — so there's no leading or trailing space from `join` itself.

**`+ " "`** — appends a trailing space after the last element.

> ```python
> "1 2 3" + " " = "1 2 3 "
>                         ↑ required by the problem
> ```

**`print(...)`** — outputs the string followed by an automatic newline `\n`.

> ```python
> print("1 2 3 ")
> # Output: "1 2 3 \n"
>            ↑     ↑
>       the string  newline from print()
> ```

---

## 📊 Full Dry Run — `A = 1 → 2 → 3`

**Memory picture:**
```
A (head) → [val=1, next→] → [val=2, next→] → [val=3, next=None]
```

**Initial state:**
```python
values  = []
current = node(1)   ← pointing at the first node
```

---

**Iteration 1:**
```
current = node(1) → truthy → enter loop

  current.val = 1
  str(1) = '1'
  values.append('1') → values = ['1']
  current = current.next → current = node(2)

Loop condition: current = node(2) → truthy → continue
```

---

**Iteration 2:**
```
current = node(2) → truthy → enter loop

  current.val = 2
  str(2) = '2'
  values.append('2') → values = ['1', '2']
  current = current.next → current = node(3)

Loop condition: current = node(3) → truthy → continue
```

---

**Iteration 3:**
```
current = node(3) → truthy → enter loop

  current.val = 3
  str(3) = '3'
  values.append('3') → values = ['1', '2', '3']
  current = current.next → current = None

Loop condition: current = None → falsy → EXIT LOOP
```

---

**After loop:**
```python
values = ['1', '2', '3']
" ".join(values) = "1 2 3"
"1 2 3" + " "  = "1 2 3 "
print("1 2 3 ")
→ Output: "1 2 3 \n"
```

---

## 📊 Dry Run — `A = 4 → 3 → 2 → 1`

| Iteration | `current.val` | `str(val)` | `values` after append | `current` after advance |
|:---------:|:-------------:|:----------:|:----------------------|:------------------------|
| 1         | 4             | `'4'`      | `['4']`               | node(3)                 |
| 2         | 3             | `'3'`      | `['4','3']`           | node(2)                 |
| 3         | 2             | `'2'`      | `['4','3','2']`       | node(1)                 |
| 4         | 1             | `'1'`      | `['4','3','2','1']`   | `None` → stop           |

```python
" ".join(['4','3','2','1']) + " " = "4 3 2 1 "
print("4 3 2 1 ")
→ Output: "4 3 2 1 \n"  ✅
```

---

## 📊 Dry Run — Single Node `A = [42]`

```
current = node(42) → truthy

  values.append('42') → values = ['42']
  current = current.next = None

current = None → loop exits

" ".join(['42']) + " " = "42 "
print("42 ")
→ Output: "42 \n"  ✅
```

> `" ".join(['42'])` with a single element produces just `"42"` — no spaces added
> (nothing between elements when there's only one). The `+ " "` adds the required trailing space.

---

## 🗺️ Complete Visual Summary

```
LINKED LIST:  A = 1 → 2 → 3 → None

TRAVERSAL:

  current      values list
  ─────────    ──────────────────
  node(1)  →   ['1']
  node(2)  →   ['1', '2']
  node(3)  →   ['1', '2', '3']
  None     →   loop ends

FORMATTING:
  ['1', '2', '3']
       ↓
  " ".join(...)  →  "1 2 3"    (space BETWEEN each)
       ↓
  + " "          →  "1 2 3 "   (trailing space added)
       ↓
  print(...)     →  1 2 3 ↵    (newline from print)

OUTPUT: "1 2 3 \n"
```

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: Forgetting `current = current.next`

```python
# ❌ INFINITE LOOP — current never moves!
while current:
    values.append(str(current.val))
    # current stays at node(1) forever

# ✅ CORRECT — advance the pointer every iteration
while current:
    values.append(str(current.val))
    current = current.next    # ← essential!
```

---

### ❗ Pitfall 2: Using `current.val` Without `str()`

```python
# ❌ TypeError — join requires strings, not integers
values.append(current.val)
print(" ".join(values))   # → TypeError!

# ✅ Convert to string first
values.append(str(current.val))
print(" ".join(values))   # → "1 2 3"  ✅
```

---

### ❗ Pitfall 3: Moving `A` Instead of `current`

```python
# ❌ WRONG — moves the head, loses the list!
while A:
    values.append(str(A.val))
    A = A.next    # A no longer points to the head!
    # If you need A again later in the function, it's gone

# ✅ CORRECT — create a separate traversal pointer
current = A       # keep A safe
while current:
    values.append(str(current.val))
    current = current.next
```

---

### ❗ Pitfall 4: Missing Trailing Space

```python
# ❌ No trailing space — fails the output requirement
print(" ".join(values))       # "1 2 3"  (no trailing space)

# ✅ Add trailing space explicitly
print(" ".join(values) + " ") # "1 2 3 "  ✅
```

---

### ❗ Pitfall 5: Printing Inside the Loop

```python
# ❌ Prints each value on its own — wrong format
while current:
    print(current.val, end=" ")
    current = current.next
print()   # newline

# This produces "1 2 3 \n" correctly by luck, but:
# - Harder to control trailing space precisely
# - Less clean separation of "collect" vs "output"
# - Can't easily verify the full string before printing

# ✅ Collect ALL values, then format and print ONCE
while current:
    values.append(str(current.val))
    current = current.next
print(" ".join(values) + " ")
```

---

## ⏱️ Complexity Analysis

| Aspect  | Value     | Reason                                             |
|:--------|:---------:|:---------------------------------------------------|
| Time    | **O(N)**  | Visit every node exactly once                      |
| Space   | **O(N)**  | `values` list stores one string per node           |

```
N = 100,000 nodes → 100,000 iterations → instant ✅
```

> **Can space be O(1)?** Yes, by printing each value directly inside the loop
> (using `print(current.val, end=" ")`), but the collect-then-join pattern
> is cleaner and easier to test.

---

## 🧪 Test It Yourself

```python
class ListNode:
    def __init__(self, x):
        self.val  = x
        self.next = None

def make_list(vals):
    """Helper: build a linked list from a Python list."""
    if not vals: return None
    head = ListNode(vals[0])
    cur  = head
    for v in vals[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head

def solve(A):
    values  = []
    current = A
    while current:
        values.append(str(current.val))
        current = current.next
    print(" ".join(values) + " ")


# Tests
solve(make_list([1, 2, 3]))           # "1 2 3 "
solve(make_list([4, 3, 2, 1]))        # "4 3 2 1 "
solve(make_list([42]))                # "42 "
solve(make_list([1, 1000000000]))     # "1 1000000000 "
solve(make_list([7, 7, 7, 7]))        # "7 7 7 7 "
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Linked List Reversal** | Traverse + rewire pointers in-place |
| **Find Length of Linked List** | Same traversal, count instead of collect |
| **Detect Cycle in Linked List** | Two-pointer (fast/slow) traversal |
| **Middle of Linked List** | Fast/slow pointer technique |
| **Merge Two Sorted Lists** | Traversal on two lists simultaneously |
| **Doubly Linked List** | Each node has both `.next` AND `.prev` |

---

> ✍️ **The Big Idea:**
> A linked list has no random access — the only way to read its values is to
> **walk it from the head** using the `.next` chain, one node at a time.
> The traversal pattern (`current = head` → `while current:` → `current = current.next`)
> is the foundation of almost every linked list algorithm.
> Here, we collect all values into a list, then format them in one shot
> using `" ".join()` + a trailing space, satisfying the output constraints exactly.

---

*Happy Coding! 🚀*
