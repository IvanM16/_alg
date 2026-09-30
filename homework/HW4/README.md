# 第四週習題：迭代法與神經網路記憶機制 (Week 4: Iterative Methods)

本專案包含第四週課程「迭代法」的完整實作與說明文件，涵蓋自訂問題迭代求解、通用迭代框架（`iter_framework.py`）解析，以及結合 2024 年諾貝爾物理學獎（John Hopfield & Geoffrey Hinton）的神經網路記憶機制實作。

---

## 📁 專案檔案結構

| 檔案名稱 | 說明 |
| :--- | :--- |
| **`iterative_custom.py`** | 習題 1：自訂問題迭代求解（採用不動點迭代法求解 $x = \cos(x)$）。 |
| **`iter_framework.py`** | 習題 2：通用迭代演算法框架（含抽象狀態轉移與收斂控制）。 |
| **`iter_nobel_nn.py`** | 補充實作：2024 諾貝爾物理學獎 Hopfield 容錯記憶網路與 RBM CD-$k$ 演算法。 |
| **`README.md`** | 本專案綜合說明文件。 |

---

## 一、 自訂問題迭代求解 (`iterative_custom.py`)

### 1. 問題描述
使用**不動點迭代法（Fixed-Point Iteration）**，求解超越方程式 $x = \cos(x)$ 在實數體上的數值解（即多蒂數 Dottie Number）。

### 2. 演算法設計
* **轉移函數**：$x_{k+1} = g(x_k) = \cos(x_k)$
* **停機條件**：$\vert{}x_{k+1} - x_k\vert{} < 10^{-7}$
* **收斂證明**：根據巴拿赫不動點定理（Banach Fixed-Point Theorem），因在解附近 $\vert{}g'(x)\vert{} = \vert{}-\sin(x)\vert{} < 1$，故該迭代保證全局收斂至唯一不動點 $x \approx 0.7390851$。

---

## 二、 通用迭代框架說明文件 (`iter_framework.py`)

### 1. 設計理念
`iter_framework.py` 為一個高階、模組化的**通用迭代求解器框架 (Generic Iterative Solver Framework)**。採用**控制權分離（Separation of Concerns）**原則，將「迭代主迴圈、收斂判斷、安全邊界」與「具體問題的狀態更新邏輯」完全解耦。

### 2. 抽象數學模型
大部分迭代演算（如梯度下降、PageRank、Hopfield 網路等）均遵循狀態遞移規律：

$$\mathbf{x}^{(k+1)} = \text{Step}(\mathbf{x}^{(k)})$$

本框架抽象出 4 個核心要素：
1. **初始狀態 ($\mathbf{x}^{(0)}$)**：迭代的起點。
2. **單步轉移函數 (`step_func`)**：計算 $\mathbf{x}^{(k+1)} = T(\mathbf{x}^{(k)})$。
3. **收斂檢測函數 (`stop_func`)**：檢測 $\Vert{}\mathbf{x}^{(k+1)} - \mathbf{x}^{(k)}\Vert{} < \epsilon$。
4. **安全防護機制 (`max_iter`)**：限制最大迭代次數，防止死迴圈。

### 3. 控制流程圖

```text
       [ 開始 ]
          |
          v
    初始化狀態 x_0
          |
          v
+------------------------+
|   進入迭代迴圈 k=1..Max |
|   x_new = step_func(x) |
+------------------------+
          |
    +-----v-----+
    | 收斂判定  | ---- (是) ----> [ 回傳 x_new 與 迭代次數 k ]
    | stop_func |
    +-----+-----+
          | (否)
    +-----v-----+
    | k >= Max  | ---- (是) ----> [ 輸出發散警告 / 回傳部分結果 ]
    +-----+-----+
          | (否)
          +---> (進行下一輪迭代 x = x_new)