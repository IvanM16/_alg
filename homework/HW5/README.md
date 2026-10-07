Tower of Hanoi Solutions (河內塔問題解法)

本專案提供 河內塔問題（Tower of Hanoi） 的兩種 Python 實現方式：

遞迴解法（Recursive Approach）

非遞迴／迭代解法（Iterative Approach）

問題背景

河內塔是一個經典的數學謎題。有三根柱子（$A$、$B$、$C$）與 $n$ 個大小不等的圓盤。初始時所有圓盤依大小疊在柱子 $A$ 上（大的在下，小的在上）。目標是將所有圓盤移至柱子 $C$，並遵循以下規則：

每次只能移動一個圓盤。

每次只能從某根柱子頂端取下圓盤，並放在另一根柱子頂端。

任何時候大盤子都不能疊在小盤子上面。

對於 $n$ 個圓盤，最少移動次數為 $T(n) = 2^n - 1$。

解法原理

1. 遞迴解法 (Recursive)

遞迴的核心思考方式為分治法（Divide and Conquer）：

基本條件（Base Case）：當 $n = 1$ 時，直接將盤子從起始柱移至目標柱。

遞迴步驟（Recursive Step）：

將上面的 $n-1$ 個盤子從起始柱（src）移動到中介柱（aux）。

將第 $n$ 個盤子（最大盤）從起始柱（src）移動到目標柱（target）。

將中介柱（aux）上的 $n-1$ 個盤子移動到目標柱（target）。

遞迴關係式：


$$T(n) = 2T(n-1) + 1, \quad T(1) = 1$$

2. 非遞迴解法 (Iterative)

非遞迴解法利用了河內塔的週期規律：

總移動次數必然為 $2^n - 1$ 次。

當盤子數量 $n$ 為偶數時，目標柱與中介柱的順序需進行對調。

在第 $i$ 次移動時，移動的兩根柱子由 $i \bmod 3$ 決定：

$i \bmod 3 = 1$：在起始柱與目標柱之間移動。

$i \bmod 3 = 2$：在起始柱與中介柱之間移動。

$i \bmod 3 = 0$：在中介柱與目標柱之間移動。

每次在兩柱之間移動時，執行唯一合法的移動（將較小的盤子疊到較大的盤子上，或移至空柱）。

複雜度分析

方法

時間複雜度

空間複雜度

特點

遞迴解法

$O(2^n)$

$O(n)$

程式碼極簡、邏輯直觀、依賴 Call Stack

非遞迴解法

$O(2^n)$

$O(n)$

無函數遞迴開銷、需額外狀態維護

使用方法

確保系統已安裝 Python 3，並於終端機執行：

python hanoi.py


範例輸出 ($n = 3$)

========================================
1. Recursive Solution (n = 3)
========================================
Move disk 1 from A -> C
Move disk 2 from A -> B
Move disk 1 from C -> B
Move disk 3 from A -> C
Move disk 1 from B -> A
Move disk 2 from B -> C
Move disk 1 from A -> C

========================================
2. Iterative Solution (n = 3)
========================================
Move disk 1 from A -> C
Move disk 2 from A -> B
Move disk 1 from C -> B
Move disk 3 from A -> C
Move disk 1 from B -> A
Move disk 2 from B -> C
Move disk 1 from A -> C


# 遞迴符號數學式微分 (Recursive Symbolic Differentiation)

本專案利用 Python 的**遞迴 (Recursion)** 與**抽象語法樹 (Abstract Syntax Tree, AST)** 結構，實現能對數學表達式進行符號微分（Symbolic Differentiation）與自動簡化的程式引擎 `sym_diff(expr)`。

---

## 1. 資料結構設計 (AST Representation)

數學表達式以 Python 的原生資料型態（Tuple、字串與數字）進行樹狀結構化封裝：

- **常數 (Constant)**：`int` 或 `float`（例：`5`, `3.14`）
- **自變數 (Variable)**：`str`（例：`'x'`, `'y'`）
- **二元運算子 (Binary Ops)**：`(op, left, right)`
  - 加法：`('+', u, v)`
  - 減法：`('-', u, v)`
  - 乘法：`('*', u, v)`
  - 除法：`('/', u, v)`
  - 次方：`('**', u, n)`
- **一元運算子 / 函數 (Unary Ops / Functions)**：`(op, u)`
  - 負號：`('-', u)`
  - 正弦：`('sin', u)`
  - 餘弦：`('cos', u)`
  - 指數：`('exp', u)`
  - 自然對數：`('ln', u)`

---

## 2. 微分法則與遞迴實作 (`sym_diff`)

核心函數 `sym_diff(expr, var='x')` 透過對表達式進行結構分解，套用對應的微積分規則（包含連鎖律 Chain Rule）：

