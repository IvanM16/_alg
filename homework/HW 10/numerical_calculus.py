"""
數值微積分與蒙地卡羅積分 (Numerical Calculus & Monte Carlo Integration)
====================================================================
【AI 使用說明 / AI Usage Disclosure】
本程式由 AI（Google Gemini）協助撰寫與結構化設計，並經人工審閱數學公式、演算法邏輯與邊界條件測試。

涵蓋題目與功能：
1. 用數值方法計算單變數微分（中心差分法）和積分（中點黎曼積分法）
2. 用蒙地卡羅法計算單變數積分
3. 用數值方法計算 n 變數微分（梯度 Gradient）和積分（超體積 Hypervolume）
4. 用蒙地卡羅法計算 n 變數積分（超體積 Hypervolume）
5. 用黎曼積分法實作函數 integral(f, low, high) 進行 n 變數積分
   - 分別測試 1 維、2 維、5 維、100 維
   - 範例函數 f(x) = x_1^2 + ... + x_n^2，積分區間 low = 0, high = 1
6. 改用蒙地卡羅法進行相同的 n 變數積分（1 維、2 維、5 維、100 維）並與解析解比較
"""

import itertools
import math
import random
import time
from typing import Callable, Sequence, Tuple


# =====================================================================
# 1. 單變數數值微分與積分
# =====================================================================
def diff_1d(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    """使用中心差分法計算單變數函數 f 在 x 點的一階導數 f'(x)，截斷誤差為 O(h^2)。"""
    return (f(x + h) - f(x - h)) / (2.0 * h)


def riemann_integral_1d(
    f: Callable[[float], float], a: float, b: float, n: int = 10000
) -> float:
    """使用中點黎曼和計算單變數函數 f 在區間 [a, b] 上的定積分。"""
    if n <= 0:
        raise ValueError("切分數 n 必須為正整數")
    dx = (b - a) / n
    total = 0.0
    for i in range(n):
        mid_x = a + (i + 0.5) * dx
        total += f(mid_x)
    return total * dx


# =====================================================================
# 2. 蒙地卡羅法單變數積分
# =====================================================================
def mc_integral_1d(
    f: Callable[[float], float],
    a: float,
    b: float,
    num_samples: int = 100000,
) -> Tuple[float, float]:
    """
    使用蒙地卡羅法計算單變數函數 f 在區間 [a, b] 上的定積分。
    回傳：(積分估計值, 標準誤 Standard Error)
    """
    if num_samples <= 0:
        raise ValueError("樣本數 num_samples 必須為正整數")
    uniform = random.uniform
    values = [f(uniform(a, b)) for _ in range(num_samples)]
    mean_val = sum(values) / num_samples
    variance = sum((v - mean_val) ** 2 for v in values) / (num_samples - 1)
    width = b - a
    estimate = width * mean_val
    std_error = width * math.sqrt(variance / num_samples)
    return estimate, std_error


# =====================================================================
# 3. n 變數數值微分（梯度）與積分（超體積）
# =====================================================================
def gradient(
    f: Callable[[Sequence[float]], float],
    x: Sequence[float],
    h: float = 1e-6,
) -> list[float]:
    """
    計算 n 變數純量函數 f 在向量 x 處的梯度向量 nabla f(x)。
    對每個座標軸使用中心差分法計算偏導數。
    """
    x_list = list(x)
    grad = []
    for i in range(len(x_list)):
        x_plus = x_list.copy()
        x_minus = x_list.copy()
        x_plus[i] += h
        x_minus[i] -= h
        df_dxi = (f(x_plus) - f(x_minus)) / (2.0 * h)
        grad.append(df_dxi)
    return grad


def riemann_hypervolume(
    f: Callable[[Sequence[float]], float],
    low: Sequence[float],
    high: Sequence[float],
    steps_per_dim: int = 10,
    max_evals: int = 5_000_000,
) -> float:
    """
    使用 n 維中點黎曼和計算多變數函數 f 在超矩形 [low, high] 上的積分（超體積）。
    當 f(x) = 1 時，計算結果即為該超矩形的幾何超體積。
    """
    if len(low) != len(high):
        raise ValueError("low 與 high 的陣列長度必須相同")
    n = len(low)
    if n == 0:
        raise ValueError("維度 n 至少必須為 1")
    if steps_per_dim <= 0:
        raise ValueError("steps_per_dim 必須為正整數")

    total_grid_points = steps_per_dim**n
    if total_grid_points > max_evals:
        raise OverflowError(
            f"維度災難：{n} 維空間每維切分 {steps_per_dim} 等分將產生 "
            f"{steps_per_dim}^{n} = {total_grid_points:.3e} 個網格點，"
            f"超過安全上限 {max_evals:,}，無法在合理時間內完成計算！"
        )

    steps = [(high[d] - low[d]) / steps_per_dim for d in range(n)]
    cell_volume = math.prod(steps)
    midpoints_per_dim = [
        [low[d] + (i + 0.5) * steps[d] for i in range(steps_per_dim)]
        for d in range(n)
    ]

    total = 0.0
    for point in itertools.product(*midpoints_per_dim):
        total += f(point)

    return total * cell_volume


# =====================================================================
# 4. 蒙地卡羅法 n 變數積分（超體積）
# =====================================================================
def mc_hypervolume(
    f: Callable[[Sequence[float]], float],
    low: Sequence[float],
    high: Sequence[float],
    num_samples: int = 100000,
) -> Tuple[float, float]:
    """
    使用蒙地卡羅法計算 n 變數函數 f 在超矩形 [low, high] 上的積分（超體積）。
    回傳：(積分估計值, 標準誤 Standard Error)
    """
    if len(low) != len(high):
        raise ValueError("low 與 high 的陣列長度必須相同")
    n = len(low)
    if n == 0:
        raise ValueError("維度 n 至少必須為 1")
    if num_samples <= 0:
        raise ValueError("num_samples 必須為正整數")

    domain_volume = math.prod(high[d] - low[d] for d in range(n))
    uniform = random.uniform

    sum_val = 0.0
    sum_sq = 0.0
    for _ in range(num_samples):
        point = [uniform(low[d], high[d]) for d in range(n)]
        val = f(point)
        sum_val += val
        sum_sq += val * val

    mean_val = sum_val / num_samples
    variance = (sum_sq - num_samples * (mean_val**2)) / (num_samples - 1)
    estimate = domain_volume * mean_val
    std_error = domain_volume * math.sqrt(max(0.0, variance) / num_samples)
    return estimate, std_error


# =====================================================================
# 5. 題目指定之黎曼積分函數 integral(f, low, high)
# =====================================================================
def integral(
    f: Callable[[Sequence[float]], float],
    low: Sequence[float],
    high: Sequence[float],
    steps_per_dim: int | None = None,
) -> float:
    """
    黎曼積分法函數 integral(f, low, high)，維度 n 由 low 與 high 的陣列長度決定。
    若未指定 steps_per_dim，會依據維度自動設定合理切分數（高維時至少切分 2 等分）。
    """
    n = len(low)
    if steps_per_dim is None:
        if n == 1:
            steps_per_dim = 1000
        elif n == 2:
            steps_per_dim = 100
        elif n <= 5:
            steps_per_dim = 10
        else:
            # 高維度（如 100 維）即使每維僅切分 2 等分，網格點數仍高達 2^100
            steps_per_dim = 2
    return riemann_hypervolume(f, low, high, steps_per_dim=steps_per_dim)


# =====================================================================
# 6. 改用蒙地卡羅法做 n 變數積分（介面與 integral(f, low, high) 對應）
# =====================================================================
def mc_integral(
    f: Callable[[Sequence[float]], float],
    low: Sequence[float],
    high: Sequence[float],
    num_samples: int = 100000,
) -> Tuple[float, float]:
    """蒙地卡羅法 n 變數積分函數，對應第 6 題要求。"""
    return mc_hypervolume(f, low, high, num_samples=num_samples)


# 測試用範例函數：f(x) = x_1^2 + x_2^2 + ... + x_n^2
def sum_of_squares(x: Sequence[float]) -> float:
    return sum(xi * xi for xi in x)


# =====================================================================
# 主程式：1 至 6 題完整測試範例
# =====================================================================
def main() -> None:
    random.seed(42)

    # -----------------------------------------------------------------
    # 測試 1：單變數數值微分與積分
    # -----------------------------------------------------------------
    print("=" * 76)
    print("【1. 單變數數值微分與積分測試】")
    print("測試函數：f(x) = x^3 + 2x，導數評估點 x = 2.0，積分區間 [0, 2]")
    print("=" * 76)
    f_1d = lambda x: x**3 + 2.0 * x
    exact_df = 3.0 * (2.0**2) + 2.0  # f'(2) = 14.0
    exact_int = (2.0**4) / 4.0 + (2.0**2)  # int_0^2 (x^3 + 2x) dx = 4 + 4 = 8.0

    num_df = diff_1d(f_1d, 2.0)
    num_int = riemann_integral_1d(f_1d, 0.0, 2.0, n=10000)
    print(f"數值微分 f'(2.0)   = {num_df:.8f} | 解析解 = {exact_df:.8f} | 誤差 = {abs(num_df - exact_df):.2e}")
    print(f"黎曼積分 int_0^2 f = {num_int:.8f} | 解析解 = {exact_int:.8f} | 誤差 = {abs(num_int - exact_int):.2e}\n")

    # -----------------------------------------------------------------
    # 測試 2：蒙地卡羅法單變數積分
    # -----------------------------------------------------------------
    print("=" * 76)
    print("【2. 蒙地卡羅法單變數積分測試】")
    print("測試函數：f(x) = x^3 + 2x，積分區間 [0, 2]，樣本數 M = 100,000")
    print("=" * 76)
    mc_1d_est, mc_1d_se = mc_integral_1d(f_1d, 0.0, 2.0, num_samples=100000)
    print(
        f"蒙地卡羅估計值     = {mc_1d_est:.6f} +/- {mc_1d_se:.6f} | "
        f"解析解 = {exact_int:.6f} | 實際誤差 = {abs(mc_1d_est - exact_int):.6f}\n"
    )

    # -----------------------------------------------------------------
    # 測試 3：n 變數數值微分（梯度）與積分（超體積）
    # -----------------------------------------------------------------
    print("=" * 76)
    print("【3. n 變數數值微分（梯度）與積分（超體積）測試】")
    print("=" * 76)
    # 3a. 梯度測試：g(x, y, z) = x^2 * y + y^2 * z + z^3 在 (1, 2, 3) 的梯度
    # 解析偏導數：dg/dx = 2xy = 4, dg/dy = x^2 + 2yz = 1 + 12 = 13, dg/dz = y^2 + 3z^2 = 4 + 27 = 31
    g_3d = lambda v: (v[0] ** 2) * v[1] + (v[1] ** 2) * v[2] + (v[2] ** 3)
    grad_est = gradient(g_3d, [1.0, 2.0, 3.0])
    print("3a. 3 變數函數 g(x, y, z) = x^2*y + y^2*z + z^3 在 (1, 2, 3) 的梯度：")
    print(f"    數值梯度 = {[round(val, 6) for val in grad_est]} | 解析解 = [4.0, 13.0, 31.0]")

    # 3b. 超體積積分測試：3 維超矩形 [0, 2] x [0, 3] x [0, 4]
    # 當 h(x, y, z) = 1 時，積分即為幾何超體積 2 * 3 * 4 = 24.0
    # 當 h(x, y, z) = x + y + z 時，解析解 = 24 * (1.0 + 1.5 + 2.0) = 108.0
    unit_fn = lambda v: 1.0
    linear_fn = lambda v: v[0] + v[1] + v[2]
    vol_geom = riemann_hypervolume(unit_fn, [0, 0, 0], [2, 3, 4], steps_per_dim=10)
    vol_weighted = riemann_hypervolume(linear_fn, [0, 0, 0], [2, 3, 4], steps_per_dim=20)
    print("3b. 3 維超矩形 [0, 2] x [0, 3] x [0, 4] 黎曼超體積積分：")
    print(f"    幾何超體積 (f=1)       = {vol_geom:.6f} | 解析解 = 24.000000")
    print(f"    加權超體積 (f=x+y+z)   = {vol_weighted:.6f} | 解析解 = 108.000000\n")

    # -----------------------------------------------------------------
    # 測試 4：蒙地卡羅法 n 變數積分（超體積）
    # -----------------------------------------------------------------
    print("=" * 76)
    print("【4. 蒙地卡羅法 n 變數積分（超體積）測試】")
    print("=" * 76)
    mc_vol_geom, se_geom = mc_hypervolume(unit_fn, [0, 0, 0], [2, 3, 4], num_samples=100000)
    mc_vol_weighted, se_weighted = mc_hypervolume(linear_fn, [0, 0, 0], [2, 3, 4], num_samples=100000)
    print(f"    幾何超體積 (f=1)       = {mc_vol_geom:.6f} +/- {se_geom:.6f} | 解析解 = 24.000000")
    print(f"    加權超體積 (f=x+y+z)   = {mc_vol_weighted:.6f} +/- {se_weighted:.6f} | 解析解 = 108.000000\n")

    # -----------------------------------------------------------------
    # 測試 5：黎曼積分法 integral(f, low, high) 測試 1, 2, 5, 100 維
    # -----------------------------------------------------------------
    print("=" * 76)
    print("【5. 黎曼積分法 integral(f, low, high) 高維測試】")
    print("測試函數：f(x) = x_1^2 + ... + x_n^2，區間 low = 0, high = 1，解析解 = n / 3")
    print("=" * 76)
    test_dims = [1, 2, 5, 100]
    for n in test_dims:
        low = [0.0] * n
        high = [1.0] * n
        exact = n / 3.0
        t0 = time.perf_counter()
        try:
            est = integral(sum_of_squares, low, high)
            elapsed = time.perf_counter() - t0
            print(
                f"n = {n:<3} 維 | 解析解 = {exact:<10.6f} | 黎曼估計 = {est:<10.6f} | "
                f"誤差 = {abs(est - exact):.6f} | 耗時 = {elapsed:.4f}s"
            )
        except OverflowError as err:
            print(f"n = {n:<3} 維 | 解析解 = {exact:<10.6f} | 計算中止：{err}")
    print()

    # -----------------------------------------------------------------
    # 測試 6：改用蒙地卡羅法做 n 變數積分（同第 5 題：1, 2, 5, 100 維）
    # -----------------------------------------------------------------
    print("=" * 76)
    print("【6. 蒙地卡羅法 n 變數積分高維測試（題目同第 5 題）】")
    print("測試函數：f(x) = x_1^2 + ... + x_n^2，區間 low = 0, high = 1，樣本數 M = 100,000")
    print("=" * 76)
    for n in test_dims:
        low = [0.0] * n
        high = [1.0] * n
        exact = n / 3.0
        t0 = time.perf_counter()
        est, se = mc_integral(sum_of_squares, low, high, num_samples=100000)
        elapsed = time.perf_counter() - t0
        print(
            f"n = {n:<3} 維 | 解析解 = {exact:<10.6f} | 蒙地卡羅 = {est:<10.6f} +/- {se:.6f} | "
            f"實際誤差 = {abs(est - exact):.6f} | 耗時 = {elapsed:.4f}s"
        )


if __name__ == "__main__":
    main()