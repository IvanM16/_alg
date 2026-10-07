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
