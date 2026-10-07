

def sym_diff(expr, var='x'):
   

    if isinstance(expr, (int, float)):
        return 0
    
    
    if isinstance(expr, str):
        return 1 if expr == var else 0


    op = expr[0]

    
    if op == '+':
        return simplify(('+', sym_diff(expr[1], var), sym_diff(expr[2], var)))

    
    elif op == '-':
        if len(expr) == 2:  # Negation -u
            return simplify(('-', sym_diff(expr[1], var)))
        return simplify(('-', sym_diff(expr[1], var), sym_diff(expr[2], var)))

   
    elif op == '*':
        u, v = expr[1], expr[2]
        du, dv = sym_diff(u, var), sym_diff(v, var)
        return simplify(('+', ('*', du, v), ('*', u, dv)))

    
    elif op == '/':
        u, v = expr[1], expr[2]
        du, dv = sym_diff(u, var), sym_diff(v, var)
        return simplify(('/', ('-', ('*', du, v), ('*', u, dv)), ('**', v, 2)))

    
    elif op == '**':
        u, n = expr[1], expr[2]
        if isinstance(n, (int, float)):
            du = sym_diff(u, var)
            return simplify(('*', ('*', n, ('**', u, n - 1)), du))
        raise NotImplementedError("General functional exponentiation u^v is not supported.")

    
    elif op == 'sin':
        u = expr[1]
        return simplify(('*', ('cos', u), sym_diff(u, var)))

   
    elif op == 'cos':
        u = expr[1]
        return simplify(('*', ('-', ('sin', u)), sym_diff(u, var)))

    
    elif op == 'exp':
        u = expr[1]
        return simplify(('*', ('exp', u), sym_diff(u, var)))

   
    elif op == 'ln':
        u = expr[1]
        return simplify(('/', sym_diff(u, var), u))

    raise ValueError(f"Unsupported mathematical operator: {op}")


def simplify(expr):
    """
    Recursively simplifies the expression tree using constant folding 
    and basic algebraic identities.
    """
    if not isinstance(expr, tuple):
        return expr

    op = expr[0]

    
    if len(expr) == 2:
        arg = simplify(expr[1])
        if op == '-':
            if isinstance(arg, (int, float)): return -arg
            if isinstance(arg, tuple) and arg[0] == '-': return arg[1]  # -(-x) -> x
        return (op, arg)

    left = simplify(expr[1])
    right = simplify(expr[2])

    
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/':
            if right == 0: raise ZeroDivisionError("Division by zero in simplification")
            return left // right if isinstance(left, int) and isinstance(right, int) and left % right == 0 else left / right
        if op == '**': return left ** right

   
    if op == '+':
        if left == 0: return right
        if right == 0: return left
    elif op == '-':
        if right == 0: return left
        if left == right: return 0
    elif op == '*':
        if left == 0 or right == 0: return 0
        if left == 1: return right
        if right == 1: return left
      
        if isinstance(left, (int, float)) and isinstance(right, tuple) and right[0] == '*' and isinstance(right[1], (int, float)):
            return simplify(('*', left * right[1], right[2]))
    elif op == '/':
        if left == 0: return 0
        if right == 1: return left
        if left == right: return 1
    elif op == '**':
        if right == 0: return 1
        if right == 1: return left
        if left == 0: return 0
        if left == 1: return 1

    return (op, left, right)


def expr_to_str(expr):
    """
    Formats the AST expression tuple into a human-readable infix mathematical string.
    """
    if not isinstance(expr, tuple):
        return str(expr)
    op = expr[0]
    if len(expr) == 2:
        return f"-({expr_to_str(expr[1])})" if op == '-' else f"{op}({expr_to_str(expr[1])})"
    left_str = expr_to_str(expr[1])
    right_str = expr_to_str(expr[2])
    return f"({left_str} {op} {right_str})"


if __name__ == "__main__":
    print("==================================================")
    print("      Recursive Symbolic Differentiation Test     ")
    print("==================================================")

    test_expressions = [
       
        ('+', ('+', ('*', 3, ('**', 'x', 2)), ('*', 2, 'x')), 5),
        
        
        ('sin', ('**', 'x', 2)),
        
       
        ('cos', 'x'),
        
        
        ('exp', ('*', 3, 'x')),
        
        
        ('*', 'x', ('ln', 'x')),
        
        
        ('/', ('*', 2, 'x'), ('+', 'x', 1))
    ]

    for i, expr in enumerate(test_expressions, 1):
        d_expr = sym_diff(expr, var='x')
        print(f"[{i}] Original  f(x)  = {expr_to_str(expr)}")
        print(f"    Derivative f'(x) = {expr_to_str(d_expr)}")
        print(f"    AST Tuple        = {d_expr}")
        print("-" * 50)