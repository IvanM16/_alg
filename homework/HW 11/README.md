# 數值微積分與蒙地卡羅積分（單變數至 $n$ 維超體積）

## AI 使用說明（AI Usage Disclosure）

* **是否使用 AI**：**是（Yes）**。
* **使用工具與方式**：本專案的 Python 程式碼（`numerical_calculus.py`）與本說明文件（`README.md`）皆由 **Google Gemini** 協助生成，並針對數值方法的數學公式、高維度「維度災難（Curse of Dimensionality）」保護機制以及 $1$ 維、$2$ 維、$5$ 維、$100$ 維的實驗數據進行人工驗證與測試。

---

## 專案檔案與執行方式

* `numerical_calculus.py`：包含題目 $1$ 至 $6$ 的完整演算法實作與測試主程式。
* `README.md`：包含 AI 使用說明、數學公式推導、測試範例說明與高維度積分效能比較。

本程式僅使用 Python 3 內建標準函式庫（`math`、`random`、`itertools`、`time`、`typing`），無需安裝任何第三方套件即可直接執行：

```bash
python numerical_calculus.py
```

---

## 1. 單變數數值微分與積分

### 1.1 中心差分法（Central Difference）
相較於截斷誤差為 $O(h)$ 的前向差分，本專案採用對稱的中心差分法計算一階導數，其截斷誤差為 $O(h^2)$：

$$f'(x) \approx \frac{f(x + h) - f(x - h)}{2h}$$

程式中預設步長 $h = 10^{-6}$。

### 1.2 中點黎曼積分法（Midpoint Riemann Sum）
將積分區間 $[a, b]$ 均分為 $N$ 個子區間，每個區間寬度為 $\Delta x = \frac{b - a}{N}$，取各子區間中點 $x_i = a + \left(i + \frac{1}{2}\right)\Delta x$ 計算函數值總和（誤差階數為 $O(\Delta x^2)$）：

$$\int_a^b f(x)\,dx \approx \sum_{i=0}^{N-1} f(x_i)\,\Delta x$$

* **測試範例**：$f(x) = x^3 + 2x$，在 $x = 2.0$ 處計算導數（解析解為 $14.0$），並在區間 $[0, 2]$ 計算定積分（解析解為 $8.0$）。

---

## 2. 蒙地卡羅法單變數積分

在區間 $[a, b]$ 內均勻隨機抽取 $M$ 個樣本點 $x_1, x_2, \dots, x_M \sim U(a, b)$，根據大數法則估計積分值：

$$\int_a^b f(x)\,dx \approx (b - a) \cdot \frac{1}{M} \sum_{m=1}^{M} f(x_m)$$

其標準誤（Standard Error）為：

$$\text{SE} = (b - a) \cdot \frac{s}{\sqrt{M}}$$

其中 $s$ 為樣本函數值的標準差，收斂速度為 $O\left(\frac{1}{\sqrt{M}}\right)$。

* **測試範例**：使用相同函數 $f(x) = x^3 + 2x$ 於 $[0, 2]$ 抽取 $M = 100,000$ 個樣本，結果收斂至解析解 $8.0$。

---

## 3. $n$ 變數數值微分（梯度）與積分（超體積）

### 3.1 數值梯度（Numerical Gradient）
對於 $n$ 變數純量函數 $f(\mathbf{x})$，其中 $\mathbf{x} = (x_1, x_2, \dots, x_n) \in \mathbb{R}^n$，梯度向量 $\nabla f(\mathbf{x})$ 由各座標方向的偏導數組成：

$$\nabla f(\mathbf{x}) = \left( \frac{\partial f}{\partial x_1}(\mathbf{x}), \frac{\partial f}{\partial x_2}(\mathbf{x}), \dots, \frac{\partial f}{\partial x_n}(\mathbf{x}) \right)$$

第 $i$ 個分量的中心差分近似為：

$$\frac{\partial f}{\partial x_i}(\mathbf{x}) \approx \frac{f(\mathbf{x} + h\mathbf{e}_i) - f(\mathbf{x} - h\mathbf{e}_i)}{2h}$$

其中 $\mathbf{e}_i$ 為第 $i$ 個標準單位向量。

### 3.2 $n$ 變數黎曼積分（超體積 Hypervolume）
給定 $n$ 維超矩形區域 $\Omega = [a_1, b_1] \times [a_2, b_2] \times \dots \times [a_n, b_n]$，若每個維度切分為 $k$ 等分，則第 $j$ 維的步長為 $h_j = \frac{b_j - a_j}{k}$，單一微元超立方體的超體積為 $\Delta V = \prod_{j=1}^{n} h_j$：

$$\int_{\Omega} f(\mathbf{x})\,dV \approx \sum_{i_1=0}^{k-1} \cdots \sum_{i_n=0}^{k-1} f\left(x_{1, i_1}, \dots, x_{n, i_n}\right) \Delta V$$

