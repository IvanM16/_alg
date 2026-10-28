import math
import random
import time
from typing import List, Tuple, Dict, Any


class TSPProblem:
    """旅行推銷員問題 (TSP) 類別，負責管理城市座標與距離矩陣計算。"""

    def __init__(self, cities: List[Tuple[float, float]]):
        self.cities = cities
        self.num_cities = len(cities)
        self.distance_matrix = self._build_distance_matrix()

    def _build_distance_matrix(self) -> List[List[float]]:
        """計算歐幾里得距離矩陣。"""
        matrix = []
        for i in range(self.num_cities):
            row = []
            for j in range(self.num_cities):
                dx = self.cities[i][0] - self.cities[j][0]
                dy = self.cities[i][1] - self.cities[j][1]
                row.append(math.sqrt(dx * dx + dy * dy))
            matrix.append(row)
        return matrix

    def compute_tour_distance(self, tour: List[int]) -> float:
        """計算給定巡迴路徑的總距離。"""
        dist = 0.0
        for i in range(self.num_cities):
            u = tour[i]
            v = tour[(i + 1) % self.num_cities]
            dist += self.distance_matrix[u][v]
        return dist


# ==========================================
# 1. 貪婪演算法 (Greedy Algorithm / Nearest Neighbor)
# ==========================================
def greedy_nearest_neighbor(tsp: TSPProblem, start_city: int = 0) -> Tuple[List[int], float]:
    """
    貪婪演算法 (最近鄰居法):
    從起點城市開始，每次選擇距離當前城市最近且尚未造訪的城市。
    """
    unvisited = set(range(tsp.num_cities))
    current_city = start_city
    tour = [current_city]
    unvisited.remove(current_city)

    while unvisited:
        next_city = min(unvisited, key=lambda city: tsp.distance_matrix[current_city][city])
        tour.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city

    return tour, tsp.compute_tour_distance(tour)


# ==========================================
# 2. 改良法 (Improvement Method / 2-Opt Heuristic)
# ==========================================
def two_opt_improvement(tsp: TSPProblem, initial_tour: List[int] = None) -> Tuple[List[int], float]:
    """
    改良法 (2-Opt 反轉法):
    從初始解出發，不斷檢查反轉子路徑 segments 能否降低總距離。
    若能改進則立即更新，直到無法再進行任何 2-Opt 改善為止。
    """
    if initial_tour is None:
        tour = list(range(tsp.num_cities))
        random.shuffle(tour)
    else:
        tour = list(initial_tour)

    improved = True
    n = tsp.num_cities

    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue  # 跳過起點與終點相連的無效交換
                
                # 計算 2-Opt 邊交換後的距離變化量 ΔCost
                u1, v1 = tour[i], tour[i + 1]
                u2, v2 = tour[j], tour[(j + 1) % n]
                
                old_dist = tsp.distance_matrix[u1][v1] + tsp.distance_matrix[u2][v2]
                new_dist = tsp.distance_matrix[u1][u2] + tsp.distance_matrix[v1][v2]

                if new_dist < old_dist:
                    # 反轉 [i+1 ... j] 區間
                    tour[i + 1 : j + 1] = reversed(tour[i + 1 : j + 1])
                    improved = True
                    break
            if improved:
                break

    return tour, tsp.compute_tour_distance(tour)


# ==========================================
# 3. 爬山演算法 (Hill Climbing Algorithm)
# ==========================================
def hill_climbing(tsp: TSPProblem, initial_tour: List[int] = None) -> Tuple[List[int], float]:
    """
    爬山演算法 (首勝 local search / First-Choice Hill Climbing):
    隨機隨機探索鄰域（如兩點對調 swap），一旦發現更優解（距離更短）就移動，
    若達到局部最佳解（周圍鄰居皆無改善）則停止。
    """
    if initial_tour is None:
        current_tour = list(range(tsp.num_cities))
        random.shuffle(current_tour)
    else:
        current_tour = list(initial_tour)

    current_dist = tsp.compute_tour_distance(current_tour)
    n = tsp.num_cities

    while True:
        improved = False
        # 探索 2-swap 鄰域
        neighbors_indices = [(i, j) for i in range(n) for j in range(i + 1, n)]
        random.shuffle(neighbors_indices)  # 隨機打亂鄰域探索順序

        for i, j in neighbors_indices:
            neighbor = list(current_tour)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbor_dist = tsp.compute_tour_distance(neighbor)

            if neighbor_dist < current_dist:
                current_tour = neighbor
                current_dist = neighbor_dist
                improved = True
                break  # 首勝策略：找到第一個更好的解就更新

        if not improved:
            break  # 無法找到更好的鄰居，終止於局部最佳解

    return current_tour, current_dist


