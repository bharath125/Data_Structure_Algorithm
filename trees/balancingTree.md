# ⚖️ Balanced Binary Tree — Bottom-Up Recursion

> **Difficulty:** Intermediate → Advanced
> **Topic:** Binary Trees · Recursion · DFS · Height Computation
> **Language:** Python
> **Constraints:** 1 ≤ size ≤ 10⁵ · Time: **O(N)** · Space: **O(H)**

---

## 📋 Problem Statement

Given the root of a binary tree, return **1** if it is height-balanced, **0** otherwise.

**Height-balanced definition:** For **every node** in the tree, the heights of its left and right subtrees differ by **at most 1**.

```
Height-balanced ✅          NOT height-balanced ❌

      1                           1
     / \                         /
    2   3                       2
                               /
                              3

|height(left) - height(right)|    Root: |2 - 0| = 2 > 1
= |1 - 1| = 0 ≤ 1 ✅              ❌ not balanced
```

---

## 🧩 Understanding the Problem Constraints — Line by Line

### Constraint 1: `1 <= size of tree <= 10⁵`

> The tree always has **at least one node** — root is never `None`.
> A single node is trivially balanced (no subtrees to compare).
>
> Maximum 100,000 nodes — the solution must be efficient.
> O(N²) would be too slow for a skewed tree with 10⁵ nodes. O(N) is required.

---

### Constraint 2: "Depth of two subtrees of EVERY node never differ by more than 1"

> The condition must hold for **every single node** — not just the root.
>
> ```
>        1              ← check: |height(2's subtree) - height(3's subtree)| ≤ 1
>       / \
>      2   3            ← check each of these nodes too
>     / \
>    4   5              ← check these too — EVERY node must pass
> ```
>
> A tree where only the root is balanced but some internal node isn't
> is **still considered unbalanced**.

---

### Constraint 3: "Height" vs "Depth"

> **Height** of a node = length of the longest path **downward** to a leaf.
> - A leaf node has height **1** (or 0 depending on convention — this code uses leaf = 1)
> - `None` node has height **0**
>
> ```
>     1        ← height 3
>    / \
>   2   3      ← height 2 (node 2), height 1 (node 3)
>  /
> 4            ← height 1 (leaf)
> ```

---

## 🌍 Real-World Analogy — Before Any Code

### 🏗️ Building Inspection

Imagine a building inspector checking a large structure of interconnected floors (a tree). Each **junction** (node) connects to two sub-structures (left and right subtrees).

The inspector checks: *"Are the heights of the left wing and right wing at this junction within 1 floor of each other?"*

**Naive approach:** For every junction, measure both wings from scratch. Very slow for a large building (O(N²)).

**Smart approach:** Start from the **bottom floors** and report the height upward. While reporting height, *also* check the balance condition. If any wing is unbalanced, send a "BROKEN" signal (-1) up. Once a -1 reaches a junction, that junction immediately passes -1 upward without measuring anything further.

This is the **bottom-up** strategy: measure height once per node, check balance on the way up.

---

## 💡 The Key Insight — Dual-Purpose Return Value

The `height` function returns:

| Return value | Meaning |
|:------------|:--------|
| A positive integer | Height of this subtree AND it's balanced so far |
| `-1` | This subtree is **unbalanced** — stop everything, propagate up |

```python
# Normal: return actual height
return max(Left, Right) + 1   # e.g. returns 3

# Sentinel: return -1 to signal "found imbalance — abort"
return -1
```

This dual-purpose trick lets us:
- **Compute height** bottom-up in a single pass
- **Detect imbalance** the moment it occurs
- **Short-circuit** immediately — no further computation once -1 is spotted

---

## 🔍 The Code — Every Line Explained

```python
def isBalanced(self, A):
    def height(A):                          # inner recursive function
        if A == None: return 0              # base case: empty node = height 0
        Left = height(A.left)               # compute left subtree height
        if Left == -1: return -1            # early exit: left already broken
        Right = height(A.right)             # compute right subtree height
        if Right == -1: return -1           # early exit: right already broken
        if abs(Left - Right) > 1: return -1 # this node is unbalanced
        return max(Left, Right) + 1         # balanced: return actual height
    return 0 if height(A) == -1 else 1      # convert -1/height to 0/1
```

---

### `def height(A):` — Inner Function

```python
def height(A):
```

> Defined **inside** `isBalanced` — this is a Python **closure**. It has access to
> the outer function's scope but is invisible outside.
>
> It serves two roles simultaneously:
> 1. Returns the **height** of the subtree rooted at `A` (if balanced)
> 2. Returns **-1** if any imbalance was found anywhere in this subtree

---

### `if A == None: return 0`

```python
if A == None: return 0
```

