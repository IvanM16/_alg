import math

def g(x):
    """定義不動點轉移函數 g(x) = cos(x)"""
    return math.cos(x)

def solve_fixed_point(g, x0, tol=1e-7, max_iter=100):
    """
    使用不動點迭代法求解 x = g(x)
    
    參數:
      g        : 迭代轉移函數
      x0       : 初始值
      tol      : 容忍誤差 (Tolerance)
      max_iter : 最大迭代次數
    """
    x = x0
    print(f"{'Step':<6} | {'x_k':<12} | {'x_{k+1}':<12} | {'|x_{k+1} - x_k|':<18}")
    print("-" * 55)
    
    for k in range(1, max_iter + 1):
        x_next = g(x)
        diff = abs(x_next - x)
        print(f"{k:<6d} | {x:<12.7f} | {x_next:<12.7f} | {diff:<18.7e}")
        
        if diff < tol:
            print("-" * 55)
            print(f"成功於第 {k} 次迭代收斂！數值解 x = {x_next:.7f}")
            return x_next
            
        x = x_next
        
    print("已達最大迭代次數，未在限定次數內收斂。")
    return x

if __name__ == "__main__":
    print("=== 自訂迭代問題：求解 x = cos(x) 的不動點 ===")
    initial_guess = 0.5
    solve_fixed_point(g, x0=initial_guess)