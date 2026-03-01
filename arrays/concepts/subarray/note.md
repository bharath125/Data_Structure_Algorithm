# 📌 Subarrays

## 🧠 What is a Subarray?

A subarray is a **continuous and ordered** part of an array.

```
array = [4, 1, 2, 3, -1, 6, 9, 8, 12]
```

| Slice | Is Subarray? | Why |
|-------|-------------|-----|
| `[2, 3, -1, 6]` | ✅ Yes | Continuous + same order |
| `[4, 2, 3, -1]` | ❌ No | Not continuous (skipped `1`) |
| `[3, 2, 1, 4]` | ❌ No | Continuous but reversed order |

> **Two rules to be a subarray:**
> 1. Elements must be **consecutive** (no skipping)
> 2. Elements must be in the **same order** as the original array

---

## ✏️ How Many Subarrays Start at Index `i`?

For any starting index `i`, you can keep extending the subarray until you hit the end of the array.

```
array = [4, 1, 2, 3, -1, 6, 9]   (n = 7)
```

**Subarrays starting at index 0:**
```
[4]
[4, 1]
[4, 1, 2]
[4, 1, 2, 3]
[4, 1, 2, 3, -1]
[4, 1, 2, 3, -1, 6]
[4, 1, 2, 3, -1, 6, 9]
```
That's **7 subarrays** — one for each element from index 0 to the end.

### Formula
```
subarrays starting at index i  =  n - i
```

### Table

| Starting Index `i` | Subarray Count `(n - i)` |
|--------------------|--------------------------|
| 0 | 7 (7 - 0) |
| 1 | 6 (7 - 1) |
| 2 | 5 (7 - 2) |
| 3 | 4 (7 - 3) |
| 4 | 3 (7 - 4) |
| 5 | 2 (7 - 5) |
| 6 | 1 (7 - 6) |

---

## ✏️ Total Number of Subarrays in an Array

Just add up all the rows from the table above:

```
total = n + (n-1) + (n-2) + ... + 1
      = n * (n + 1) / 2
```

For `n = 7`:
```
total = 7 * 8 / 2 = 28 subarrays
```

---

## ✏️ Print All Subarrays

### My Code
```python
arr = [1, 2, 3]
n = len(arr)

for j in range(0, n):
    for k in range(0, j + 1):
        print(arr[k], end=" ")
    print()
```

### What's happening step by step

The outer loop `j` controls **how far the subarray extends**.
The inner loop `k` **prints from index 0 up to j**.

| `j` | `k` goes from | Elements printed |
|-----|--------------|-----------------|
| 0 | 0 to 0 | `1` |
| 1 | 0 to 1 | `1 2` |
| 2 | 0 to 2 | `1 2 3` |

**Output:**
```
1
1 2
1 2 3
```

> ⚠️ Note: This code only prints subarrays **starting from index 0**.
> To print ALL subarrays (every possible start), you'd need a third outer loop for the start index.

### Print ALL subarrays (every start index)
```python
## printing subarray from 0 th index
arr = [1,2,3]
n = len(arr)

for j in range(0, n):
    for k in range(0, j+1): ## why j+1 when i=0, k can be 0 (not 0,1 as range doesn't include last index) ; i=1, k can be 0,1 ; i=2, k can be 0,1,2
        print(arr[k], end=" ") # giving space after the number eg:; 1 2
    print() ## for pring the second loop, it will take it to new line
```

**Output:**
```
1
1 2
1 2 3
2
2 3
3
```

---

## ⏱️ Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Count subarrays | O(1) using formula | O(1) |
| Print all subarrays | O(n³) — 3 nested loops | O(1) |

---

## 🔑 Key Takeaways

- A subarray must be **continuous** — no skipping elements
- A subarray must preserve **original order** — no reversing
- Subarrays starting at index `i` = `n - i`
- Total subarrays in array of size `n` = `n * (n + 1) / 2`
- `end=" "` keeps elements on the same line; `print()` moves to next line

---

## 🔗 Related Problems to Try
- Maximum Subarray (Kadane's Algorithm) — LeetCode 53
- Subarray Sum Equals K — LeetCode 560
- Longest Subarray with Sum K