> **Base case of the recursion.** An empty node has height **0**.
>
> ```
> Why 0?
>   A leaf node's children are both None.
>   height(leaf.left)  = 0
>   height(leaf.right) = 0
>   → leaf height = max(0,0)+1 = 1 ✅ (leaf has height 1)
> ```
>
> This correctly makes leaf nodes height 1 and propagates heights upward.
>
> This also prevents `None.left` or `None.val` crashes — all recursion stops here.

---

### `Left = height(A.left)` and `if Left == -1: return -1`

```python
Left = height(A.left)
if Left == -1: return -1
```

> Recurse into the **left subtree** first.
>
> The `if Left == -1: return -1` is the **early exit guard**.
> If the left subtree is already unbalanced (returned -1), there's no point
> computing the right subtree — the whole tree is unbalanced regardless.
>
> ```
> Think of it as: "If my left wing is broken, I don't need to measure my right wing.
> I already know the whole building fails inspection."
> ```
>
> Without this guard, we'd still recurse into the right subtree even when
> we already know the answer is "unbalanced" — wasting computation.

---

### `Right = height(A.right)` and `if Right == -1: return -1`

```python
Right = height(A.right)
if Right == -1: return -1
```

> Same logic for the **right subtree**.
> Only reached if the left subtree was balanced (Left ≠ -1).
>
> After both guards, we know: Left ≥ 0 AND Right ≥ 0
> Both subtrees are balanced — now we just check the current node.

---

### `if abs(Left - Right) > 1: return -1`

```python
if abs(Left - Right) > 1: return -1
```

> **The balance condition check at this node.**
>
> `abs(Left - Right)` = difference in heights between left and right subtrees.
>
> ```
> Left=1, Right=1 → difference=0 ✅ balanced
> Left=2, Right=1 → difference=1 ✅ still balanced (≤1 allowed)
> Left=3, Right=1 → difference=2 ❌ unbalanced → return -1
> Left=0, Right=2 → difference=2 ❌ unbalanced → return -1
> ```
>
> If we reach this line, both subtrees are balanced within themselves.
> We're checking if **this specific node** satisfies the balance condition.

---

### `return max(Left, Right) + 1`

```python
return max(Left, Right) + 1
```

> **All checks passed!** This node and both its subtrees are balanced.
> Return the actual height of this subtree.
>
> `max(Left, Right)` = height of the taller subtree.
> `+ 1` = add this node itself to the height.
>
> ```
> Node with Left=2, Right=1 → height = max(2,1)+1 = 3
> Leaf node: Left=0, Right=0 → height = max(0,0)+1 = 1
> ```

---

### `return 0 if height(A) == -1 else 1`

```python
return 0 if height(A) == -1 else 1
```

> Calls `height(A)` on the root and converts the result to the required format:
>
> ```
> height(A) == -1  →  unbalanced  →  return 0
> height(A) >= 1   →  balanced    →  return 1
> ```
>
> Python ternary: `value_if_true if condition else value_if_false`

---

## 📊 Full Dry Run — Example 1: Balanced Tree

```
    1
   / \
  2   3
```

**Call stack (bottom-up recursion):**

```
height(1)
├── height(2)
│   ├── height(None) → returns 0     [left of 2]
│   │   Left = 0, not -1
│   ├── height(None) → returns 0     [right of 2]
│   │   Right = 0, not -1
│   │   |0 - 0| = 0 ≤ 1 ✅
│   └── return max(0,0)+1 = 1
│
│   Left = 1, not -1
│
├── height(3)
│   ├── height(None) → returns 0     [left of 3]
│   │   Left = 0, not -1
│   ├── height(None) → returns 0     [right of 3]
│   │   Right = 0, not -1
│   │   |0 - 0| = 0 ≤ 1 ✅
│   └── return max(0,0)+1 = 1
│
│   Right = 1, not -1
│   |1 - 1| = 0 ≤ 1 ✅
└── return max(1,1)+1 = 2

height(root) = 2  (not -1) → return 1 ✅
```

---

## 📊 Full Dry Run — Example 2: Unbalanced Tree

```
  1
 /
2
/
3
```

**Call stack:**

```
height(1)
└── height(2)                      [left of 1]
    └── height(3)                  [left of 2]
        ├── height(None) → 0       [left of 3]
        │   Left = 0
        ├── height(None) → 0       [right of 3]
        │   Right = 0
        │   |0-0| = 0 ≤ 1 ✅
        └── return max(0,0)+1 = 1

        Left = 1, not -1
    ├── height(None) → 0           [right of 2]
        Right = 0
        |1-0| = 1 ≤ 1 ✅  (node 2 is barely balanced itself)
    └── return max(1,0)+1 = 2

    Left = 2, not -1
└── height(None) → 0               [right of 1]
    Right = 0
    |2 - 0| = 2 > 1 ❌ UNBALANCED!
    return -1

height(root) = -1 → return 0 ✅
```

