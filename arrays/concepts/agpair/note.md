# 📌 AG Pair Count

## 🧠 What is the AG Pair Problem?

Given a string, count the number of pairs `(i, j)` where:
- `string[i] == 'a'`
- `string[j] == 'g'`
- `i < j` (the `'a'` must come **before** the `'g'`)

> Example: `'acbagkagg'` → pairs are `(a,g)` at positions (0,4), (0,7), (0,8), (3,4), (3,7), (3,8), (6,7), (6,8)  = **8 pairs**

---

## ✏️ Part 1 — Brute Force Solution

### My Code
```python
string = 'acbagkagg'
length = len(string)
pair_count = 0

for i in range(length - 1):
    if string[i] == 'a':
        for j in range(i + 1, length - 1):
            if string[j] == 'g':
                pair_count += 1

print(pair_count)
```

### What's happening

For every `'a'` found at index `i`, scan everything to its right and count all `'g'`s.

| Outer `i` | `string[i]` | Is `'a'`? | Inner loop finds `'g'` at | `pair_count` |
|-----------|------------|-----------|--------------------------|--------------|
| 0 | `'a'` | ✅ | index 4, 7 | 2 |
| 4 | `'a'` | ✅ | index 7 | 3 |
| others | not `'a'` | ❌ | — | 3 |

### Problem with this approach
For every `'a'`, we loop through the rest of the string again — **loop inside a loop**.

```
⏱️ Time:  O(n²) — nested loops
💾 Space: O(1)
```

---

## ✏️ Part 2 — Optimized Solution

### My Code
```python
string = 'acbagkagg'
length = len(string)
pair_count = 0
count_a = 0

for i in range(length):
    if string[i] == 'a':
        count_a += 1
    elif string[i] == 'g':
        pair_count += count_a

print(pair_count)
```

### What's happening step by step

| Index `i` | `string[i]` | `count_a` | `pair_count` | Reason |
|-----------|------------|-----------|--------------|--------|
| 0 | `'a'` | 1 | 0 | found an `'a'`, increment count_a |
| 1 | `'c'` | 1 | 0 | neither, skip |
| 2 | `'b'` | 1 | 0 | neither, skip |
| 3 | `'a'` | 2 | 0 | found another `'a'` |
| 4 | `'g'` | 2 | 2 | found `'g'` → 2 `'a'`s came before it |
| 5 | `'k'` | 2 | 2 | neither, skip |
| 6 | `'a'` | 3 | 2 | found another `'a'` |
| 7 | `'g'` | 3 | 5 | found `'g'` → 3 `'a'`s came before it |
| 8 | `'g'` | 3 | 8 | found `'g'` → 3 `'a'`s came before it |

### Key Idea
Every time you see a `'g'`, you already know **exactly how many `'a'`s came before it** — that's just `count_a`. So instead of going back and counting, you just add `count_a` directly.

```
⏱️ Time:  O(n) — single pass
💾 Space: O(1) — just two counters
```

---

## 🔍 Brute Force vs Optimized

| | Brute Force | Optimized |
|--|-------------|-----------|
| Loops | 2 (nested) | 1 |
| Time | O(n²) | O(n) |
| Space | O(1) | O(1) |
| Idea | check every (i,j) pair | count `'a'`s on the fly |

---

## 💡 The Core Insight

> When you reach a `'g'`, every `'a'` you've seen so far forms a valid pair with it.

You don't need to look backward. `count_a` keeps a **live tally** of all usable `'a'`s, so the moment a `'g'` appears, the answer is already ready.

This pattern — **tracking a count forward and using it when a condition is met** — appears in many string problems.

---

## 🔑 Key Takeaways

- Nested loops scream O(n²) — always ask *"can I precompute something on the way?"*
- `count_a` acts like a **memory** — it remembers how many valid left-side elements exist at any point
- `elif` is important here — a character can't be both `'a'` and `'g'` at the same time
- Single pass + two counters is often the sweet spot for pair-counting problems

---

## 🔗 Related Problems to Try
- Count of pairs with given sum in array
- Number of 'b' before 'a' pairs
- LeetCode 1512 — Number of Good Pairs
