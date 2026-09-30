class IterativeFramework:
    def __init__(self, step_func, stop_func, max_iter=1000):
        """
        初始化通用迭代框架
        
        :param step_func: Callable[[State], State] -> 單步狀態轉移邏輯
        :param stop_func: Callable[[State, State, int], bool] -> 終止檢測邏輯
        :param max_iter:  int -> 最大迭代次數限制
        """
        self.step_func = step_func
        self.stop_func = stop_func
        self.max_iter = max_iter

    def run(self, initial_state):
        """
        執行迭代主流程
        
        :param initial_state: 初始狀態 x_0
        :return: (最終狀態, 總迭代次數)
        """
        state = initial_state
        for iter_count in range(1, self.max_iter + 1):
            next_state = self.step_func(state)
            
            # 檢查是否滿足自訂終止條件
            if self.stop_func(state, next_state, iter_count):
                return next_state, iter_count
                
            state = next_state
            
        print(f"Warning: Reached maximum iterations ({self.max_iter}) without full convergence.")
        return state, self.max_iter