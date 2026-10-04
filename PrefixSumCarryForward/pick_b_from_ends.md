# Maximum Sum by Removing B Elements from Either End

**Date:** 2026-10-04

## Problem

Given an integer array `A` of size `N`, perform exactly `B` operations. In each operation, remove either the leftmost or rightmost element. Return the maximum possible sum of the `B` removed elements.

### Constraints

```text
1 <= N <= 10^5
1 <= B <= N
-10^3 <= A[i] <= 10^3
```

Example:

```python
A = [5, -2, 3, 1, 2]
B = 3

answer = 8
```

---

# My Reasoning Journey

## 1. Initial idea: Prefix Sum

My first thought was:

> "Prefix sum will help here."

This was a good direction because the problem repeatedly asks for sums of elements from the left and right ends.

I initially thought prefix sum itself would be `O(N)`, so because `N <= 10^5`, I considered whether it was better not to use it.

### Important correction

Building the prefix-sum array is `O(N)`, but using it to answer a range-sum query is `O(1)`.

So an approach using prefix sums could still be `O(N)` overall if the number of queries is also `O(N)`.

However, while thinking through the problem, I found that I could avoid the prefix-sum array completely by maintaining a running sum.

---

# 2. Understanding the possible choices

For `B = 3`, there are `B + 1 = 4` possible distributions of the removed elements:

```text
0 from left + 3 from right
1 from left + 2 from right
2 from left + 1 from right
3 from left + 0 from right
```

For:

```python
A = [5, -2, 3, 1, 2]
B = 3
```

The possibilities are:

```text
0 left + 3 right → [3, 1, 2]       → 6
1 left + 2 right → [5] + [1, 2]    → 8
2 left + 1 right → [5, -2] + [2]   → 5
3 left + 0 right → [5, -2, 3]      → 6
```

Maximum = `8`.

---

# 3. Brute-force approach

I realized that the straightforward approach is to try every possible number of elements taken from the left.

For every `left_count` from `0` to `B`:

```text
right_count = B - left_count
```

Then calculate:

```text
sum(first left_count elements)
+
sum(last right_count elements)
```

and keep the maximum.

Conceptually:

```python
max_sum = -infinity

for left_count in range(B + 1):
    right_count = B - left_count

    left_sum = sum(A[:left_count])
    right_sum = sum(A[N - right_count:])

    current_sum = left_sum + right_sum
    max_sum = max(max_sum, current_sum)
```

## Why this is correct

Every valid solution must consist of:

```text
some number from the left
+
remaining number from the right
```

If we try every `left_count` from `0` through `B`, we consider every possible valid combination.

## Complexity

There are `B + 1` possibilities.

For each possibility, recalculating the sums can take `O(B)` work.

Therefore:

```text
Time = O(B²)
```

With `B` potentially equal to `100000`:

```text
O(100000²) = O(10^10)
```

That is too slow.

---

# 4. Finding the repeated work

The important observation was:

> I don't need to recalculate the whole sum for every possibility.

Consider:

```text
0 left + 3 right
[3, 1, 2]
```

Then move to:

```text
1 left + 2 right
[5] + [1, 2]
```

The `[1, 2]` part is already present in the previous selection.

Only two elements changed:

```text
3 leaves the selected set
5 enters the selected set
```

Therefore:

```text
new_sum = old_sum - element_removed_from_right + element_added_from_left
```

This eliminates the repeated sum calculation.

---

# 5. Deriving the running-sum solution

First, start with the case:

```text
0 from left + B from right
```

So:

```python
current = sum(A[-B:])
max_sum = current
```

Then gradually increase the number taken from the left.

For `B = 3`:

### Transition 1

```text
0 left + 3 right
→ 1 left + 2 right
```

```python
current = current - A[-3] + A[0]
```

### Transition 2

```text
1 left + 2 right
→ 2 left + 1 right
```

```python
current = current - A[-2] + A[1]
```

### Transition 3

```text
2 left + 1 right
→ 3 left + 0 right
```

```python
current = current - A[-1] + A[2]
```

The general transition is:

```python
current = current - A[-(B - i)] + A[i]
```

---

# 6. Final solution I derived

```python
def solve(self, A, B):
    current = sum(A[-B:])
    max_sum = current

    for i in range(B):  # B transitions after the initial case
        current = current - A[-(B - i)] + A[i]

        if current > max_sum:
            max_sum = current

    return max_sum
```

---

# 7. Why `range(B)` and not `range(B + 1)`?

There are `B + 1` possible solutions:

