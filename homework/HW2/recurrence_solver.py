import math
import time
import sys


sys.setrecursionlimit(5000)

def T1_recursive(n):
    if n <= 1:
        return 1
    return T1_recursive(n - 1) + 8

def T1_exact(n):
    return 8 * n - 7


def T2_recursive(n):
    if n <= 1:
        return 1
    return 2 * T2_recursive(n - 1) + 9

def T2_exact(n):
    return 5 * (2 ** n) - 9



def T3_recursive(n):
    if n <= 1:
        return 1
    return 2 * T3_recursive(n // 2) + 1

def T3_exact(n):
    return 2 * n - 1


def T4_recursive(n):
    if n <= 1:
        return 1
    return T4_recursive(n // 2) + 1

def T4_exact(n):
    return int(math.log2(n)) + 1


def run_verification():
    print("=" * 70)
    print(" VERIFYING RECURRENCE FORMULAS AGAINST EXACT CLOSED-FORM SOLUTIONS")
    print("=" * 70)

    print("\n--- Equation 1: T(n) = T(n-1) + 8  |  O(n) ---")
    for n in [1, 5, 10, 100]:
        rec_val = T1_recursive(n)
        ext_val = T1_exact(n)
        print(f"n = {n:<4} | Recursive: {rec_val:<6} | Exact: {ext_val:<6} | Match: {rec_val == ext_val}")

   
    print("\n--- Equation 2: T(n) = 2T(n-1) + 9  |  O(2^n) ---")
    for n in [1, 5, 10, 20]:
        rec_val = T2_recursive(n)
        ext_val = T2_exact(n)
        print(f"n = {n:<4} | Recursive: {rec_val:<10} | Exact: {ext_val:<10} | Match: {rec_val == ext_val}")

    
    print("\n--- Equation 3: T(n) = 2T(n/2) + 1  |  O(n) ---")
    for k in [0, 3, 6, 10]: 
        n = 2 ** k
        rec_val = T3_recursive(n)
        ext_val = T3_exact(n)
        print(f"n = {n:<4} | Recursive: {rec_val:<6} | Exact: {ext_val:<6} | Match: {rec_val == ext_val}")


    print("\n--- Equation 4: T(n) = T(n/2) + 1  |  O(log n) ---")
    for k in [0, 3, 10, 20]:  
        n = 2 ** k
        rec_val = T4_recursive(n)
        ext_val = T4_exact(n)
        print(f"n = {n:<7} | Recursive: {rec_val:<4} | Exact: {ext_val:<4} | Match: {rec_val == ext_val}")


if __name__ == "__main__":
    run_verification()