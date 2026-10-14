#!/usr/bin/env python3
"""
Lambda Calculus Interpreter (無類型 Lambda 運算解譯器)
支援功能：
1. 語法解析 (Parser & Lexer) - 支援 \\ 或 λ 符號、括號與組合子巨集定義。
2. Capture-avoiding Substitution - 防止變數綁定衝突（包含 $\alpha$-conversion 換名機制）。
3. Step-by-Step Normal Order Reduction (正規序 $\beta$-規約) - 顯示每一步的計算過程。
4. 內建 Church Encodings 程式庫（邏輯邏輯、Church 數值與算術運算）。
"""

import re
import sys



class Term:
    """Lambda 運算式的抽象基底類別"""
    pass

class Var(Term):
    """變數 (Variable): e.g., x"""
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

class Abs(Term):
    """抽象/函數定義 (Abstraction): e.g., \x. E"""
    def __init__(self, param: str, body: Term):
        self.param = param
        self.body = body

    def __repr__(self):
        return f"(\\ {self.param}. {self.body})"

    def __eq__(self, other):
        return isinstance(other, Abs) and self.param == other.param and self.body == other.body

class App(Term):
    """應用/函數呼叫 (Application): e.g., (E1 E2)"""
    def __init__(self, fn: Term, arg: Term):
        self.fn = fn
        self.arg = arg

    def __repr__(self):
        return f"({self.fn} {self.arg})"

    def __eq__(self, other):
        return isinstance(other, App) and self.fn == other.fn and self.arg == other.arg



def free_vars(term: Term) -> set:
    """計算語法樹中的所有自由變數 (Free Variables)"""
    if isinstance(term, Var):
        return {term.name}
    elif isinstance(term, Abs):
        return free_vars(term.body) - {term.param}
    elif isinstance(term, App):
        return free_vars(term.fn) | free_vars(term.arg)
    return set()

def fresh_var(base: str, forbidden: set) -> str:
    """產生不會與 forbidden 集合衝突的新變數名稱 (Alpha-conversion 換名用)"""
    counter = 1
    new_var = f"{base}'"
    while new_var in forbidden:
        counter += 1
        new_var = f"{base}{counter}"
    return new_var

def substitute(term: Term, var_name: str, replacement: Term) -> Term:
    """
    捕獲迴避的代換 [replacement / var_name] term
    規避 Variable Capture 問題
    """
    if isinstance(term, Var):
        if term.name == var_name:
            return replacement
        return term

    elif isinstance(term, Abs):
       
        if term.param == var_name:
            return term
        
        
        if term.param in free_vars(replacement):
            forbidden = free_vars(term.body) | free_vars(replacement) | {var_name}
            new_param = fresh_var(term.param, forbidden)
            renamed_body = substitute(term.body, term.param, Var(new_param))
            return Abs(new_param, substitute(renamed_body, var_name, replacement))
        else:
            return Abs(term.param, substitute(term.body, var_name, replacement))

    elif isinstance(term, App):
        return App(
            substitute(term.fn, var_name, replacement),
            substitute(term.arg, var_name, replacement)
        )

    return term




def step_reduce(term: Term) -> tuple[Term, bool]:
    """
    單步規約 (Normal Order Reduction: 外層優先/Call-by-Name)
    回傳 (新語法樹, 是否有進行規約)
    """
    if isinstance(term, App):
        
        if isinstance(term.fn, Abs):
            reduced = substitute(term.fn.body, term.fn.param, term.arg)
            return reduced, True
        
        
        fn_reduced, changed = step_reduce(term.fn)
        if changed:
            return App(fn_reduced, term.arg), True
        
       
        arg_reduced, changed = step_reduce(term.arg)
        if changed:
            return App(term.fn, arg_reduced), True
        
        return term, False

    elif isinstance(term, Abs):
       
        body_reduced, changed = step_reduce(term.body)
        if changed:
            return Abs(term.param, body_reduced), True
        return term, False

    return term, False


def evaluate_with_trace(term: Term, max_steps: int = 50):
    """求值並輸出完整推導步驟"""
    curr = term
    print(f"[ Step 0 ] {curr}")
    
    step = 1
    while step <= max_steps:
        curr, changed = step_reduce(curr)
        if not changed:
            print(f"==> 達成正規型 (Normal Form) ，共經過 {step - 1} 步規約。\n")
            return curr
        print(f"[ Step {step} ] {curr}")
        step += 1
        
    print(f"(!) 達到最大規約步數限制 ({max_steps} 步)，可能存在無限迴圈/非終止條件。\n")
    return curr




