import time
import random
from typing import List, Tuple

# ==========================================
# 1. 動態規劃法 (LCS DIFF)
# ==========================================
def lcs_dp_diff(a: List[str], b: List[str]) -> Tuple[int, List[Tuple[str, str]]]:
    """
    使用基於 LCS (最長公共子序列) 的動態規劃進行文本差異比較。
    時間複雜度: O(M * N)
    空間複雜度: O(M * N)
    """
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 填寫 DP 表格
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    # 回溯 (Traceback) 以重建 Diff 腳本
    diff = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            diff.append(('=', a[i - 1]))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            diff.append(('+', b[j - 1]))
            j -= 1
        elif i > 0 and (j == 0 or dp[i - 1][j] > dp[i][j - 1]):
            diff.append(('-', a[i - 1]))
            i -= 1
            
    diff.reverse()
    edit_distance = (m - dp[m][n]) + (n - dp[m][n])
    return edit_distance, diff


# ==========================================
# 2. 非動態規劃法 (MEYER'S O(ND) DIFF)
# ==========================================
def meyers_diff(a: List[str], b: List[str]) -> Tuple[int, List[Tuple[str, str]]]:
    """
    使用 Meyer's 貪婪編輯圖演算法 (Greedy Edit Graph Algorithm) 進行文本比較。
    時間複雜度: O((M+N) * D)
    空間複雜度: O(D^2) (用於重建 Diff 腳本)
    """
    m, n = len(a), len(b)
    max_d = m + n
    v = {1: 0}
    trace = []
    
    # 基於編輯距離 D 進行最短路徑搜尋
    for d in range(max_d + 1):
        v_copy = v.copy()
        trace.append(v_copy)
        
        for k in range(-d, d + 1, 2):
            # 選擇移動方向：Down (新增) 或 Right (刪除)
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                x = v.get(k + 1, 0)
            else:
                x = v.get(k - 1, 0) + 1
                
            y = x - k
            
            # 沿對角線延伸（相同行不花費成本）
            while x < m and y < n and a[x] == b[y]:
                x += 1
                y += 1
                
            v[k] = x
            
            # 若到達圖的右下角
            if x >= m and y >= n:
                # 回溯以重建差異腳本
                diff = []
                x_curr, y_curr = m, n
                
                for d_step in range(d, 0, -1):
                    v_prev = trace[d_step]
                    k_curr = x_curr - y_curr
                    
                    if k_curr == -d_step or (k_curr != d_step and v_prev.get(k_curr - 1, -1) < v_prev.get(k_curr + 1, -1)):
                        prev_k = k_curr + 1
                    else:
                        prev_k = k_curr - 1
                        
                    prev_x = v_prev[prev_k]
                    prev_y = prev_x - prev_k
                    
                    # 沿對角線向上回溯
                    while x_curr > prev_x and y_curr > prev_y:
                        diff.append(('=', a[x_curr - 1]))
                        x_curr -= 1
                        y_curr -= 1
                        
                    # 判斷是新增還是刪除
                    if x_curr == prev_x:
                        diff.append(('+', b[y_curr - 1]))
                        y_curr -= 1
                    else:
                        diff.append(('-', a[x_curr - 1]))
                        x_curr -= 1
                        
                while x_curr > 0 and y_curr > 0:
                    diff.append(('=', a[x_curr - 1]))
                    x_curr -= 1
                    y_curr -= 1
                    
                diff.reverse()
                return d, diff
                
    return 0, []


# ==========================================
# 工具函式與效能基準測試 (BENCHMARK)
# ==========================================
def print_diff(title: str, diff_result: List[Tuple[str, str]]):
    print(f"\n--- {title} ---")
    for tag, line in diff_result:
        if tag == '=':
            print(f"  {line}")
        elif tag == '+':
            print(f"+ {line}")
        elif tag == '-':
            print(f"- {line}")

def run_benchmark():
    print("==================================================")
    print("程式碼差異比較測試 (Demo)")
    print("==================================================")
    
    doc_a = [
        "import os",
        "import sys",
        "def hello():",
        "    print('Hello World')",
        "hello()"
    ]
    
    doc_b = [
        "import os",
        "import sys",
        "def hello():",
        "    print('Hello, Algoritma!')",
        "    print('Fitur Baru')",
        "hello()"
    ]

    _, dp_res = lcs_dp_diff(doc_a, doc_b)
    _, meyers_res = meyers_diff(doc_a, doc_b)
    
    print_diff("Diff 結果 (動態規劃 LCS)", dp_res)
    print_diff("Diff 結果 (Meyer's 演算法)", meyers_res)

    print("\n==================================================")
    print("效能基準測試：大型文件與少量修改")
    print("==================================================")
    
    n_lines = 1000
    edit_count = 10
    
    base_file = [f"line_{i}: function_body_content_code_{i}" for i in range(n_lines)]
    modified_file = base_file.copy()
    
    random.seed(42)
    for _ in range(edit_count):
        idx = random.randint(0, n_lines - 1)
        modified_file[idx] = f"modified_line_{idx}: updated_content"

    # 測試 DP
    t0 = time.perf_counter()
    dp_d, _ = lcs_dp_diff(base_file, modified_file)
    t_dp = time.perf_counter() - t0

    # 測試 Meyer's
    t0 = time.perf_counter()
    meyers_d, _ = meyers_diff(base_file, modified_file)
    t_meyers = time.perf_counter() - t0

    print(f"文件 A 大小 : {n_lines} 行")
    print(f"文件 B 大小 : {len(modified_file)} 行")
    print(f"修改行數    : ~{edit_count} 行")
    print(f"\n[動態規劃 LCS]")
    print(f"  總編輯距離 (Edit Distance) : {dp_d}")
    print(f"  執行時間                  : {t_dp:.6f} 秒")
    
    print(f"\n[Meyer's 演算法 (非 DP)]")
    print(f"  總編輯距離 (Edit Distance) : {meyers_d}")
    print(f"  執行時間                  : {t_meyers:.6f} 秒")
    
    if t_meyers > 0:
        speedup = t_dp / t_meyers
        print(f"\n--> 在此情境下，Meyer's 演算法比動態規劃快了 **{speedup:.2f} 倍**！")

if __name__ == "__main__":
    run_benchmark()