# Recurrence Relations Solver & Time Complexity Analysis

This project provides mathematical derivations and Python implementations to verify exact closed-form solutions and Big $O$ time complexities for four fundamental recurrence relations.

---

## Summary of Recurrence Relations

| Equation | Recurrence Relation | Exact Closed-Form $T(n)$ | Big $O$ Complexity | Algorithm Prototype |
| :--- | :--- | :--- | :--- | :--- |
| **1** | $T(n) = T(n-1) + 8$ | $8n - 7$ | $O(n)$ | Linear Iteration / Linear Search |
| **2** | $T(n) = 2T(n-1) + 9$ | $5 \cdot 2^n - 9$ | $O(2^n)$ | Unoptimized Double Recursion / Tower of Hanoi |
| **3** | $T(n) = 2T(n/2) + 1$ | $2n - 1$ | $O(n)$ | Full Binary Tree Traversal |
| **4** | $T(n) = T(n/2) + 1$ | $\log_2 n + 1$ | $O(\log n)$ | Binary Search |

---

## Detailed Mathematical Proofs

### Equation 1: $T(n) = T(n-1) + 8, \quad T(1) = 1$
Unrolling the relation step-by-step:
$$\begin{aligned} T(n) &= T(n-1) + 8 \\ &= [T(n-2) + 8] + 8 = T(n-2) + 2(8) \\ &= T(n-3) + 3(8) \\ &\ \ \vdots \\ &= T(1) + (n-1) \cdot 8 \end{aligned}$$
Substituting base condition $T(1) = 1$:
$$T(n) = 1 + 8n - 8 = 8n - 7 \implies \mathbf{O(n)}$$

---

### Equation 2: $T(n) = 2T(n-1) + 9, \quad T(1) = 1$
Unrolling the relation step-by-step:
$$\begin{aligned} T(n) &= 2T(n-1) + 9 \\ &= 2[2T(n-2) + 9] + 9 = 2^2 T(n-2) + 2(9) + 9 \\ &= 2^2 [2T(n-3) + 9] + 2(9) + 9 = 2^3 T(n-3) + 2^2(9) + 2(9) + 9 \\ &\ \ \vdots \\ &= 2^{n-1} T(1) + 9 \sum_{i=0}^{n-2} 2^i \end{aligned}$$
Using the geometric sum formula $\sum_{i=0}^{n-2} 2^i = 2^{n-1} - 1$:
$$\begin{aligned} T(n) &= 2^{n-1}(1) + 9(2^{n-1} - 1) \\ &= 10 \cdot 2^{n-1} - 9 \\ &= 5 \cdot 2^n - 9 \implies \mathbf{O(2^n)} \end{aligned}$$

---

### Equation 3: $T(n) = 2T(n/2) + 1, \quad T(1) = 1$
Let $n = 2^k$ (so $k = \log_2 n$):
$$\begin{aligned} T(n) &= 2T(n/2) + 1 \\ &= 2[2T(n/4) + 1] + 1 = 2^2 T(n/2^2) + 2 + 1 \\ &= 2^2 [2T(n/2^3) + 1] + 2 + 1 = 2^3 T(n/2^3) + 2^2 + 2 + 1 \\ &\ \ \vdots \\ &= 2^k T(n/2^k) + \sum_{i=0}^{k-1} 2^i \end{aligned}$$
Substituting $2^k = n$, $T(1) = 1$, and $\sum_{i=0}^{k-1} 2^i = 2^k - 1 = n - 1$:
$$T(n) = n(1) + (n - 1) = 2n - 1 \implies \mathbf{O(n)}$$

---

### Equation 4: $T(n) = T(n/2) + 1, \quad T(1) = 1$
Let $n = 2^k$ (so $k = \log_2 n$):
$$\begin{aligned} T(n) &= T(n/2) + 1 \\ &= [T(n/4) + 1] + 1 = T(n/2^2) + 2 \\ &= T(n/2^3) + 3 \\ &\ \ \vdots \\ &= T(n/2^k) + k \end{aligned}$$
Substituting $n/2^k = 1$ ($k = \log_2 n$) and $T(1) = 1$:
$$T(n) = T(1) + \log_2 n = \log_2 n + 1 \implies \mathbf{O(\log n)}$$

---

## File Structure

```text
.
├── recurrence_solver.py  # Python verification code (Recursive vs Exact formula)
└── README.md             # Theoretical analysis and execution guidelines