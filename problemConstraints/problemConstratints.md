# 🧠 DSA Constraints Cheat Sheet
> **The #1 skill in competitive programming:** Look at N → know your complexity → pick the algorithm. This guide teaches you exactly that.

---

## 📖 Table of Contents
1. [Why Binary Search is called "Binary"](#why-binary-search)
2. [The 10⁸ Rule — Your Golden Budget](#the-10⁸-rule)
3. [The Golden Table — N → Complexity → Algorithm](#the-golden-table)
4. [The Complete Cheat Card](#the-complete-cheat-card)
5. [Magic Phrases → Instant Algorithm Signals](#magic-phrases)
6. [Problem Patterns Deep Dive](#problem-patterns-deep-dive)
7. [The Mental Process for Any Problem](#the-mental-process)

---

## The 10⁸ Rule

```
~10⁸ (100,000,000) simple operations per second
```

This is your budget on any competitive programming judge. If your algorithm does **more than 10⁸ ops** for the given N, it will **TLE (Time Limit Exceeded)**.

**Examples:**
- ✅ N = 10⁵, O(N log N) → ~1,700,000 ops → **Safe**
- ✅ N = 10⁶, O(N) → 1,000,000 ops → **Safe**
- ❌ N = 10⁵, O(N²) → 10,000,000,000 ops → **TLE**
- ❌ N = 10⁶, O(N²) → 10¹² ops → **TLE**

---

## The Golden Table

> Memorize this. It is the entire game.

| N (constraint) | Max Complexity | Approx Ops | Loops Needed | Algorithms / Patterns |
|---|---|---|---|---|
| N ≤ 10–12 | O(N!) | ~3.6M | Brute force | All permutations, backtracking |
| N ≤ 20 | O(2ᴺ) | ~1M | Bitmask / recursion | Bitmask DP, subsets, meet in middle |
| N ≤ 100 | O(N³) | ~1M | 3 nested loops | Floyd-Warshall, 3-state DP |
| N ≤ 1,000 | O(N²) | ~1M | 2 nested loops | Bubble sort, 2D DP, brute pairs |
| N ≤ 10⁵ | O(N log N) | ~1.7M | 1 loop + log step | Merge sort, binary search, seg tree, heap, BFS/DFS |
| N ≤ 10⁶ | O(N) | ~1M | 1 single pass | Two pointers, sliding window, hashing, stack, Kadane |
| N ≤ 10⁹ | O(log N) | ~30 | No loops at all | Binary search on answer, fast expo, GCD/math |
| N ≤ 10¹⁸ | O(1) or O(√N) | ~1 | Formula only | Direct formula, prime factors, pure math |

---

## The Complete Cheat Card

```
N ≤ 10–12   →  O(N!)       →  brute force          →  Try everything, all permutations
N ≤ 20      →  O(2ᴺ)      →  bitmask trick        →  Enumerate all subsets
N ≤ 400     →  O(N³)       →  3 nested loops       →  Triple DP, Floyd-Warshall
N ≤ 5,000   →  O(N²)       →  2 nested loops       →  Double DP, brute pairs
N ≤ 10⁵    →  O(N log N)  →  1 loop + log step    →  Sort, binary search, segment tree
N ≤ 10⁶    →  O(N)        →  1 single pass        →  Two pointers, sliding window, hash
N ≤ 10⁸    →  O(N) careful→  ultra-lean 1 pass    →  Only simplest ops, no log allowed
N ≤ 10⁹    →  O(log N)    →  NO loops at all      →  Binary search on answer, math
N ≤ 10¹⁸  →  O(1)/O(√N)  →  formula only         →  Closed-form math, prime factors
```

---

## Magic Phrases

> Scan the problem statement for these words. They are **secret signals** that point directly to an algorithm — before you even fully understand the problem.

| If you see this phrase... | Your brain should fire... |
|---|---|
| `"sorted array"` / `"non-decreasing"` | **Binary search** |
| `"subarray"` / `"substring"` / `"contiguous"` | **Sliding window / Kadane** |
| `"all permutations"` / `"arrangements"` | **Backtracking — O(N!)** |
| `"minimum moves"` / `"minimum steps"` | **BFS** (never DFS for shortest path!) |
| `"number of ways"` / `"count paths"` | **Dynamic Programming** |
| `"maximum value"` / `"minimum cost"` | **DP or binary search on answer** |
| `N ≤ 20` in constraints | **Bitmask DP** |
| `"graph"` / `"connected"` / `"components"` | **BFS / DFS / Union-Find** |
| `"K closest"` / `"K largest"` / `"K smallest"` | **Heap / Priority queue** |
| `"range queries"` / `"update and query"` | **Segment tree / BIT (Fenwick tree)** |
| `"find minimum X such that..."` | **Binary search on the answer** |
| `"choose K items"` / `"subset sum"` | **Knapsack DP** |
| `"cycle"` / `"detect loop"` | **Floyd's algorithm / DFS with color** |
| `"intervals"` / `"overlapping"` | **Sorting by start/end + greedy** |
| `"palindrome"` | **Two pointers / DP** |

---

## Problem Patterns Deep Dive

### Pattern 1 — Sorted Array → Binary Search

**Keywords:** `sorted`, `non-decreasing`, `strictly increasing`

**Why:** A sorted array guarantees "everything left is smaller, everything right is larger." This lets you eliminate half the search space in one comparison.

**Complexity:** O(log N)

```cpp
// Find target in sorted array
int lo = 0, hi = n - 1;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;  // avoids integer overflow
    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) lo = mid + 1;  // go right
    else hi = mid - 1;                          // go left
}
return -1; // not found
```

> 🔑 **Trick:** The word `"sorted"` is basically a flashing sign that says USE BINARY SEARCH.

---

### Pattern 2 — Subarray / Substring → Sliding Window

**Keywords:** `subarray`, `substring`, `contiguous`, `consecutive`, `window`

**Why:** You don't need to recompute from scratch. Slide a window: expand the right pointer, shrink the left pointer. One pass = O(N).

**Complexity:** O(N)

```cpp
// Maximum sum subarray — Kadane's Algorithm
int maxSum = arr[0], cur = arr[0];
for (int i = 1; i < n; i++) {
    cur = max(arr[i], cur + arr[i]);   // extend or restart
    maxSum = max(maxSum, cur);
}

// Longest subarray with sum ≤ K — Sliding window
int lo = 0, sum = 0, maxLen = 0;
for (int hi = 0; hi < n; hi++) {
    sum += arr[hi];
    while (sum > K) sum -= arr[lo++];  // shrink left
    maxLen = max(maxLen, hi - lo + 1);
}
```

---

### Pattern 3 — All Subsets / Choose K → Bitmask or DP

**Keywords:** `all subsets`, `every combination`, `choose k`, `subset sum`, `powerset`

**When N ≤ 20:** Enumerate all 2ᴺ subsets using bitmasks. Each bit = "is item i included?"

**Complexity:** O(2ᴺ) for bitmask, O(N × amount) for knapsack DP

```cpp
// Enumerate all 2^N subsets — bitmask
for (int mask = 0; mask < (1 << n); mask++) {
    for (int i = 0; i < n; i++) {
        if (mask & (1 << i)) {
            // item i is included in this subset
        }
    }
}

// Subset sum / Knapsack DP — when N is larger
// dp[i] = true if sum i is achievable
vector<bool> dp(target + 1, false);
dp[0] = true;
for (int num : nums)
    for (int j = target; j >= num; j--)
        dp[j] = dp[j] || dp[j - num];
```

> 🔑 **Trick:** If N > 20 and you see "choose K", switch to DP — not bitmask brute force.

---

### Pattern 4 — Shortest Path / Minimum Steps → BFS

**Keywords:** `shortest path`, `minimum steps`, `minimum moves`, `minimum cost`, `reachable`

**Why:** BFS explores nodes level by level. Each level = one step. So the first time you reach a node, it's guaranteed to be the shortest path.

**Complexity:** O(V + E)

```cpp
// BFS shortest path
queue<int> q;
vector<int> dist(n, -1);
q.push(start);
dist[start] = 0;

while (!q.empty()) {
    int u = q.front(); q.pop();
    for (auto v : adj[u]) {
        if (dist[v] == -1) {
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }
}
```

> ⚠️ **Never use DFS for shortest path.** DFS does not guarantee the shortest route. BFS always does (for unweighted graphs).

---

### Pattern 5 — Optimization / Counting → Dynamic Programming

**Keywords:** `minimum cost`, `maximum profit`, `number of ways`, `fewest operations`, `can we achieve exactly X`

**Why:** DP avoids recomputing subproblems. Ask: "Can the answer to a big problem be built from answers to smaller problems?" If yes → DP.

**Complexity:** Depends on states × transitions

```cpp
// Coin change — minimum coins to make amount
// dp[i] = minimum coins to make sum i
vector<int> dp(amount + 1, INT_MAX);
dp[0] = 0;
for (int i = 1; i <= amount; i++) {
    for (int coin : coins) {
        if (coin <= i && dp[i - coin] != INT_MAX) {
            dp[i] = min(dp[i], dp[i - coin] + 1);
        }
    }
}

// Longest Common Subsequence — classic 2D DP
// dp[i][j] = LCS of first i chars of s1 and first j chars of s2
for (int i = 1; i <= m; i++)
    for (int j = 1; j <= n; j++)
        dp[i][j] = (s1[i-1] == s2[j-1])
            ? dp[i-1][j-1] + 1
            : max(dp[i-1][j], dp[i][j-1]);
```

---

### Pattern 6 — Huge N + "Find Minimum X" → Binary Search on Answer

**Keywords:** `N ≤ 10⁹`, `find minimum`, `find maximum possible`, `smallest X that satisfies`, `at least`, `at most`

**Why:** When N is massive and you're asked for the minimum/maximum value satisfying a condition, binary search *on the answer* — not on the array. Write an `isFeasible(X)` check, run it O(log N) times.

**Complexity:** O(N log(max_value)) total

```cpp
// Binary search on the answer
bool isFeasible(int mid, /* other params */) {
    // Check: "Is it possible to achieve mid?"
    // This function runs in O(N) or O(N log N)
    return /* true or false */;
}

int lo = 1, hi = 1e9, ans = -1;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (isFeasible(mid)) {
        ans = mid;
        hi = mid - 1;  // look for smaller (minimize)
    } else {
        lo = mid + 1;
    }
}
```

> 🔑 **The magic phrase:** *"Is it possible to achieve X?"* — If you can answer that in O(N), wrap it in binary search for O(N log N) total.

---

## The Mental Process

Follow these steps for **every** problem you encounter:

```
Step 1 → Find N in the constraints
Step 2 → Use the Golden Table: N → max allowed complexity
Step 3 → Scan the problem for Magic Phrases
Step 4 → Match phrase → algorithm family
Step 5 → Verify: ops count < 10⁸ for the given N?
Step 6 → Code it up
```

### Quick Decision Tree

```
Read constraints
      │
      ├── N ≤ 20?          → Bitmask DP / try all subsets
      ├── N ≤ 1000?        → O(N²) is fine, think 2D DP
      ├── N ≤ 10⁵?         → Need O(N log N): sort + binary search
      ├── N ≤ 10⁶?         → Must be O(N): sliding window / hash
      └── N ≤ 10⁹?         → O(log N) only: binary search on answer

Read problem words
      │
      ├── "sorted"         → Binary search
      ├── "subarray"       → Sliding window / Kadane
      ├── "min steps"      → BFS
      ├── "ways / count"   → DP
      ├── "max/min value"  → DP or binary search on answer
      └── "graph/connected"→ BFS / DFS / Union-Find
```

---

## Summary — The One-Liner Rule

> **"The constraint gives you the complexity. The words give you the algorithm. The 10⁸ rule confirms your choice."**

---

*Made for quick revision. Bookmark it, fork it, come back whenever you need it.* 🚀