# ==========================================
# 4. 梯度下降法 (Steepest Discrete Gradient Descent)
# ==========================================
def steepest_gradient_descent(tsp: TSPProblem, initial_tour: List[int] = None) -> Tuple[List[int], float]:
    """
    梯度下降法 (離散極速下降法 / Steepest Descent):
    對於組合優化問題，將「離散梯度」定義為每個鄰域動作導致的代價變化量 ΔCost。
    在每一步計算鄰域中所有可能的變更方向，並沿著下降幅度最大（負梯度最大）的方向移動。
    """
    if initial_tour is None:
        current_tour = list(range(tsp.num_cities))
        random.shuffle(current_tour)
    else:
        current_tour = list(initial_tour)

    current_dist = tsp.compute_tour_distance(current_tour)
    n = tsp.num_cities

    while True:
        best_gradient = 0.0  # 代價下降量
        best_move = None

        # 計算整個鄰域中所有方向的離散梯度
        for i in range(n - 1):
            for j in range(i + 2, n):
                if i == 0 and j == n - 1:
                    continue
                
                u1, v1 = current_tour[i], current_tour[i + 1]
                u2, v2 = current_tour[j], current_tour[(j + 1) % n]
                
                # 計算梯度 = -ΔCost = (舊距離 - 新距離)
                delta_dist = (tsp.distance_matrix[u1][v1] + tsp.distance_matrix[u2][v2]) - \
                             (tsp.distance_matrix[u1][u2] + tsp.distance_matrix[v1][v2])

                if delta_dist > best_gradient:
                    best_gradient = delta_dist
                    best_move = (i, j)

        # 若存在陡峭下降方向，則沿著最大負梯度方向更新解
        if best_move is not None:
            i, j = best_move
            current_tour[i + 1 : j + 1] = reversed(current_tour[i + 1 : j + 1])
            current_dist -= best_gradient
        else:
            break  # 梯度歸零/無下降方向，收斂至局部最佳解

    return current_tour, current_dist


# ==========================================
# 5. 模擬退火法 (Simulated Annealing)
# ==========================================
def simulated_annealing(
    tsp: TSPProblem,
    initial_tour: List[int] = None,
    initial_temp: float = 1000.0,
    cooling_rate: float = 0.995,
    min_temp: float = 1e-3
) -> Tuple[List[int], float]:
    """
    模擬退火法:
    結合 Metropolis 準則，以一定機率接受較差的解以跳脫局部最佳解。
    高溫時機率高，隨著溫度降低漸漸轉為局部搜尋。
    """
    if initial_tour is None:
        current_tour = list(range(tsp.num_cities))
        random.shuffle(current_tour)
    else:
        current_tour = list(initial_tour)

    current_dist = tsp.compute_tour_distance(current_tour)
    best_tour = list(current_tour)
    best_dist = current_dist

    temp = initial_temp
    n = tsp.num_cities

    while temp > min_temp:
        # 隨機產生 2-Opt 鄰居
        i = random.randint(0, n - 2)
        j = random.randint(i + 2, n if i > 0 else n - 1)

        neighbor = list(current_tour)
        neighbor[i + 1 : j + 1] = reversed(neighbor[i + 1 : j + 1])
        neighbor_dist = tsp.compute_tour_distance(neighbor)

        delta = neighbor_dist - current_dist

        # 若新解更好，或者滿足 Metropolis 接受機率則移動
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_tour = neighbor
            current_dist = neighbor_dist

            if current_dist < best_dist:
                best_tour = list(current_tour)
                best_dist = current_dist

        # 降溫
        temp *= cooling_rate

    return best_tour, best_dist


# ==========================================
# 主程式測試與效能評比
# ==========================================
def run_benchmark():
    random.seed(42)  # 固定隨機種子以確保實驗可重複性

    num_cities = 30
    print(f"=== 生成 {num_cities} 個隨機城市測試資料 ===")
    cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_cities)]
    tsp = TSPProblem(cities)

    methods = [
        ("1. 貪婪演算法 (Greedy / Nearest Neighbor)", lambda: greedy_nearest_neighbor(tsp, start_city=0)),
        ("2. 改良法 (2-Opt Improvement)", lambda: two_opt_improvement(tsp)),
        ("3. 爬山演算法 (Hill Climbing)", lambda: hill_climbing(tsp)),
        ("4. 梯度下降法 (Steepest Gradient Descent)", lambda: steepest_gradient_descent(tsp)),
        ("5. 模擬退火法 (Simulated Annealing)", lambda: simulated_annealing(tsp)),
    ]

    results = []

    print("\n" + "=" * 65)
    print(f"{'演算法名稱':<35} | {'總距離 (Distance)':<12} | {'執行時間 (Sec)':<10}")
    print("=" * 65)

    for name, method_func in methods:
        start_time = time.time()
        tour, distance = method_func()
        exec_time = time.time() - start_time
        
        results.append((name, distance, exec_time))
        print(f"{name:<35} | {distance:<17.2f} | {exec_time:<10.4f}")

    print("=" * 65)


if __name__ == "__main__":
    run_benchmark()