> Note: Node 2's subtree is itself balanced (|1-0|=1 ≤ 1). Only the **root node** fails.
> This is why we must check **every** node — not just the root or just the leaves.

---

## 🎨 Visual — The Dual-Purpose Return Value

```
BALANCED subtree → returns actual HEIGHT
UNBALANCED subtree → returns -1 (sentinel signal)

         height values flowing UPWARD:

    ✅ Balanced tree [1,2,3]:

         2          ← height(root) = 2 → return 1
        / \
       1   1        ← height(2) = 1, height(3) = 1
      / \ / \
     0  0 0  0      ← height(None) = 0

    ❌ Unbalanced tree [1,2,None,3]:

         -1         ← height(root) = -1 → return 0
        /    \
       2      0     ← height(2)=2, height(None)=0, |2-0|=2>1 → -1
      / \
     1   0          ← height(3)=1, height(None)=0, |1-0|=1≤1 ✅
    / \
   0   0            ← leaves
```

---

## 🆚 Brute Force O(N²) vs Optimised O(N)

### Brute Force Approach

```python
def isBalanced_brute(root):
    def getHeight(node):                # separate height function
        if not node: return 0
        return 1 + max(getHeight(node.left), getHeight(node.right))

    if not root: return True
    left_h  = getHeight(root.left)      # compute height: O(N)
    right_h = getHeight(root.right)     # compute height: O(N)
    if abs(left_h - right_h) > 1: return False
    return isBalanced_brute(root.left) and isBalanced_brute(root.right)
    # ↑ recurse on children — each child calls getHeight again!
```

For a skewed tree of N nodes:
- Root calls `getHeight` on N nodes: O(N)
- Then recurses on the child, which calls `getHeight` on N-1 nodes: O(N-1)
- Total: O(N) + O(N-1) + ... + O(1) = **O(N²)** ❌

---

### This Solution — O(N)

```python
def height(A):
    if A == None: return 0
    Left  = height(A.left)              # ← also checks balance below!
    if Left  == -1: return -1
    Right = height(A.right)             # ← also checks balance below!
    if Right == -1: return -1
    if abs(Left - Right) > 1: return -1
    return max(Left, Right) + 1
```

Each node is visited **exactly once**. Height is computed and balance is checked in the **same recursive call** — no recomputation. Total: **O(N)** ✅

```
N = 100,000 (skewed tree):
Brute force: 100,000² / 2 = 5 × 10⁹ operations ❌
Optimised:   100,000 operations ✅
```

---

## 📊 Recursion Call Order Visualised

```
For a balanced tree:       1
                          / \
                         2   3
                        / \
                       4   5

The recursion goes DEPTH-FIRST, hitting leaves first:

Call order:
  height(1)           ← enters first
    height(2)
      height(4)
        height(None)  ← returns 0
        height(None)  ← returns 0
      returns 1       ← height(4) returns
      height(5)
        height(None)  ← returns 0
        height(None)  ← returns 0
      returns 1       ← height(5) returns
    returns 2         ← height(2) returns
    height(3)
      height(None)    ← returns 0
      height(None)    ← returns 0
    returns 1         ← height(3) returns
  |2-1|=1 ≤ 1 ✅
  returns 3           ← height(1) returns

Each node visited ONCE → O(N) total
```

---

## ⚠️ Common Pitfalls

### ❗ Pitfall 1: Forgetting the Early Exit Guards

```python
# ❌ WRONG — always computes both subtrees even when left is -1
Left  = height(A.left)
Right = height(A.right)             # wasteful when Left==-1

# ✅ CORRECT — skip right subtree if left already broken
Left = height(A.left)
if Left == -1: return -1            # ← early exit
Right = height(A.right)
```

Without the guard, the code still gives **correct answers** (since `-1` would still propagate up via the `abs(Left-Right)>1` check), but it wastes time visiting subtrees we already know are unbalanced.

---

### ❗ Pitfall 2: Checking Balance Only at the Root

```python
# ❌ WRONG — only checks root's balance
left_h  = getHeight(root.left)
right_h = getHeight(root.right)
if abs(left_h - right_h) > 1: return False  # only root checked!
return True

# This would incorrectly call the tree below "balanced":
#       1
#      / \
#     2   3
#    /
#   4
#  /
# 5
# Root: |3-1|=2 → caught ✅
# But what if the imbalance was deeper?
```

The correct solution checks **every node** via the bottom-up recursion.

---

