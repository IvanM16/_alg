import time
import sys

# Increase recursion depth limit
sys.setrecursionlimit(2000)

def power2n_1(n):
    return 2**n

def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)

def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)

memo = {}
def power2n_3(n):
    if n == 0:
        return 1
    if n in memo:
        return memo[n]
    
    # Corrected indentation (4 spaces)
    memo[n] = power2n_3(n - 1) + power2n_3(n - 1)
    return memo[n]

def test_power2n(func, n, func_name):
    print(f"--- 測試 {func_name} (n={n}) ---")
    start_time = time.time()
    try:
        result = func(n)
        end_time = time.time()
        exec_time = end_time - start_time
        print(f"結果位數 : {len(str(result))} 位數")
        print(f"執行時間 : {exec_time:.6f} 秒\n")
    except Exception as e:
        end_time = time.time()
        print(f"執行失敗 : {e}")
        print(f"耗時     : {end_time - start_time:.6f} 秒\n")

if __name__ == "__main__":
    test_n = 100

    print("==========================================")
    print(f" 開始執行 $2^{{{test_n}}}$ 效能測試 ")
    print("==========================================\n")

    test_power2n(power2n_1, test_n, "方法 1 (2**n)")
    test_power2n(power2n_2b, test_n, "方法 2b (2*power2n(n-1))")
    test_power2n(power2n_3, test_n, "方法 3 (遞迴+查表)")

    print("注意：方法 2a 在 n=100 時複雜度為 O(2^100)，將無法在合理時間內算完。")
    print("先以 n=30 示範其耗時：")
    test_power2n(power2n_2a, 30, "方法 2a (雙重遞迴, n=30)")