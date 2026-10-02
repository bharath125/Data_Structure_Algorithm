# Max Profit — DSA Problem Journey

> **Date:** 2026-10-02  
> **Approx. thinking time:** 2 hours 11 minutes  
> **Goal of this note:** Remember the *reasoning journey*, not just the final solution.

---

## 1. Problem

Given an array `A` where `A[i]` is the stock price on day `i`:

- I can make **at most one transaction**.
- One transaction means **buy once and sell once**.
- The buy must happen **before** the sell.
- Return the **maximum possible profit**.

### Constraints

```text
0 <= A.size() <= 700000
1 <= A[i] <= 10^7
```

### Examples

```text
A = [1, 2]
Answer = 1

A = [1, 4, 5, 2, 4]
Answer = 4
```

Profit is:

```text
selling price - buying price
```

Important: the order matters.

```text
buy day < sell day
```

---

# 2. Initial Understanding

At first I did not fully understand the wording of the problem.

After breaking it down, I understood it as:

> Find a buying day and a later selling day that produce the maximum profit.

The important condition is:

```text
BUY first → SELL later
```

This became important later because simply finding the minimum and maximum values is not enough.

---

# 3. Attempt 1 — Find the Global Maximum and Minimum

My first approach was:

1. Find the maximum element and its index.
2. Find the minimum element and its index.
3. Check whether the minimum happened before the maximum.
4. If yes, calculate:

```text
max_price - min_price
```

5. Otherwise return `0`.

### My initial complexity calculation

I had two separate loops:

```text
First loop  → O(n)
Second loop → O(n)
```

Therefore:

```text
O(n + n)
= O(2n)
= O(n)
```

Space:

```text
O(1)
```

### The problem with this approach

I discovered that the **global minimum and global maximum do not necessarily form a valid or optimal transaction** because their order matters.

Example:

```text
A = [7, 1, 5, 3, 6, 4]
```

Global maximum:

```text
7
```

Global minimum:

```text
1
```

But `7` appears before `1`, so I cannot buy at `1` and sell at `7`.

There is still a valid profitable transaction:

```text
1 → 6 = 5
```

### Lesson

> **When a problem has an ordering constraint, independently finding minimum and maximum values may not be enough.**

---

# 4. Attempt 2 — Brute Force: Check Every Buy/Sell Pair

I then changed the approach.

Instead of finding one global minimum and maximum, I decided:

> For every possible buying day, check every possible selling day after it.

Conceptually:

```text
for i = 0 ... n-1:
    buy at A[i]

    for j = i+1 ... n-1:
        sell at A[j]

        profit = A[j] - A[i]

        update max_profit
```

My reasoning was:

> `O(n²)` checks every possible buy/sell scenario. Since the buy happens before the sell (`j > i`), every valid transaction is considered. Because `max_profit` is updated whenever a larger profit is found, the final value must be the maximum possible profit.

### Why this approach is correct

For every pair:

```text
i = buying day
j = selling day
```

I only consider:

```text
j > i
```

Therefore, buying always happens before selling.

Since every valid pair is considered, the maximum of all calculated profits must be the answer.

### Complexity

Outer loop:

```text
O(n)
```

Inner loop:

```text
O(n)
```

Therefore:

```text
Time = O(n²)
Space = O(1)
```

---

# 5. Constraint Check — Why O(n²) Is a Problem

The constraint is:

```text
A.size() <= 700000
```

For an `O(n²)` solution, the worst case is approximately:

```text
700000 × 700000
= 490,000,000,000
```

That is roughly **490 billion** pair checks.

So although the brute-force solution is correct, it is not practical for the maximum input size.

This told me:

> I need to find a way to avoid the nested loop.

---

# 6. Finding the Repeated Work

I asked myself:

> **What am I repeatedly doing in the nested loop?**

For example:

```text
A = [7, 1, 5, 3, 6, 4]
```

If I buy at `1`, I calculate:

```text
5 - 1 = 4
3 - 1 = 2
6 - 1 = 5
4 - 1 = 3
```

I realized I was repeatedly examining future prices for every possible buying price.

This led to the next question:

> **Can I remove the inner loop by carrying some useful information forward?**

That was the main turning point.

---

# 7. Failed Optimization Idea — Carry Only Previous Price

My first attempt to remove the inner loop was:

```text
max_profit = 0
previous_price = 0

for every day:
    compare current price with previous price
```

In other words, calculate:

```text
current price - yesterday's price
```

For:

```text
A = [7, 1, 5, 3, 6, 4]
```

This gives:

```text
7 → 1 = -6
1 → 5 = 4
5 → 3 = -2
3 → 6 = 3
6 → 4 = -2
```

Maximum = `4`.

But the real best transaction is:

```text
1 → 6 = 5
```

### Lesson

> **The previous element is not necessarily the useful information I need.**

I needed something more meaningful from the previous days.

---

# 8. Key Question — What Information Do I Need From the Past?

I asked:

> If today's price is the selling price, what do I need to remember from previous days?

Example:

```text
A = [7, 1, 5, 3, 6, 4]
```

When I reach `6`, the previous prices are:

```text
7, 1, 5, 3
```

I do **not** need all four values.

I only need the useful information:

```text
1
```

because `1` is the **cheapest buying price seen so far**.

Then I can calculate:

```text
6 - 1 = 5
```

This was the key insight.

---

# 9. Final Optimized Approach

Maintain two pieces of information while moving through the array once:

### `cheapest_price`

The cheapest price seen so far.

### `max_profit`

The maximum profit found so far.

For every current price:

1. If today's price is cheaper than `cheapest_price`, update `cheapest_price`.
2. Calculate the profit from selling today:

