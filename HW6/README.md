# Lambda Calculus 解譯器 (Lambda Calculus Interpreter)

本專案為一個基於 Python 實作的 **Lambda Calculus (無類型 Lambda 運算) 解譯器**，支援語法解析、名稱展開、捕獲迴避代換（Capture-avoiding substitution with $\alpha$-conversion），以及完整展示 $\beta$-規約（$\beta$-reduction）計算步驟的功能。

---

## 一、 功能特色

1. **語法分析與巨集展開 (Parser & Macro Expansion)**：
   - 支援經典 Lambda 語法標記 `\` 與 `λ`。
   - 支援函數應用的左結合律（Left-associative Application）與括號優先權調整。
   - 內建組合子與 Church 編碼（Church Booleans、Church Numerals、 Church Arithmetic）。

2. **正確的代換機制 ($\alpha$-conversion)**：
   - 實作 Capture-avoiding substitution，自動偵測自由變數（Free Variables）。
   - 在發生變數名稱衝突時自動重新命名（Generate fresh variable），避免產生 Variable Capture 錯誤。

3. **完整的計算過程展示 ($\beta$-reduction Step-by-Step Trace)**：
   - 使用 **正規序 (Normal Order Reduction)**，保證若表達式存在正規型 (Normal Form)，必能正確規約。
   - 逐步列印出每次 $\beta$-規約後的 AST 變化狀況。

---

## 二、 語法說明

* **變數 (Variable)**: `x`, `y`, `a`, `b`
* **抽象/函數定義 (Abstraction)**: `\x. x` 或 `λx. x`
* **應用/呼叫 (Application)**: `(f x)` 或 `f x y`
* **預設巨集 (Built-in Macros)**:
  * 邏輯：`TRUE`, `FALSE`, `AND`, `OR`, `NOT`
  * 數值：`ZERO`, `ONE`, `TWO`, `THREE`
  * 運算：`SUCC` (加一), `PLUS` (加法), `MULT` (乘法)

---

## 三、 安裝與執行方式

### 需求環境
* Python 3.8+ (無須額外安裝第三方套件)

### 執行步驟

1. 將 `lambda_interpreter.py` 存至本地檔夾。
2. 開啟終端機 (Terminal) 並執行：

```bash
python3 lambda_interpreter.py