### ❗ Pitfall 3: Using Height 0 for Leaves Instead of Height 1

This is a convention question. The code uses:
- `None` → height 0
- leaf → height 1 (= max(0,0)+1)

This is consistent and correct. Just be consistent throughout — if you change the base case, update all comparisons.

---

### ❗ Pitfall 4: Off-by-One in the Balance Check

```python
if abs(Left - Right) > 1: return -1   # ✅ difference of 2+ is unbalanced
if abs(Left - Right) >= 1: return -1  # ❌ difference of exactly 1 is STILL balanced!
```

A difference of **exactly 1** is **allowed**. `> 1` is correct; `>= 1` is too strict.

---

## ⏱️ Complexity Analysis

| Aspect         | Value          | Reason                                        |
|:---------------|:--------------:|:----------------------------------------------|
| Time           | **O(N)**       | Each node visited exactly once                |
| Space          | **O(H)**       | Recursion call stack depth = tree height H    |
| Best case space| O(log N)       | Balanced tree: H = log₂N                     |
| Worst case space| O(N)          | Skewed tree: H = N (linear chain)             |

---

## 🧪 Test It Yourself

```python
class TreeNode:
    def __init__(self, x):
        self.val   = x
        self.left  = None
        self.right = None

def make_tree(vals):
    """Build tree from level-order (BFS) list. None = missing node."""
    if not vals or vals[0] is None: return None
    root = TreeNode(vals[0])
    queue, i = [root], 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root

def isBalanced(A):
    def height(A):
        if A == None: return 0
        Left = height(A.left)
        if Left == -1: return -1
        Right = height(A.right)
        if Right == -1: return -1
        if abs(Left - Right) > 1: return -1
        return max(Left, Right) + 1
    return 0 if height(A) == -1 else 1


tests = [
    ([1, 2, 3],          1, "balanced 3 nodes"),
    ([1, 2, None, 3],    0, "left spine 3 nodes (unbalanced at root)"),
    ([1],                1, "single node"),
    ([1,2,3,4,5,6,7],   1, "perfect 7-node tree"),
    ([1,2,3,4,None,None,None,5], 0, "unbalanced deep left"),
    ([1,2,3,None,None,4,5],      1, "balanced with deeper right"),
]

for vals, expected, desc in tests:
    root   = make_tree(vals)
    result = isBalanced(root)
    status = "✅" if result == expected else f"❌ expected {expected}"
    print(f"{status}  {desc:40s}  → {result}")
```

---

## 🗺️ Complete Visual Summary

```
ALGORITHM: Bottom-up recursion with dual-purpose return value

height(node) returns:
  0        ← if node is None
  -1       ← if ANY node in this subtree is unbalanced (sentinel)
  height   ← if this subtree is balanced (actual positive integer)

DECISION AT EACH NODE:
  ┌─────────────────────────────────────────────────────────────┐
  │  Left  = height(node.left)                                  │
  │  if Left  == -1 → propagate -1 upward immediately          │
  │  Right = height(node.right)                                 │
  │  if Right == -1 → propagate -1 upward immediately          │
  │  if |Left - Right| > 1 → return -1 (this node unbalanced)  │
  │  else → return max(Left, Right) + 1  (all good, report H)  │
  └─────────────────────────────────────────────────────────────┘

FINAL:
  height(root) == -1  →  return 0  (unbalanced)
  height(root) >= 1   →  return 1  (balanced)

COMPLEXITY: O(N) time, O(H) space
  Each node visited once — no recomputation of heights
  -1 propagates immediately — no wasted work after finding imbalance
```

---

## 📚 What to Learn Next

| Topic | Connection |
|:------|:-----------|
| **Maximum Depth of Binary Tree** | Same height computation without balance check |
| **Diameter of Binary Tree** | Also uses bottom-up height, tracks max at each node |
| **Lowest Common Ancestor** | Bottom-up recursion returning node references |
| **AVL Tree** | Self-balancing BST that maintains balance after every insert/delete |
| **Tree DFS Patterns** | Pre-order, in-order, post-order traversals |
| **Path Sum** | Bottom-up accumulation pattern through a tree |

---

> ✍️ **The Big Idea:**
> A naive approach checks balance at every node by calling a separate height function
> for each — O(N²) total. The smart approach uses a **dual-purpose return value**:
> the `height` function returns the actual height when balanced, or `-1` as a sentinel
> when any imbalance is found. This way, height is computed and balance is checked
> in a **single bottom-up pass** — O(N). The moment `-1` is returned, it propagates
> up through all ancestor calls immediately via the two guard checks
> (`if Left == -1: return -1` and `if Right == -1: return -1`),
> short-circuiting all further computation.

---

*Happy Coding! 🚀*
