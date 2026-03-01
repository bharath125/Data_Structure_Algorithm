# 📌 Prefix Sum

## 🧠 What is Prefix Sum?

Instead of recalculating sums again and again, we **precompute** running totals and store them in a new array. Then any range sum becomes an O(1) lookup instead of O(n).

> Think of it like a **cumulative scoreboard** — you don't recount all goals, you just look at the scoreboard at two points and subtract.

---

## ✏️ Part 1 — Building a Basic Prefix Sum

### My Code
```python
arr = [2, 4, 3, 1, 5]
length = len(arr)
prefix_sum = []
res = 0

for j in range(len(arr)):
    res = res + arr[j]
    prefix_sum.append(res)

# prefix_sum = [2, 6, 9, 10, 15]
```

### What's happening step by step

| Index `j` | `arr[j]` | `res` (running total) | `prefix_sum` so far |
|-----------|----------|-----------------------|---------------------|
| 0 | 2 | 2 | [2] |
| 1 | 4 | 6 | [2, 6] |
| 2 | 3 | 9 | [2, 6, 9] |
| 3 | 1 | 10 | [2, 6, 9, 10] |
| 4 | 5 | 15 | [2, 6, 9, 10, 15] |

### Key Idea
`prefix_sum[i]` = sum of all elements from `arr[0]` up to `arr[i]`

So to get the sum of any subarray `arr[l..r]`:
```python
range_sum = prefix_sum[r] - prefix_sum[l - 1]  # O(1) — no loop needed!
```

---

## ✏️ Part 2 — Prefix Sum at Even Indexes Only

### My Code
```python
prefix_sum[0] = arr[0]

for i in range(1, length):
    if i % 2 == 0:
        prefix_sum[i] = prefix_sum[i-1] + arr[i]   # even index → add current element
    else:
        prefix_sum[i] = prefix_sum[i-1]             # odd index → carry forward, don't add

# prefix_sum = [2, 2, 5, 5, 10]
```

### What's happening step by step

| Index `i` | `i % 2 == 0`? | `arr[i]` | `prefix_sum[i-1]` | `prefix_sum[i]` |
|-----------|--------------|----------|--------------------|-----------------|
| 0 | ✅ (base case) | 2 | — | 2 |
| 1 | ❌ odd | 4 | 2 | 2 (carry) |
| 2 | ✅ even | 3 | 2 | 2 + 3 = 5 |
| 3 | ❌ odd | 1 | 5 | 5 (carry) |
| 4 | ✅ even | 5 | 5 | 5 + 5 = 10 |

### Key Idea
- Even index → **accumulate** (add current element to previous prefix)
- Odd index → **freeze** (carry forward the previous prefix, don't add)

This is a **conditional prefix sum** — the accumulation rule changes based on a condition.

---

## ⏱️ Complexity

| | Time | Space |
|-|------|-------|
| Building prefix sum | O(n) | O(n) |
| Range sum query | O(1) | O(1) |

---

## 💡 When to Use Prefix Sum

- Sum of subarray `arr[l..r]` — multiple times
- Count of elements satisfying a condition in a range
- Problems with the word **"subarray sum"** or **"range sum"**

---

## 🔑 Key Takeaways

- `res` acts as a running accumulator — no need for a nested loop
- `i % 2 == 0` is the go-to check for even indexes (remainder is zero)
- The **carry-forward** trick (`prefix_sum[i] = prefix_sum[i-1]`) is powerful — it lets you skip adding at certain positions while keeping the sum consistent
- Prefix sum trades **space for time** — you use extra memory to avoid repeated computation

---

## 🔗 Related Problems to Try
- Subarray Sum Equals K (LeetCode 560)
- Range Sum Query (LeetCode 303)
- Product of Array Except Self (LeetCode 238)
