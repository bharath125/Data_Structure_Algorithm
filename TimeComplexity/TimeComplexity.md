<div align="center">

# 📘 DSA Notes — Learning Journey

**Handwritten class notes → clean, revisable GitHub notes**

![Topic](https://img.shields.io/badge/Topic-Time%20Complexity-blue)
![Language](https://img.shields.io/badge/Code-Python%20%7C%20Pseudocode-yellow)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange)

</div>

---

## 📑 Table of Contents

1. [⏱️ Time Complexity](#️-time-complexity)
2. [🔍 Power of Observation + Time & Space Complexity](#-power-of-observation--time--space-complexity)
   - [Problem: Count the Factors of a Number](#-problem-count-the-factors-of-a-number)
   - [Approach 1: Brute Force](#-approach-1-brute-force)
   - [Why We Can't Measure "Execution Time"](#-why-we-cant-measure-execution-time)
   - [The 10⁸ Iterations Rule](#-the-10-iterations-rule)
   - [Approach 2: Optimization Using Observation](#-approach-2-optimization-using-observation)
   - [Optimized Code (and the Perfect Square Trap)](#-optimized-code-and-the-perfect-square-trap)
   - [`i * i <= n` vs `i <= sqrt(n)`](#-i--i--n-vs-i--sqrtn)
   - [My Python Code](#-my-python-code)
   - [Quick Revision Summary](#-quick-revision-summary)
3. [🧮 Arrays and Manipulation](#-arrays-and-manipulation)
4. [📸 Original Notebook Pages](#-original-notebook-pages)

---

## ⏱️ Time Complexity

> [!NOTE]
> Time complexity tells us **how the number of steps (iterations) grows as the input `n` grows**, not how many seconds a program takes.
> The notes below build this idea step by step using one problem: **counting factors**.

---

## 🔍 Power of Observation + Time & Space Complexity

### 🎯 Problem: Count the Factors of a Number

> **Given a number `n`, find the number of factors of `n`.**

A number `i` is a **factor** of `n` if it divides `n` completely:

```
n % i == 0   →   i is a factor of n
```

#### Examples

| `n` | Check every number from 1 to n | Factors | Count |
|:---:|:---|:---|:---:|
| **10** | `10 % 1 = 0` ✅, `10 % 2 = 0` ✅, 3 ❌, 4 ❌, 5 ✅, 6 ❌, 7 ❌, 8 ❌, 9 ❌, 10 ✅ | 1, 2, 5, 10 | **4** |
| **24** | Keep only the ones that divide 24 | 1, 2, 3, 4, 6, 8, 12, 24 | **8** |

---

### 🐢 Approach 1: Brute Force

**Idea:** Try every number from `1` to `n`. If it divides `n`, count it.

#### Pseudocode (as taught in class)

```c
int countFactors(int n) {
    int c = 0;
    for (i = 1; i <= n; i++) {
        if (n % i == 0) {
            c++;
        }
    }
    return c;
}
```

#### Python version

```python
def count_factors(n):
    c = 0
    for i in range(1, n + 1):
        if n % i == 0:
            c += 1
    return c
```

> [!IMPORTANT]
> **Number of iterations = `n`**
> The loop runs once for every number from 1 to n.

---

### 🌋 Why We Can't Measure "Execution Time"

**Execution time?** ➜ We **cannot** give an exact time, because **it depends on the environment and system**.

> [!TIP]
> **Instructor's real-world example 🌋🏔️**
>
> | Where the person (computer) is | Condition | Result |
> |:---|:---|:---|
> | 🌋 On a **volcano** | It is **hot** | **Slow** execution |
> | 🏔️ On **Mount Everest** | It is **cold** | **Fast** execution |
>
> The *same code* can take different time on different machines and conditions.
> So instead of **seconds**, we count **iterations**, which stay the same everywhere.

---

### ⚡ The 10⁸ Iterations Rule

> **Assumption:** $10^8$ iterations are executed in **1 second**.

| `n` | Number of iterations | Execution time |
|:---:|:---:|:---|
| $10^8$ | $10^8$ | **1 sec** |
| $10^9$ | $10^9$ | $\frac{10^9}{10^8}$ = **10 sec** |
| $10^{18}$ | $10^{18}$ | $\frac{10^{18}}{10^8} = 10^{10}$ sec ≈ **317 years** 😱 |

#### How the calculation works

```
10⁸ iterations  →  1 sec
1 iteration     →  1/10⁸ sec
10⁹ iterations  →  10⁹/10⁸  = 10 sec
10¹⁸ iterations →  10¹⁸/10⁸ = 10¹⁰ sec  ≈ 317 years
```

> [!TIP]
> **Instructor's real-world example 👨‍👩‍👧‍👦**
> 317 years is so long that the answer would only reach your **5th generation**!
>
> ```mermaid
> flowchart LR
>     A[👤 You] --> B[👶 Children] --> C[🧒 Grandchildren] --> D[4th generation] --> E[5th generation gets the answer 🎉]
> ```
>
> **Lesson:** For big inputs, the brute force `O(n)` approach is far too slow. We must optimize.

---

### 🔍 Approach 2: Optimization Using Observation

**Key observation:** Factors always come in **pairs**.

$$i \times j = n \quad \text{(i and j are both factors of n)}$$

$$j = \frac{n}{i} \quad \text{(so i and } \tfrac{n}{i} \text{ are both factors of n)}$$

#### Example: `n = 24`

| `i` | `n / i` | |
|:---:|:---:|:---|
| 1 | 24/1 = **24** | ⬅️ **Part 1** |
| 2 | 24/2 = **12** | ⬅️ **Part 1** |
| 3 | 24/3 = **8** | ⬅️ **Part 1** |
| 4 | 24/4 = **6** | ⬅️ **Part 1** |
| 6 | 24/6 = **4** | 🔁 Part 2 (repeat) |
| 8 | 24/8 = **3** | 🔁 Part 2 (repeat) |
| 12 | 24/12 = **2** | 🔁 Part 2 (repeat) |
| 24 | 24/24 = **1** | 🔁 Part 2 (repeat) |

> [!IMPORTANT]
> **Part 1 already has all the answers!** Part 2 is just the same pairs flipped.
>
> Part 1 is where `i <= n/i`, so:
>
> $$i \le \frac{n}{i} \;\Rightarrow\; i^2 \le n \;\Rightarrow\; i \le \sqrt{n}$$
>
> 👉 We only need to loop **up to √n**, and count **2 factors** (`i` and `n/i`) each time.

---

### 🚀 Optimized Code (and the Perfect Square Trap)

Loop condition: `i <= sqrt(n)` **or** `i * i <= n`

#### ❌ First attempt (wrong)

```c
int countFactorsOptimised(int n) {
    count = 0;
    for (i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            count += 2;
        }
    }
    return count;
}
```

> [!WARNING]
> **This is wrong for perfect squares!**
> For `n = 100`, when `i = 10` we get `n / i = 10`, which is the **same number**.
> Adding 2 counts `10` **twice**.

#### Example: `n = 100`

| `i` | `n / i` | |
|:---:|:---:|:---|
| 1 | 100/1 = 100 | |
| 2 | 100/2 = 50 | |
| 5 | 100/5 = 20 | |
| **10** | **100/10 = 10** | ⭕ **`i == n/i` → count only once!** |
| 20 | 100/20 = 5 | |
| 50 | 100/50 = 2 | |
| 100 | 100/100 = 1 | |

> [!NOTE]
> *Added while making these notes:* the full factor list of 100 also includes **4** and **25** (`100/4 = 25`).
> Complete list: 1, 2, 4, 5, 10, 20, 25, 50, 100 → **9 factors**.

#### ✅ Correct optimized code

```c
int countFactorsOptimised(int n) {
    count = 0;
    for (i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            if (i == n / i) {
                count += 1;     // perfect square: i and n/i are the same
            } else {
                count += 2;     // i and n/i are two different factors
            }
        }
    }
    return count;
}
```

**Iterations:** only **√n**, so the time complexity is **O(√n)**.

---

### ⚖️ `i * i <= n` vs `i <= sqrt(n)`

| Loop condition | What happens | Complexity | Verdict |
|:---|:---|:---:|:---|
| `i * i <= n` | `2×2`, `3×3` are simple multiplications (constant work), no extra calculation needed | O(√n) | ⚡ **Fast** |
| `i <= sqrt(n)` inside the loop | `sqrt(n)` is recalculated **at every iteration** (≈ `log n` work each time) | O(√n) | 🐌 More expensive |
| `limit = sqrt(n)` computed **once**, then `i <= limit` | Square root is calculated only one time | O(√n) | 👍 Very good |

> [!TIP]
> In terms of speed, **`i * i <= n` is the faster choice.**

---

### 🐍 My Python Code

This is the version I wrote in the Python compiler, **with one fix**:

```python
n = 100
i = 1
count = 0
while i * i <= n:
    if n % i == 0:
        if i == n // i:      # ✅ fixed: was  i == n % i
            count += 1
        else:
            count += 2
    i += 1
print(count)   # 9
```

> [!CAUTION]
> **Bug I made:** I originally wrote `if (i == n % i)`.
> Inside this block `n % i` is always `0` (we already checked `n % i == 0`), so the condition is never true and every pair adds 2.
> For `n = 100` that printed **10** instead of **9**.
> ✔️ Use `n // i` (integer division), **not** `n % i` (remainder).

---

### 📝 Quick Revision Summary

| | Brute Force | Optimized |
|:---|:---:|:---:|
| **Loop runs** | `1 → n` | `1 → √n` |
| **Iterations** | `n` | `√n` |
| **Time Complexity** | **O(n)** | **O(√n)** |
| **Space Complexity** | O(1) | O(1) |
| **n = 10¹⁸** (at 10⁸ iterations/sec) | ≈ 317 years 😱 | √10¹⁸ = 10⁹ iterations ≈ **10 sec** ⚡ |

**🧠 Remember:**
- Count **iterations**, not seconds (🌋 volcano vs 🏔️ Everest).
- **10⁸ iterations ≈ 1 second.**
- Factors come in **pairs** `(i, n/i)`, so we only loop till **√n**.
- Watch out for **perfect squares**: when `i == n/i`, count **once**.
- Prefer `i * i <= n` over calling `sqrt(n)` every iteration.

---

## 🧮 Arrays and Manipulation

> [!NOTE]
> 🚧 *Notes coming soon — will be added after the next class.*

---

## 📸 Original Notebook Pages

<details>
<summary><b>Click to view my handwritten notes</b></summary>

<br>

**Page 1: Problem, brute force, execution time**

<img src="images/page-1.jpeg" alt="Notebook page 1" width="600">

**Page 2: 10⁸ rule and optimization approach**

<img src="images/page-2.jpeg" alt="Notebook page 2" width="600">

**Page 3: Optimized code and perfect squares**

<img src="images/page-3.jpeg" alt="Notebook page 3" width="600">

</details>

---

<div align="center">

⭐ *Made with consistency, one class at a time.* ⭐

</div>