```text
current_price - cheapest_price
```

3. If this profit is larger than `max_profit`, update `max_profit`.

This removes the need for the nested loop.

---

# 10. My Final Code

```python
def maxProfit(self, A):
    max_profit = 0
    cheapest_price = 0

    for i in range(len(A)):
        if i == 0:
            cheapest_price = A[i]
            continue

        if A[i] < cheapest_price:
            cheapest_price = A[i]

        res = A[i] - cheapest_price

        if res > max_profit:
            max_profit = res

    return max_profit
```

---

# 11. Dry Run

For:

```text
A = [7, 1, 5, 3, 6, 4]
```

| Day | Current Price | Cheapest Price So Far | Profit If Sold Today | Max Profit |
|---:|---:|---:|---:|---:|
| 0 | 7 | 7 | — | 0 |
| 1 | 1 | 1 | 0 | 0 |
| 2 | 5 | 1 | 4 | 4 |
| 3 | 3 | 1 | 2 | 4 |
| 4 | 6 | 1 | 5 | 5 |
| 5 | 4 | 1 | 3 | 5 |

Final answer:

```text
5
```

Transaction:

```text
Buy at 1
Sell at 6
Profit = 5
```

---

# 12. Complexity of Final Solution

Only one loop is needed.

### Time Complexity

```text
O(n)
```

### Space Complexity

```text
O(1)
```

Only a few variables are maintained:

```text
cheapest_price
max_profit
res
```

No additional array or data structure is required.

---

# 13. Complete Reasoning Journey

```text
Understand the problem
        ↓
Find global minimum + maximum
        ↓
❌ Ordering problem
        ↓
Check every valid buy/sell pair
        ↓
✅ Correct but O(n²)
        ↓
Constraint says n <= 700,000
        ↓
O(n²) is too expensive
        ↓
Ask: "What work am I repeating?"
        ↓
Try to remove the inner loop
        ↓
Carry previous price
        ↓
❌ Previous price is not enough
        ↓
Ask: "What information from the past do I actually need?"
        ↓
Cheapest price seen so far
        ↓
Compare current price against cheapest price
        ↓
Update max profit
        ↓
✅ O(n) time
✅ O(1) space
```

---

# 14. Important DSA Lessons From This Problem

## Lesson 1 — Ordering constraints matter

Don't blindly find:

```text
minimum + maximum
```

when the problem says:

```text
buy before sell
```

The positions of the values matter.

---

## Lesson 2 — Brute force is useful

The `O(n²)` solution was not wasted effort.

It gave me a correctness baseline:

> If I check every valid pair, I know I have considered every possible transaction.

Then I could focus on optimizing it.

---

## Lesson 3 — Look for repeated work

The important question was:

> **What am I repeatedly calculating or searching for?**

That question helped me identify the nested-loop bottleneck.

---

## Lesson 4 — Carry forward useful information

Instead of repeatedly searching previous/future elements, maintain information that summarizes what I need.

Here:

```text
cheapest price seen so far
```

This is a useful general DSA technique.

---

## Lesson 5 — Previous value vs useful history

I first thought:

```text
previous_price
```

would be enough.

It wasn't.

The useful information was:

```text
cheapest_price_so_far
```

This distinction is important:

> The immediately previous value is not always the information needed from the past.

---

## Lesson 6 — Constraints should influence algorithm choice

The constraint:

```text
n <= 700000
```

should make me suspicious of:

```text
O(n²)
```

and push me to investigate:

```text
O(n)
O(n log n)
```

or another scalable approach.

---

# 15. Questions I Asked Myself During the Problem

These questions were important because they moved my thinking forward:

### Q1
> Can I simply find the minimum and maximum?

No — ordering matters.

### Q2
> How can I guarantee correctness?

Check every valid buy/sell pair.

### Q3
> Why is that too slow?

Because it is `O(n²)` and `n` can be `700,000`.

### Q4
> What am I repeating?

Searching through future prices for every possible buying day.

### Q5
> Can I remove the inner loop by carrying something forward?

Yes.

### Q6
> Is the previous price enough?

No.

### Q7
> What information from previous days is actually useful?

The cheapest buying price seen so far.

### Q8
> What do I compare today's price with?

The cheapest price seen before/today.

### Q9
> What do I keep globally?

The maximum profit found so far.

---

# 16. Personal Record — 2026-10-02

**Problem:** Maximum Profit With At Most One Stock Transaction

**Approx. thinking time:** ~2 hours 11 minutes

**Starting point:** I initially didn't fully understand the question.

**First approach:** Global minimum + global maximum.

**First mistake:** Minimum and maximum can occur in the wrong order.

**Second approach:** Check every possible valid buy/sell pair.

**Second approach correctness:** ✅

**Second approach complexity:** `O(n²)`

**Optimization question:** What work am I repeating?

**First optimization attempt:** Previous price.

**Why it failed:** It only considers buying yesterday and selling today.

**Key insight:** Carry the cheapest price seen so far.

**Final solution:** One pass through the array.

**Final complexity:** `O(n)` time, `O(1)` space.

---

# 17. Most Important Takeaway

> **I did not memorize the optimized solution. I reached it by starting with brute force, proving why brute force was correct, identifying the repeated work, and asking what information I could carry forward to remove that repetition.**

When I face another DSA problem, I should remember this process:

```text
Understand
   ↓
Brute force
   ↓
Prove correctness
   ↓
Check constraints
   ↓
Find bottleneck / repeated work
   ↓
Ask what information can be maintained
   ↓
Optimize
   ↓
Re-check correctness
   ↓
Re-check TC + SC
```