class Lexer:
    """詞法分析器"""
    def __init__(self, code: str):
        self.code = code
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        token_specification = [
            ('LAMBDA',   r'\\|λ'),
            ('DOT',      r'\.'),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('ID',       r"[a-zA-Z_0-9']+" ),
            ('SKIP',     r'[ \t\n]+'),
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            val = mo.group()
            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise SyntaxError(f"未知的字元: {val!r}")
            else:
                self.tokens.append((kind, val))

class Parser:
    """語法分析器 (支援左結合應用與巨集展開)"""
    def __init__(self, tokens: list, env: dict = None):
        self.tokens = tokens
        self.pos = 0
        self.env = env or {}

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return (None, None)

    def consume(self, expected_kind: str = None):
        kind, val = self.peek()
        if expected_kind and kind != expected_kind:
            raise SyntaxError(f"語法錯誤: 預期 {expected_kind}，但取得 {kind} ({val})")
        self.pos += 1
        return kind, val

    def parse_expression(self) -> Term:
     
        kind, _ = self.peek()
        if kind == 'LAMBDA':
            self.consume('LAMBDA')
            _, param = self.consume('ID')
            self.consume('DOT')
            body = self.parse_expression()
            return Abs(param, body)
        return self.parse_application()

    def parse_application(self) -> Term:
    
        expr = self.parse_atom()
        while True:
            kind, _ = self.peek()
            if kind in ('LAMBDA', 'LPAREN', 'ID'):
                next_atom = self.parse_atom()
                expr = App(expr, next_atom)
            else:
                break
        return expr

    def parse_atom(self) -> Term:
        kind, val = self.peek()
        if kind == 'ID':
            self.consume('ID')
        
            if val in self.env:
                return self.env[val]
            return Var(val)
        elif kind == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        elif kind == 'LAMBDA':
            return self.parse_expression()
        else:
            raise SyntaxError(f"無法解析的語法標記: {kind} ({val})")

def parse(code: str, env: dict = None) -> Term:
    lexer = Lexer(code)
    parser = Parser(lexer.tokens, env)
    return parser.parse_expression()




def get_standard_library() -> dict:
    """初始化標準組合子庫與 Church 編碼庫"""
    env = {}
    

    env["I"] = parse("\\x. x", env)
    env["K"] = parse("\\x. \\y. x", env)
    env["S"] = parse("\\x. \\y. \\z. x z (y z)", env)


    env["TRUE"]  = parse("\\x. \\y. x", env)
    env["FALSE"] = parse("\\x. \\y. y", env)
    env["AND"]   = parse("\\p. \\q. p q p", env)
    env["OR"]    = parse("\\p. \\q. p p q", env)
    env["NOT"]   = parse("\\p. p FALSE TRUE", env)

  
    env["ZERO"]  = parse("\\f. \\x. x", env)
    env["ONE"]   = parse("\\f. \\x. f x", env)
    env["TWO"]   = parse("\\f. \\x. f (f x)", env)
    env["THREE"] = parse("\\f. \\x. f (f (f x))", env)


    env["SUCC"]  = parse("\\n. \\f. \\x. f (n f x)", env)
    env["PLUS"]  = parse("\\m. \\n. \\f. \\x. m f (n f x)", env)
    env["MULT"]  = parse("\\m. \\n. \\f. m (n f)", env)

    return env


def main():
    print("==================================================")
    print("   Lambda Calculus 解譯器 (顯示完整計算過程)      ")
    print("==================================================\n")

    env = get_standard_library()

    test_cases = [
        ("基礎 Identity 測試", "(\\x. x) a"),
        ("Alpha Conversion 避免變數捕獲測試", "(\\x. \\y. x y) y"),
        ("Church 邏輯布林運算 (AND TRUE FALSE)", "AND TRUE FALSE"),
        ("Church 數字加法 (SUCC ONE -> TWO)", "SUCC ONE"),
        ("Church 數字加法 (PLUS ONE TWO -> THREE)", "PLUS ONE TWO"),
        ("Church 數字乘法 (MULT TWO TWO)", "MULT TWO TWO"),
    ]

    for title, expr_str in test_cases:
        print(f"------ [測試項目] {title} ------")
        print(f"輸入表達式: {expr_str}")
        parsed_term = parse(expr_str, env)
        print(f"巨集展開後 AST: {parsed_term}")
        print("計算推導步驟:")
        evaluate_with_trace(parsed_term)
        print("-" * 50 + "\n")

if __name__ == "__main__":
    main()