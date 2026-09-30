import itertools
import re

def extract_variables(formula_str):
    """
    從邏輯運算式中自動提取所有變數名稱（過濾 Python 布爾關鍵字）
    """
    keywords = {'and', 'or', 'not', 'True', 'False', '(', ')'}
    tokens = re.findall(r'\b[a-zA-Z_]\w*\b', formula_str)
    variables = sorted(list(set(tokens) - keywords))
    return variables

def solve_sat_brute_force(formula_str, print_table=True):
    """
    使用窮舉真值表法解決 SAT 問題
    """
    variables = extract_variables(formula_str)
    n = len(variables)
    
    if n == 0:
        print("錯誤：未檢測到有效的布爾變數！")
        return

    print(f"邏輯運算式 : {formula_str}")
    print(f"提取變數    : {variables} (共 {n} 個變數，真值表列數為 2^{n} = {2**n})\n")

    header = " | ".join(variables) + " | Result"
    separator = "-" * len(header)
    
    if print_table:
        print(header)
        print(separator)

    satisfying_assignments = []
    

    for values in itertools.product([False, True], repeat=n):
 
        assignment = dict(zip(variables, values))
 
        try:
            result = bool(eval(formula_str, {}, assignment))
        except Exception as e:
            print(f"運算式求值錯誤 : {e}")
            return

        if print_table:
            row_str = " | ".join(f"{str(assignment[var]):<5}" for var in variables)
            res_str = "1 (SAT)" if result else "0"
            print(f"{row_str} | {res_str}")

        if result:
            satisfying_assignments.append(assignment)

    if print_table:
        print(separator)


    print("\n[求解結果]")
    if satisfying_assignments:
        print(f" Status: SATISFIABLE (可滿足)")
        print(f" 找到 {len(satisfying_assignments)} 組可滿足的解：")
        for idx, assign in enumerate(satisfying_assignments, 1):
            formatted_assign = ", ".join(f"{k}={v}" for k, v in assign.items())
            print(f"   解 {idx}: {formatted_assign}")
    else:
        print(" Status: UNSATISFIABLE (不可滿足)")
        print(" 找不到任何一組賦值能使運算式為 True。")

if __name__ == "__main__":
    print("==================================================")
    print(" 測試 1：可滿足問題 (SAT)")
    print(" Formula: (A or B) and (not A or C) and (not B or not C)")
    print("==================================================")
    formula_1 = "(A or B) and (not A or C) and (not B or not C)"
    solve_sat_brute_force(formula_1, print_table=True)

    print("\n" + "="*50)
    print(" 測試 2：不可滿足問題 (UNSAT)")
    print(" Formula: A and not A")
    print("==================================================")
    formula_2 = "A and not A"
    solve_sat_brute_force(formula_2, print_table=True)