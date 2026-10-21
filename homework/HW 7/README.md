# 文本差異比較 (Diff): 動態規劃 (LCS) vs Meyer's O(ND) 演算法

本專案探討並比較解決兩份文字檔案比較（**Text Difference / Diff**）問題的兩種主要演算法：
1. **動態規劃法 (Dynamic Programming, LCS - Longest Common Subsequence)**
2. **非動態規劃法 (Non-Dynamic Programming, Meyer's Greedy Edit Graph Algorithm)**

---

## 📌 問題描述

給定兩個文字檔案或字串陣列 $A = [a_1, a_2, \dots, a_m]$ 與 $B = [b_1, b_2, \dots, b_n]$，`diff` 操作的目標是找到**最短編輯腳本 (Shortest Edit Script, SES)** —— 即將文件 $A$ 轉換為文件 $B$ 所需的最少新增 (`+`) 與刪除 (`-`) 操作序列。

---

## 📐 演算法原理

### 1. 動態規劃法 (LCS - 最長公共子序列)

動態規劃將大問題分解為重複的子問題，並使用大小為 $(M+1) \times (N+1)$ 的 2D 矩陣紀錄中間結果。

#### 遞迴公式：
矩陣 $DP[i][j]$ 儲存字串前綴 $A[0 \dots i-1]$ 與 $B[0 \dots j-1]$ 的 LCS 長度：

$$DP[i][j] = \begin{cases} DP[i-1][j-1] + 1 & \text{若 } A[i-1] = B[j-1] \\  \max(DP[i-1][j], DP[i][j-1]) & \text{若 } A[i-1] \neq B[j-1] \end{cases}$$

填滿表格後，從 $DP[M][N]$ 開始進行**回溯 (Backtracking)** 回至 $DP[0][0]$，即可重建完整的差異腳本。

* **時間複雜度：** $O(M \times N)$
* **空間複雜度：** $O(M \times N)$（用於建立表格與回溯路徑）

---

### 2. 非動態規劃法 (Meyer's $O(ND)$ 演算法)

Meyer's 演算法將差異比較轉換為在**編輯圖 (Edit Graph)** 上尋找最短路徑問題。在編輯圖中：
* 向右移動代表「刪除 (`-`)」
* 向下移動代表「新增 (`+`)」
* 沿對角線移動代表「內容相同（不花費成本 / Cost 0）」

#### 運作機制（基於對角線的廣度優先搜尋 BFS）：
* 演算法依據編輯距離 $D$（從 $D = 0, 1, 2, \dots$）進行搜尋。
* 使用對角線座標 $k = x - y$。
* 在每個 $D$ 步數下，演算法會沿對角線盡可能延伸（連續相同的文字行不需要花費額外成本）。

* **時間複雜度：** $O(N \cdot D)$，其中 $N = M + N$，$D$ 為編輯距離 (Edit Distance，即相異的行數)。
* **空間複雜度：** $O(D^2)$（用於儲存回溯軌跡），若僅計算距離則可優化至 $O(D)$。

> **說明：** 在實際程式碼版本控制（如 Git）的情境中，修改的行數 $D$ 通常遠小於文件總行數 $N$ ($D \ll N$)。這使得 Meyer's 演算法在實際應用中比傳統的 LCS 動態規劃快上許多。

---

## 📊 綜合比較

| 特性 / 維度 | 動態規劃法 (LCS) | 非動態規劃法 (Meyer's Algorithm) |
| :--- | :--- | :--- |
| **核心思想** | 二維表格填表 (Bottom-Up Tabulation) | 編輯圖上的貪婪廣度搜尋 (Greedy BFS) |
| **時間複雜度** | $O(M \times N)$ | $O((M+N) \cdot D)$ |
| **空間複雜度** | $O(M \times N)$ | $O(D^2)$ |
| **當 $D \ll N$ 時效能** | 較慢（仍須計算整個矩陣） | **極快**（效能隨修改量 $D$ 線性變化） |
| **最壞情況複雜度** | $O(M \times N)$ | $O((M+N)^2)$（兩檔案完全不同時） |
| **實際應用場景** | 計算理論、生物資訊學 (DNA 比對) | `git diff`、GNU `diff`、SVN |

---

## 🚀 執行方式

執行 Python 腳本即可檢視差異比較輸出與效能基準測試：

```bash
python diff_comparison.py