```text
0 left + B right
1 left + B-1 right
2 left + B-2 right
...
B left + 0 right
```

But the first case is already initialized here:

```python
current = sum(A[-B:])
```

So the loop only needs to perform the remaining `B` transitions:

```text
0 → 1 left
1 → 2 left
...
B-1 → B left
```

Therefore:

```python
range(B)
```

is correct.

---

# 8. Dry run

For:

```python
A = [5, -2, 3, 1, 2]
B = 3
```

Initial:

```text
current = sum([3, 1, 2])
        = 6
max_sum = 6
```

### i = 0

```text
current = 6 - A[-3] + A[0]
        = 6 - 3 + 5
        = 8

max_sum = 8
```

Selected elements:

```text
[5] + [1, 2]
```

### i = 1

```text
current = 8 - A[-2] + A[1]
        = 8 - 1 + (-2)
        = 5

max_sum = 8
```

Selected elements:

```text
[5, -2] + [2]
```

### i = 2

```text
current = 5 - A[-1] + A[2]
        = 5 - 2 + 3
        = 6

max_sum = 8
```

Selected elements:

```text
[5, -2, 3]
```

Final answer:

```text
8
```

---

# 9. Complexity

The initial sum:

```python
sum(A[-B:])
```

is `O(B)`.

The loop runs `B` times and performs constant work each time:

```text
O(B)
```

Therefore:

```text
Time = O(B)
```

Since:

```text
B <= N
```

the worst-case complexity can also be described as:

```text
Time = O(N)
```

For the exact Python implementation, `A[-B:]` creates a temporary slice containing `B` elements, so its temporary auxiliary space is `O(B)`.

The underlying algorithmic idea uses only constant additional state (`current` and `max_sum`), i.e. `O(1)` auxiliary space apart from the Python slice.

---

# 10. My complete reasoning flow

```text
Problem
  ↓
There are B + 1 possible left/right combinations
  ↓
Think about prefix sum
  ↓
Realize prefix sum construction is O(N), but queries can be O(1)
  ↓
Construct the brute-force approach
  ↓
Brute force checks every left/right split
  ↓
Repeatedly recalculates almost the same sums
  ↓
Ask: what changes between two consecutive splits?
  ↓
Only one right element leaves
and one left element enters
  ↓
Maintain the current sum
  ↓
O(B²) → O(B)
  ↓
Since B <= N
  ↓
O(N) worst-case
```

---

# 11. Important DSA lessons from this problem

## Lesson 1: Don't reject O(N) because N is large

`N = 10^5` is completely reasonable for an `O(N)` solution.

The real concern was `O(N²)`, not `O(N)`.

## Lesson 2: Prefix sum is preprocessing

Building prefix sum:

```text
O(N)
```

Querying a range using prefix sum:

```text
O(1)
```

These are different costs.

## Lesson 3: Look for repeated work

The brute-force solution repeatedly calculated sums that overlapped heavily.

The optimization came from asking:

> What changed from one candidate solution to the next?

## Lesson 4: Carry forward useful information

Instead of recalculating:

```text
new sum = sum of many elements
```

we used:

```text
new sum = previous sum - old element + new element
```

## Lesson 5: Understand the number of possibilities carefully

There are `B + 1` possible distributions, but if one is used as the initial state, only `B` transitions are required.

---

# 12. Questions I asked myself during the problem

- Does prefix sum help?
- What does `N <= 10^5` allow?
- How many possible left/right combinations are there?
- What would the brute-force solution look like?
- Am I recalculating the same sums repeatedly?
- What changes when I move from `0 left + B right` to `1 left + B-1 right`?
- Can I carry the previous sum forward?
- Which right element leaves the selected set?
- Which left element enters the selected set?
- Why is the loop `range(B)` instead of `range(B + 1)`?

---

# 13. Reusable problem-solving process

For future problems, I want to remember this process:

```text
1. Understand exactly what the problem allows.
2. Read the constraints.
3. Think of the obvious brute-force solution.
4. Prove that the brute-force solution covers every valid case.
5. Calculate its time and space complexity.
6. Find the bottleneck.
7. Ask what work is being repeated.
8. Look for information that can be carried forward.
9. Optimize the repeated work.
10. Re-check correctness.
11. Re-check TC and SC.
```

## Most important takeaway from this problem

> **Optimization often comes from comparing two consecutive states and asking: what actually changed?**

Here, almost the entire selected set stayed the same. Only one element was removed from the right side and one element was added from the left side.

That observation turned a repeated-sum approach into a running-sum `O(N)` solution.
