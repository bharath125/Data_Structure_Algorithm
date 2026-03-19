## Binary Search


## 📖 Table of Contents
1. [Why Binary Search is called "Binary"](#why-binary-search)

---

## Why Binary Search is called "Binary"

"Binary" comes from Latin *binarius* — **"consisting of two."**

At every single step, binary search makes **one decision that splits the world into exactly two halves** — left half or right half. Always exactly **two** choices. That two-way split, repeated over and over, *is* the algorithm. Hence the name.

### Why O(log N)?

Every step cuts the problem **in half**. Not by one, not by a fixed number — by *half*.

```
16 elements → 8 → 4 → 2 → 1    (4 steps = log₂(16))
```

> **The math:** "How many times can I divide N by 2 before reaching 1?" = **log₂(N)**

| Array Size (N) | Linear Search (worst) | Binary Search (worst) |
|---|---|---|
| 10 | 10 steps | 4 steps |
| 100 | 100 steps | 7 steps |
| 1,000 | 1,000 steps | 10 steps |
| 1,000,000 | 1,000,000 steps | 20 steps |
| 1,000,000,000 | 1,000,000,000 steps | **30 steps** |

> ⚠️ **Key requirement:** Binary search only works on a **sorted** array.

---
