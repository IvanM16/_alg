"""
Advanced Search Algorithms Collection
1. Rat in a Maze (DFS)
2. Wolf, Goat, Cabbage River Crossing (BFS)
3. 8-Queens Problem (DFS / Backtracking)
4. NPC Pathfinding (A* Search)
5. IC Circuit Routing (Lee's Algorithm / Wavefront BFS)
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Set, Dict
import heapq
from collections import deque


# ======================================================================
# 1. 老鼠走迷宮問題 (Rat in a Maze - DFS)
# ======================================================================
class MazeSolverDFS:
    """使用深度優先搜尋 (DFS) 與回溯法 (Backtracking) 解老鼠走迷宮問題。"""

    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    def solve(self, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        visited: Set[Tuple[int, int]] = set()
        path: List[Tuple[int, int]] = []

        def dfs(r: int, c: int) -> bool:
            # 邊界與障礙物檢查
            if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                return False
            if self.grid[r][c] == 1 or (r, c) in visited:
                return False

            visited.add((r, c))
            path.append((r, c))

            if (r, c) == end:
                return True

            # 探索 4 個方向：下、右、上、左
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for dr, dc in directions:
                if dfs(r + dr, c + dc):
                    return True

            # 回溯 (Backtrack)
            path.pop()
            return False

        if dfs(start[0], start[1]):
            return path
        return None

    def render(self, path: Optional[List[Tuple[int, int]]] = None) -> str:
        """將迷宮與路徑繪製為 ASCII 字串。"""
        path_set = set(path) if path else set()
        lines = []
        for r in range(self.rows):
            line = []
            for c in range(self.cols):
                if (r, c) in path_set:
                    line.append("*")  # 路徑標示
                elif self.grid[r][c] == 1:
                    line.append("#")  # 牆壁
                else:
                    line.append(".")  # 平地
            lines.append(" ".join(line))
        return "\n".join(lines)


# ======================================================================
# 2. 狼羊甘藍菜過河問題 (Wolf, Goat, Cabbage - BFS)
# ======================================================================
# 狀態標示：(農夫, 狼, 羊, 甘藍菜) -> 0 代表左岸，1 代表右岸
State = Tuple[int, int, int, int]


class RiverCrossingBFS:
    """使用廣度優先搜尋 (BFS) 尋找狼羊甘藍菜過河的最佳（最少步數）解法。"""

    NAMES = ["農夫", "狼", "羊", "甘藍菜"]

    @staticmethod
    def is_valid(state: State) -> bool:
        f, w, g, c = state
        # 狼與羊單獨留在一起（農夫不在）
        if w == g and f != w:
            return False
        # 羊與甘藍菜單獨留在一起（農夫不在）
        if g == c and f != g:
            return False
        return True

    def solve(self) -> Optional[List[State]]:
        start_state: State = (0, 0, 0, 0)
        target_state: State = (1, 1, 1, 1)

        queue = deque([(start_state, [start_state])])
        visited = {start_state}

        while queue:
            curr_state, path = queue.popleft()
            if curr_state == target_state:
                return path

            f, w, g, c = curr_state

            # 農夫可以獨自過河，或攜帶同岸的一件物品
            items_to_move = [None]  # 農夫單獨
            items = [w, g, c]
            item_indices = [1, 2, 3]

            for idx, side in zip(item_indices, items):
                if side == f:
                    items_to_move.append(idx)

            for item in items_to_move:
                next_f = 1 - f
                next_w = 1 - w if item == 1 else w
                next_g = 1 - g if item == 2 else g
                next_c = 1 - c if item == 3 else c

                next_state: State = (next_f, next_w, next_g, next_c)

                if self.is_valid(next_state) and next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [next_state]))

        return None

    def format_path(self, path: List[State]) -> List[str]:
        """格式化輸出每一步驟。"""
        steps = []
        for i in range(len(path) - 1):
            curr, nxt = path[i], path[i + 1]
            moved = []
            for j in range(4):
                if curr[j] != nxt[j]:
                    moved.append(self.NAMES[j])
            direction = "左岸 ➔ 右岸" if nxt[0] == 1 else "右岸 ➔ 左岸"
            steps.append(f"步驟 {i+1}: 帶着 [{' & '.join(moved)}] ({direction})")
        return steps


# ======================================================================
# 3. 八皇后問題 (8-Queens Problem - DFS / Backtracking)
# ======================================================================
class NQueensDFS:
    """使用 DFS 回溯演算法解 N-Queens 問題（預設 8 皇后）。"""

    def __init__(self, n: int = 8):
        self.n = n

    def solve_all(self) -> List[List[int]]:
        """回傳所有解法列表，每個解法包含各行皇后所在的欄位索引。"""
        solutions = []
        board = [-1] * self.n

        cols: Set[int] = set()
        diag1: Set[int] = set()  # 主對角線 r - c
        diag2: Set[int] = set()  # 反對角線 r + c

        def backtrack(row: int):
            if row == self.n:
                solutions.append(list(board))
                return

            for col in range(self.n):
                if col in cols or (row - col) in diag1 or (row + col) in diag2:
                    continue

                cols.add(col)
                diag1.add(row - col)
                diag2.add(row + col)
                board[row] = col

                backtrack(row + 1)

                # 回溯
                cols.remove(col)
                diag1.remove(row - col)
                diag2.remove(row + col)
                board[row] = -1

        backtrack(0)
        return solutions

    def render_board(self, solution: List[int]) -> str:
        lines = []
        for col in solution:
            row_str = ["."] * self.n
            row_str[col] = "Q"
            lines.append(" ".join(row_str))
        return "\n".join(lines)


# ======================================================================
# 4. NPC 搜尋玩家問題 (NPC Pathfinding - A* Search)
# ======================================================================
@dataclass(order=True)
class PrioritizedNode:
    f_score: float
    position: Tuple[int, int] = field(compare=False)


class NPCPathfinderAStar:
    """在具備地形移動成本的 2D 網格上，使用 A* 搜尋演算法尋找最佳路徑。"""

    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    def _heuristic(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        # 使用 曼哈頓距離 (Manhattan Distance) 作為啟發式估計值
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def find_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        open_set: List[PrioritizedNode] = []
        heapq.heappush(open_set, PrioritizedNode(0.0, start))

        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {start: 0.0}

        while open_set:
            current = heapq.heappop(open_set).position

            if current == target:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dr, dc in directions:
                neighbor = (current[0] + dr, current[1] + dc)
                r, c = neighbor

                if 0 <= r < self.rows and 0 <= c < self.cols:
                    cost = self.grid[r][c]
                    if cost < 0:  # < 0 代表無法採踏的障礙物/牆壁
                        continue

                    tentative_g = g_score[current] + cost
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g
                        f_score = tentative_g + self._heuristic(neighbor, target)
                        heapq.heappush(open_set, PrioritizedNode(f_score, neighbor))

        return None

    def render(self, path: Optional[List[Tuple[int, int]]] = None) -> str:
        path_set = set(path) if path else set()
        lines = []
        for r in range(self.rows):
            line = []
            for c in range(self.cols):
                if (r, c) in path_set:
                    line.append("P")  # NPC 路徑標示
                elif self.grid[r][c] < 0:
                    line.append("X")  # 障礙物
                else:
                    line.append(str(self.grid[r][c]))  # 耗費成本
            lines.append(" ".join(line))
        return "\n".join(lines)


# ======================================================================
# 5. IC 設計電路繞線問題 (IC Circuit Routing - Lee's Maze Router)
# ======================================================================
class ICCircuitRouter:
    """
    IC 電路網格繞線演算法：Lee's Algorithm (Wavefront Expansion)。
    使用波前擴展搜尋確保點對點最短布線，將已布線路徑標記為後續 Net 的障礙物。
    """

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        # 0: 空白可通行, -1: 障礙物/晶片巨集, >0: 已繞線的 Net ID
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def add_obstacle(self, r: int, c: int):
        self.grid[r][c] = -1

    def route_net(self, net_id: int, pin_a: Tuple[int, int], pin_b: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if pin_a == pin_b:
            return [pin_a]

        wave = [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        queue = deque([pin_a])
        wave[pin_a[0]][pin_a[1]] = 0

        found = False
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # 步驟一：波前擴展 (Wavefront Expansion / BFS Fill)
        while queue:
            r, c = queue.popleft()
            curr_dist = wave[r][c]

            if (r, c) == pin_b:
                found = True
                break

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if (self.grid[nr][nc] == 0 or (nr, nc) == pin_b) and wave[nr][nc] == -1:
                        wave[nr][nc] = curr_dist + 1
                        queue.append((nr, nc))

        if not found:
            return None

        # 步驟二：回溯構建導線 (Backtracking / Retrace)
        path = [pin_b]
        curr = pin_b
        while curr != pin_a:
            r, c = curr
            curr_dist = wave[r][c]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and wave[nr][nc] == curr_dist - 1:
                    curr = (nr, nc)
                    path.append(curr)
                    break

        path.reverse()

        # 將此 Net 路線更新回全域網格
        for r, c in path:
            self.grid[r][c] = net_id

        return path

    def render_grid(self) -> str:
        lines = []
        for r in range(self.rows):
            line = []
            for c in range(self.cols):
                val = self.grid[r][c]
                if val == -1:
                    line.append(" X ")
                elif val == 0:
                    line.append(" . ")
                else:
                    line.append(f"N{val:<2}")
            lines.append("".join(line))
        return "\n".join(lines)


# ======================================================================
# 主測試程式 (Main Demonstration)
# ======================================================================
def main():
    print("=" * 65)
    print("1. 老鼠走迷宮問題 (Rat in a Maze - DFS)")
    print("=" * 65)
    maze_grid = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
    ]
    maze_solver = MazeSolverDFS(maze_grid)
    maze_path = maze_solver.solve((0, 0), (4, 4))
    print(f"解出路徑 (長度 {len(maze_path) if maze_path else 0}): {maze_path}")
    print(maze_solver.render(maze_path))

    print("\n" + "=" * 65)
    print("2. 狼羊甘藍菜過河問題 (Wolf, Goat, Cabbage - BFS)")
    print("=" * 65)
    river_solver = RiverCrossingBFS()
    river_path = river_solver.solve()
    if river_path:
        for step in river_solver.format_path(river_path):
            print(step)

    print("\n" + "=" * 65)
    print("3. 八皇后問題 (8-Queens - DFS / Backtracking)")
    print("=" * 65)
    queens_solver = NQueensDFS(8)
    solutions = queens_solver.solve_all()
    print(f"8 皇后問題總共獲得 {len(solutions)} 組可行解。")
    print("第一組解的可視化棋盤：")
    print(queens_solver.render_board(solutions[0]))

    print("\n" + "=" * 65)
    print("4. NPC 搜尋玩家問題 (NPC Pathfinding - A* Search)")
    print("=" * 65)
    # 數字代表地形移動代價 (1=平地, 3=泥濘), -1代表牆壁
    terrain_grid = [
        [1, 1, 1, 1, 1],
        [-1, -1, 3, -1, 1],
        [1, 1, 3, 1, 1],
        [1, -1, -1, -1, 1],
        [1, 1, 1, 1, 1],
    ]
    npc_solver = NPCPathfinderAStar(terrain_grid)
    start_pos, target_pos = (0, 0), (4, 4)
    path = npc_solver.find_path(start_pos, target_pos)
    print(f"NPC 最佳路徑: {path}")
    print(npc_solver.render(path))

    print("\n" + "=" * 65)
    print("5. IC 設計中的電路繞線問題 (IC Circuit Routing - Lee's Algorithm)")
    print("=" * 65)
    router = ICCircuitRouter(6, 6)
    router.add_obstacle(2, 2)
    router.add_obstacle(2, 3)

    net1_path = router.route_net(1, (0, 0), (4, 4))
    net2_path = router.route_net(2, (0, 5), (5, 0))
    print(f"Net 1 繞線結果 (長度 {len(net1_path) if net1_path else '失敗'}): {net1_path}")
    print(f"Net 2 繞線結果 (長度 {len(net2_path) if net2_path else '失敗'}): {net2_path}")
    print("晶片網格繞線圖:")
    print(router.render_grid())


if __name__ == "__main__":
    main()