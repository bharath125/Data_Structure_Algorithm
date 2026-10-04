# Leaders in an Array

## Problem

Given an array `A` of `N` distinct integers, an element is a **leader** if it is strictly greater than every element to its right.

The rightmost element is always a leader.

Example:

```text
A = [16, 17, 4, 3, 5, 2]

Leaders = [17, 5, 2]
```

The problem allows the leaders to be returned in any order.

## Constraints

```text
1 <= N <= 100000
1 <= A[i] <= 100000000
```

Because `N` can be `100000`, an `O(N^2)` solution is too slow.

---

# My Problem-Solving Journey

## 1. Brute Force

My first idea was:

> For every element `A[i]`, check every element to its right. If `A[i]` is greater than all of them, add it to the leaders array.

Conceptually:

```python
for i in range(len(A)):
    for j in range(i + 1, len(A)):
        # check A[i] against A[j]
```

The important part is **all** elements.

For example:

```text
A = [5, 3, 7]
```

For `5`:

```text
5 > 3  -> True
5 > 7  -> False
```

Therefore `5` is not a leader.

A correct brute-force implementation is:

```python
def solve(self, A):
    leaders = []

    for i in range(len(A)):
        is_leader = True

        for j in range(i + 1, len(A)):
            if A[i] <= A[j]:
                is_leader = False
                break

        if is_leader:
            leaders.append(A[i])

    return leaders
```

### Complexity

```text
Time: O(N^2)
Space: O(K)
```

`K` is the number of leaders returned.

With `N = 100000`, `O(N^2)` is not acceptable.

---

## 2. Identify the Repeated Work

For every `A[i]`, I don't actually care about every individual element on the right.

I only need to know:

> **What is the maximum value on the right?**

So the logic can be expressed as:

```python
if A[i] > max(A[i + 1:]):
    # A[i] is a leader
```

This is logically correct.

But:

```python
max(A[i + 1:])
```

itself takes `O(N)` in the worst case.

If that happens inside an `O(N)` loop:

```text
O(N) × O(N) = O(N^2)
```

So I have not really removed the repeated work.

---

## 3. Key Insight

The next question was:

> Can I calculate the maximum once and maintain it instead of recalculating it?

Consider:

```text
A = [16, 17, 4, 3, 5, 2]
```

If I process from the right:

```text
2
```

is automatically a leader.

Then:

```text
5 > 2
```

so `5` is a leader.

Now the maximum seen on the right is `5`.

For `3`:

```text
3 > 5 -> False
```

For `4`:

```text
4 > 5 -> False
```

For `17`:

```text
17 > 5 -> True
```

Now the maximum becomes `17`.

For `16`:

```text
16 > 17 -> False
```

The important realization is:

> **The maximum of the right side can be maintained while traversing instead of recalculated for every element.**

Processing right-to-left makes this possible because the elements already processed are exactly the elements to the current element's right.

---

## 4. Final Optimized Solution

```python
def solve(self, A):
    leaders = []

    max_right = A[-1]
    leaders.append(max_right)

    for i in range(len(A) - 2, -1, -1):
        if A[i] > max_right:
            leaders.append(A[i])
            max_right = A[i]

    return leaders
```

For:

```text
A = [16, 17, 4, 3, 5, 2]
```

the result is:

```text
[2, 5, 17]
```

This is valid because the problem allows any order.

---

## 5. Complexity

Every element is visited exactly once.

```text
Time Complexity: O(N)
```

The algorithm maintains only `max_right` apart from the required output:

```text
Auxiliary Space: O(1)
Output Space:    O(K)
```

where `K` is the number of leaders.

---

# 6. My Problem-Solving Lesson

The important lesson is not simply:

> "Traverse from right to left."

The reasoning was:

```text
Brute force
    ↓
For every A[i], scan everything to the right
    ↓
Repeated work
    ↓
What information do I actually need from the right?
    ↓
Only the maximum value
    ↓
Can I maintain that maximum?
    ↓
Yes
    ↓
Process from right to left
    ↓
O(N)
```

This is a reusable DSA pattern:

> **When a brute-force solution repeatedly calculates some property of a previous or next portion of an array, ask whether that property can be maintained incrementally.**

---

# 7. Independent-Solve Assessment

Initially, I received a hint to think about processing from the right, so I should **not** count the first implementation as a completely independent solve.

After restarting the reasoning, I independently identified:

1. The right side only needs to be represented by its maximum.
2. `max(A[i + 1:])` repeated inside a loop is still `O(N^2)`.
3. The maximum can be carried forward instead of recalculated.
4. Right-to-left traversal makes the already-processed values exactly the values to the current element's right.

That is the important problem-solving insight.

---

# 8. Reusable Checklist

For similar array problems, ask:

```text
1. What does the brute force repeatedly calculate?
2. Am I scanning the same elements multiple times?
3. Can I summarize those elements with one value?
4. Can I maintain that value as I traverse?
5. Which traversal direction makes the needed information already available?
6. Can I reduce O(N^2) to O(N)?
```

For this problem:

```text
Repeated calculation → maximum on the right
Summary              → max_right
Traversal            → right to left
Time                 → O(N)
```
