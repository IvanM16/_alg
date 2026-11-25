from typing import Dict, Tuple, List, Callable, Any


# =====================================================================
# 1. 有限狀態機 (Deterministic Finite Automaton, DFA)
# 對應書中章節：05-喬姆斯基的語法 (Chomsky Hierarchy - Type 3 正規語言)
# =====================================================================
class DFA:
    """確定性有限狀態自動機：識別包含偶數個 '1' 的二進位字串"""

    def __init__(self):
        self.states = {'q_even', 'q_odd'}
        self.alphabet = {'0', '1'}
        self.start_state = 'q_even'
        self.accept_states = {'q_even'}
        self.transitions: Dict[Tuple[str, str], str] = {
            ('q_even', '0'): 'q_even',
            ('q_even', '1'): 'q_odd',
            ('q_odd', '0'): 'q_odd',
            ('q_odd', '1'): 'q_even',
        }

    def accepts(self, input_str: str) -> bool:
        current_state = self.start_state
        for symbol in input_str:
            if symbol not in self.alphabet:
                raise ValueError(f"非法字元 '{symbol}'，不在字母表 {self.alphabet} 中")
            current_state = self.transitions[(current_state, symbol)]
        return current_state in self.accept_states


# =====================================================================
# 2. 丘奇的函數：Lambda 演算與 Y 組合子 (Y Combinator)
# 對應書中章節：03-丘奇的函數 (Church's Lambda Calculus)
# =====================================================================
# 嚴格求值 (Call-by-value) 下的 Z 組合子（Y 組合子的變體，適用於 Python）
Z = lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v)))

# 使用純匿名函數實現階乘 (Factorial)，完全不使用 def 或函數名稱自我呼叫
factorial_step = lambda f: lambda n: 1 if n == 0 else n * f(n - 1)
lambda_factorial = Z(factorial_step)


# =====================================================================
# 3. 圖靈機模擬器 (Turing Machine Simulator)
# 對應書中章節：04-圖靈的機器 (Turing's Machine)
# =====================================================================
class TuringMachine:
    """單帶圖靈機模擬器：實作二進位數加 1 (Binary Incrementer)"""

    def __init__(self, tape: str, blank: str = '_'):
        self.tape: List[str] = list(tape) if tape else [blank]
        self.blank = blank
        self.head = 0
        self.state = 'MOVE_RIGHT'
        # 轉移函數: (當前狀態, 讀取符號) -> (新狀態, 寫入符號, 移動方向 'L'/'R'/'S')
        self.transitions: Dict[Tuple[str, str], Tuple[str, str, str]] = {
            # 第一階段：向右移動到數字最右端（最低位元）
            ('MOVE_RIGHT', '0'): ('MOVE_RIGHT', '0', 'R'),
            ('MOVE_RIGHT', '1'): ('MOVE_RIGHT', '1', 'R'),
            ('MOVE_RIGHT', '_'): ('ADD_CARRY', '_', 'L'),
            # 第二階段：從右向左進行加 1 與進位處理
            ('ADD_CARRY', '0'): ('HALT', '1', 'S'),       # 遇 0 變 1，進位結束，停機
            ('ADD_CARRY', '1'): ('ADD_CARRY', '0', 'L'),  # 遇 1 變 0，繼續向左進位
            ('ADD_CARRY', '_'): ('HALT', '1', 'S'),       # 最高位仍進位，補 1 並停機
        }

    def step(self) -> bool:
        if self.state == 'HALT':
            return False

        # 若讀寫頭超出紙帶邊界，自動擴展空白符號
        if self.head < 0:
            self.tape.insert(0, self.blank)
            self.head = 0
        elif self.head >= len(self.tape):
            self.tape.append(self.blank)

        current_symbol = self.tape[self.head]
        action = self.transitions.get((self.state, current_symbol))
        if action is None:
            raise RuntimeError(f"未定義的狀態轉移: ({self.state}, {current_symbol})")

        next_state, write_symbol, direction = action
        self.tape[self.head] = write_symbol
        self.state = next_state

        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1

        return self.state != 'HALT'

    def run(self, max_steps: int = 1000) -> str:
        steps = 0
        while self.step():
            steps += 1
            if steps >= max_steps:
                raise RuntimeError("超過最大步數限制（可能進入無窮迴圈）")
        return ''.join(self.tape).strip(self.blank)


# =====================================================================
# 4. 圖靈停機問題 (Halting Problem) 悖論演示
# 對應書中章節：01-希爾伯特的問題、02-哥德爾的定理、04-圖靈的機器
# =====================================================================
class HaltingParadoxDemo:
    """
    透過反證法演示為何不存在通用的停機判定器 halts(program, input)。
    """

    @staticmethod
    def hypothetical_halts(program: Callable[[Any], Any], inp: Any) -> bool:
        """
        假設存在一個神諭函數能判斷 program(inp) 是否會停機。
        （此處僅作邏輯推演示意，實際上此函數無法被實作出來）
        """
        raise NotImplementedError("圖靈已證明：通用的停機判定函數在邏輯上不可能存在！")

    @staticmethod
    def paradox_machine(program: Callable[[Any], Any]):
        """
        圖靈構造的對角線悖論機器 D(P)：
        如果 P(P) 會停機，D(P) 就故意進入無窮迴圈；
        如果 P(P) 不會停機，D(P) 就立刻停機。
        當我們呼叫 D(D) 時，就會產生「停機 <=> 不停機」的邏輯矛盾！
        """
        print("當嘗試對 paradox_machine 自身進行停機判定時：")
        print("  - 若判定 D(D) 會停機 -> D(D) 根據定義會進入無窮迴圈（矛盾！）")
        print("  - 若判定 D(D) 不會停機 -> D(D) 根據定義會立刻停機（矛盾！）")
        print("結論：希爾伯特的『判定性問題 (Entscheidungsproblem)』答案為否定！")


def main():
    print("=" * 60)
    print("第12週習題：計算理論核心概念程式演示")
    print("=" * 60)

    # 1. 測試 DFA
    print("\n[1] 喬姆斯基語法與有限狀態機 (DFA - 偶數個 '1' 檢查器)")
    dfa = DFA()
    test_strings = ["1010", "111", "0000", "11011"]
    for s in test_strings:
        print(f"  輸入字串 '{s}' -> 是否接受 (偶數個 1): {dfa.accepts(s)}")

    # 2. 測試 Lambda 演算
    print("\n[2] 丘奇的函數 (Lambda 演算 + Z 組合子計算階乘)")
    for n in range(6):
        print(f"  {n}! = {lambda_factorial(n)}")

    # 3. 測試圖靈機
    print("\n[3] 圖靈機模擬 (二進位加法器: N + 1)")
    binary_inputs = ["1011", "111", "0"]
    for b in binary_inputs:
        tm = TuringMachine(b)
        result = tm.run()
        print(f"  輸入紙帶: {b} (十進位 {int(b, 2)}) -> 輸出紙帶: {result} (十進位 {int(result, 2)})")

    # 4. 展示停機問題
    print("\n[4] 計算的極限：圖靈停機問題 (Halting Problem)")
    HaltingParadoxDemo.paradox_machine(HaltingParadoxDemo.paradox_machine)


if __name__ == "__main__":
    main()