* **測試範例**：
  * **梯度**：$g(x, y, z) = x^2 y + y^2 z + z^3$ 在 $(1, 2, 3)$ 處的梯度，數值解為 $[4.0, 13.0, 31.0]$，與解析解完全吻合。
  * **超體積**：在 $3$ 維超矩形 $[0, 2] \times [0, 3] \times [0, 4]$ 上，當 $f(\mathbf{x}) = 1$ 時得出幾何超體積 $24.0$；當 $f(x, y, z) = x + y + z$ 時得出加權積分 $108.0$。

---

## 4. 蒙地卡羅法 $n$ 變數積分（超體積）

在 $n$ 維超矩形 $\Omega = \prod_{j=1}^{n} [a_j, b_j]$ 內均勻隨機產生 $M$ 個 $n$ 維點 $\mathbf{x}^{(1)}, \dots, \mathbf{x}^{(M)}$，設區域總超體積為 $V_{\Omega} = \prod_{j=1}^{n} (b_j - a_j)$，則積分近似為：

$$\int_{\Omega} f(\mathbf{x})\,dV \approx V_{\Omega} \cdot \frac{1}{M} \sum_{m=1}^{M} f\left(\mathbf{x}^{(m)}\right)$$

* **測試範例**：以 $M = 100,000$ 樣本計算 $3$ 維超矩形 $[0, 2] \times [0, 3] \times [0, 4]$ 的幾何超體積（$24.0$）與加權積分（$108.0$）。

---

## 5. 黎曼積分函數 `integral(f, low, high)` 高維度測試

本題針對測試函數：

$$f(\mathbf{x}) = x_1^2 + x_2^2 + \dots + x_n^2 = \sum_{i=1}^{n} x_i^2$$

在單位超立方體 $\Omega = [0, 1]^n$ 上的解析精確解為：

$$\int_{[0, 1]^n} \left(\sum_{i=1}^{n} x_i^2\right) dx_1 \cdots dx_n = \sum_{i=1}^{n} \int_0^1 x_i^2\,dx_i = \frac{n}{3}$$

在黎曼積分法 `integral(f, low, high)` 中，若每個維度切分 $k$ 等分，總計算網格點數為 $k^n$：

* **$1$ 維（$n = 1$）**：取 $k = 1000$，網格點數 $1000^1 = 1,000$，解析解為 $\frac{1}{3} \approx 0.333333$。
* **$2$ 維（$n = 2$）**：取 $k = 100$，網格點數 $100^2 = 10,000$，解析解為 $\frac{2}{3} \approx 0.666667$。
* **$5$ 維（$n = 5$）**：取 $k = 10$，網格點數 $10^5 = 100,000$，解析解為 $\frac{5}{3} \approx 1.666667$。
* **$100$ 維（$n = 100$）**：**遭遇維度災難（Curse of Dimensionality）**。即使每個維度僅切分 $k = 2$ 等分，總網格點數仍高達 $2^{100} \approx 1.27 \times 10^{30}$ 個，在有限時間內無法完成計算（程式內建安全檢查並拋出 `OverflowError` 提示）。

---

## 6. 改用蒙地卡羅法做 $n$ 變數積分（$1$ 維、$2$ 維、$5$ 維、$100$ 維）

改用蒙地卡羅法（`mc_integral(f, low, high, num_samples=100000)`）計算相同題目時，誤差收斂速度為 $O\left(\frac{1}{\sqrt{M}}\right)$，與維度 $n$ 無關，因此在 $100$ 維空間依然能在 $1$ 秒內精準完成計算：

| 維度 $n$ | 解析精確解 ($n / 3$) | 黎曼積分 `integral` 結果 | 黎曼網格點數 ($k^n$) | 蒙地卡羅法結果 ($M = 100,000$) | 蒙地卡羅標準誤 ($\text{SE}$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| $1$ 維 | $0.333333$ | $0.333333$ | $1,000$ | $0.333 \pm 0.002$ | $\approx 0.0009$ |
| $2$ 維 | $0.666667$ | $0.666650$ | $10,000$ | $0.667 \pm 0.003$ | $\approx 0.0013$ |
| $5$ 維 | $1.666667$ | $1.662500$ | $100,000$ | $1.667 \pm 0.004$ | $\approx 0.0021$ |
| $100$ 維 | $33.333333$ | **無法完成（網格點數 $2^{100}$）** | $1.27 \times 10^{30}$ | $33.333 \pm 0.019$ | $\approx 0.0094$ |

### 理論標準誤驗證（$100$ 維）
對於獨立同分佈的均勻隨機變數 $X_i \sim U(0, 1)$，單一維度平方項的變異數為：

$$\text{Var}(X_i^2) = \mathbb{E}[X_i^4] - (\mathbb{E}[X_i^2])^2 = \frac{1}{5} - \left(\frac{1}{3}\right)^2 = \frac{4}{45}$$

在 $n = 100$ 維時，總變異數為 $100 \times \frac{4}{45} = \frac{400}{45}$，因此抽樣 $M = 100,000$ 次的理論標準誤為：

$$\text{SE} = \sqrt{\frac{400 / 45}{100,000}} = \sqrt{\frac{4}{45,000}} \approx 0.009428$$

程式實測結果與理論標準誤完全一致。