| 數學表達式 $f(x)$ | 微分規則 $\frac{d}{dx}f(x)$ | 遞迴邏輯 (Python) |
| :--- | :--- | :--- |
| 常數 $c$ | $0$ | `return 0` |
| 自變數 $x$ | $1$ | `return 1 if expr == var else 0` |
| 和 $u + v$ | $u' + v'$ | `('+', sym_diff(u), sym_diff(v))` |
| 差 $u - v$ | $u' - v'$ | `('-', sym_diff(u), sym_diff(v))` |
| 積 $u \cdot v$ | $u'v + uv'$ *(積法則)* | `('+', ('*', du, v), ('*', u, dv))` |
| 商 $\frac{u}{v}$ | $\frac{u'v - uv'}{v^2}$ *(商法則)* | `('/', ('-', ('*', du, v), ('*', u, dv)), ('**', v, 2))` |
| 冪次 $u^n$ | $n \cdot u^{n-1} \cdot u'$ *(連鎖律)* | `('*', ('*', n, ('**', u, n - 1)), du)` |
| $\sin(u)$ | $\cos(u) \cdot u'$ *(連鎖律)* | `('*', ('cos', u), du)` |
| $\cos(u)$ | $-\sin(u) \cdot u'$ *(連鎖律)* | `('*', ('-', ('sin', u)), du)` |
| $e^u$ | $e^u \cdot u'$ *(連鎖律)* | `('*', ('exp', u), du)` |
| $\ln(u)$ | $\frac{u'}{u}$ *(連鎖律)* | `('/', du, u)` |

---

## 3. 表達式簡化引擎 (`simplify`)

為避免微分展開後產生冗餘的樹狀結點（如 $0 \cdot x + 1 \cdot v$），`simplify(expr)` 提供遞迴代數簡化：

1. **常數折疊 (Constant Folding)**：
   - 例：`3 + 5` $\to$ `8`；`3 * 2` $\to$ `6`
2. **代數恆等式簡化 (Algebraic Identities)**：
   - $0 + u \to u$、 $u + 0 \to u$
   - $0 \cdot u \to 0$、 $1 \cdot u \to u$
   - $u - 0 \to u$、 $u - u \to 0$
   - $u^1 \to u$、 $u^0 \to 1$

---

## 4. 執行方式與範例輸出

### 執行命令

```bash
python sym_diff.py
==================================================
      Recursive Symbolic Differentiation Test     
==================================================
[1] Original  f(x)  = (((3 * (x ** 2)) + (2 * x)) + 5)
    Derivative f'(x) = ((6 * x) + 2)
    AST Tuple        = ('+', ('*', 6, 'x'), 2)
--------------------------------------------------
[2] Original  f(x)  = sin((x ** 2))
    Derivative f'(x) = (cos((x ** 2)) * (2 * x))
    AST Tuple        = ('*', ('cos', ('**', 'x', 2)), ('*', 2, 'x'))
--------------------------------------------------
[3] Original  f(x)  = cos(x)
    Derivative f'(x) = -(sin(x))
    AST Tuple        = ('-', ('sin', 'x'))
--------------------------------------------------
[4] Original  f(x)  = exp((3 * x))
    Derivative f'(x) = (exp((3 * x)) * 3)
    AST Tuple        = ('*', ('exp', ('*', 3, 'x')), 3)
--------------------------------------------------
[5] Original  f(x)  = (x * ln(x))
    Derivative f'(x) = (ln(x) + (x * (1 / x)))
    AST Tuple        = ('+', ('ln', 'x'), ('*', 'x', ('/', 1, 'x')))
--------------------------------------------------
[6] Original  f(x)  = ((2 * x) / (x + 1))
    Derivative f'(x) = (((2 * (x + 1)) - (2 * x)) / ((x + 1) ** 2))
    AST Tuple        = ('/', ('-', ('*', 2, ('+', 'x', 1)), ('*', 2, 'x')), ('**', ('+', 'x', 1), 2))
--------------------------------------------------


# Modular Pure Functional Programming: Custom High-Order Tools & Loopless Bubble Sort

This project is structured into separate Python modules demonstrating **Pure Functional Programming** principles. It features custom implementations of core higher-order functions (`my_map`, `my_filter`, `my_reduce`) and a **Loopless Bubble Sort** algorithm that strictly avoids `for` and `while` loops.

---

## Project Structure

```text
.
├── functional_core.py   # Core recursive implementations of map, filter, reduce, make_range
├── bubble_sort.py       # Functional Bubble Sort implementation using my_reduce
├── main.py              # Application entry point & test suite runner
└── README.md            # Technical documentation

#!/usr/bin/env bash
set -e

echo "🚀 Generating project files..."

# ==============================================================================
# 1. Create functional_core.py
# ==============================================================================
cat << 'EOF' > functional_core.py
"""
Functional Programming Core Utilities
Provides pure recursive implementations of map, filter, reduce, and range generation
without using any 'for' or 'while' loops.
"""

def my_map(func, seq):
    """
    Custom recursive implementation of map().
    """
    if not seq:
        return []
    return [func(seq[0])] + my_map(func, seq[1:])


def my_filter(func, seq):
    """
    Custom recursive implementation of filter().
    """
    if not seq:
        return []
    head, tail = seq[0], seq[1:]
    if func(head):
        return [head] + my_filter(func, tail)
    return my_filter(func, tail)


def my_reduce(func, seq, initializer=None):
    """
    Custom recursive implementation of reduce().
    """
    if initializer is None:
        if not seq:
            raise TypeError("my_reduce() of empty sequence with no initial value")
        return my_reduce(func, seq[1:], seq[0])
    if not seq:
        return initializer
    return my_reduce(func, seq[1:], func(initializer, seq[0]))


def make_range(n):
    """
    Custom recursive range generator replacement for range(1, n + 1).
    """
    if n <= 0:
        return []
    return make_range(n - 1) + [n]
EOF

echo "  ✔ Created functional_core.py"

# ==============================================================================
# 2. Create bubble_sort.py
# ==============================================================================
cat << 'EOF' > bubble_sort.py
"""
Loopless Bubble Sort Module
Implements functional Bubble Sort using custom my_reduce and make_range
from functional_core.py, completely eliminating for/while loops.
"""

from functional_core import my_reduce, make_range


def bubble_sort_functional(lst):
    """
    Sorts a list using Bubble Sort without any for/while loops.
    """
    if len(lst) <= 1:
        return lst

    # Inner Pass: Perform single-pass pairwise comparison & swaps using my_reduce
    def bubble_pass(arr):
        def step(acc, x):
            res_list, swapped = acc
            if not res_list:
                return ([x], swapped)
            last = res_list[-1]
            prev = res_list[:-1]
            if last > x:
                # Out of order: Swap last and x, set swapped flag to True
                return (prev + [x, last], True)
            else:
                return (res_list + [x], swapped)

        return my_reduce(step, arr, ([], False))

    # Outer Pass: Repeat inner pass up to N times using my_reduce over make_range(N)
    def outer_step(acc, pass_num):
        arr, swapped = acc
        # Early exit optimization: If no swaps occurred in previous pass, skip further passes
        if not swapped and pass_num != 1:
            return (arr, False)
        return bubble_pass(arr)

    # Trigger N outer passes via my_reduce
    sorted_arr, _ = my_reduce(outer_step, make_range(len(lst)), (lst, True))
    return sorted_arr
EOF

echo "  ✔ Created bubble_sort.py"

# ==============================================================================
# 3. Create main.py
# ==============================================================================
cat << 'EOF' > main.py
"""
Main Execution Script
Demonstrates custom high-order functions and loopless bubble sort across multiple test cases.
"""

from functional_core import my_map, my_filter, my_reduce
from bubble_sort import bubble_sort_functional


def main():
    print("=" * 60)
    print(" 1. Testing Custom High-Order Functions (my_map, my_filter, my_reduce)")
    print("=" * 60)

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Test my_map: Square elements
    squared = my_map(lambda x: x ** 2, numbers)
    print(f"my_map (Square)     : {squared}")

    # Test my_filter: Keep even numbers
    evens = my_filter(lambda x: x % 2 == 0, numbers)
    print(f"my_filter (Evens)   : {evens}")

    # Test my_reduce: Sum of elements
    total_sum = my_reduce(lambda acc, x: acc + x, numbers, 0)
    print(f"my_reduce (Sum)     : {total_sum}")

    print("\n" + "=" * 60)
    print(" 2. Testing Loopless Bubble Sort (bubble_sort_functional)")
    print("=" * 60)

    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [42, -5, 0, 18, -10, 42],
        []
    ]

    def run_case(case):
        sorted_res = bubble_sort_functional(case)
        filtered_gt_10 = my_filter(lambda x: x > 10, sorted_res)
        print(f"Original : {case}")
        print(f"Sorted   : {sorted_res}")
        print(f"Filtered (> 10): {filtered_gt_10}")
        print("-" * 50)

    # Run all test cases via my_map
    my_map(run_case, test_cases)


if __name__ == "__main__":
    main()
EOF

echo "  ✔ Created main.py"

# ==============================================================================
# 4. Create README.md
# ==============================================================================
cat << 'EOF' > README.md
# Modular Pure Functional Programming: Custom High-Order Tools & Loopless Bubble Sort

This project provides a pure functional programming implementation in Python that strictly eliminates all imperative iteration constructs (`for` and `while` loops). It features custom recursive implementations of foundational higher-order functions (`my_map`, `my_filter`, `my_reduce`) and applies them to execute a **Loopless Bubble Sort** algorithm using state fold reductions.

---

## 📁 Project Structure

```text
.
├── functional_core.py   # Core recursive implementations of map, filter, reduce, make_range
├── bubble_sort.py       # Loopless Bubble Sort implemented via my_reduce
├── main.py              # Test suite and execution runner
└── README.md            # Comprehensive project documentation