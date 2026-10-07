"""
Tower of Hanoi (河內塔問題)
Course Exercise: Recursive vs Iterative implementations
"""

def hanoi_recursive(n: int, src: str = 'A', aux: str = 'B', target: str = 'C') -> None:
    """
    Solves Tower of Hanoi using Recursion.
    
    Time Complexity: O(2^n)
    Space Complexity: O(n) (call stack)
    """
    if n <= 0:
        return
    if n == 1:
        print(f"Move disk 1 from {src} -> {target}")
        return
    
    # Step 1: Move top n-1 disks from src to aux using target as temporary peg
    hanoi_recursive(n - 1, src, target, aux)
    
    # Step 2: Move the largest disk from src to target
    print(f"Move disk {n} from {src} -> {target}")
    
    # Step 3: Move n-1 disks from aux to target using src as temporary peg
    hanoi_recursive(n - 1, aux, src, target)


def hanoi_iterative(n: int, src: str = 'A', aux: str = 'B', target: str = 'C') -> None:
    """
    Solves Tower of Hanoi Iteratively (Non-recursive) using modulo 3 patterns.
    
    Time Complexity: O(2^n)
    Space Complexity: O(n) (to maintain disk stacks)
    """
    if n <= 0:
        return

    total_moves = (1 << n) - 1  # Equivalent to 2^n - 1
    
    # Initialize stacks for pegs
    pegs = {
        'A': list(range(n, 0, -1)),
        'B': [],
        'C': []
    }
    
    s, a, t = src, aux, target
    
    # If number of disks is even, swap auxiliary and target destination sequence
    if n % 2 == 0:
        a, t = t, a

    def make_legal_move(p1: str, p2: str) -> None:
        """Executes the only valid move between two pegs p1 and p2."""
        if not pegs[p1]:
            disk = pegs[p2].pop()
            pegs[p1].append(disk)
            print(f"Move disk {disk} from {p2} -> {p1}")
        elif not pegs[p2]:
            disk = pegs[p1].pop()
            pegs[p2].append(disk)
            print(f"Move disk {disk} from {p1} -> {p2}")
        elif pegs[p1][-1] < pegs[p2][-1]:
            disk = pegs[p1].pop()
            pegs[p2].append(disk)
            print(f"Move disk {disk} from {p1} -> {p2}")
        else:
            disk = pegs[p2].pop()
            pegs[p1].append(disk)
            print(f"Move disk {disk} from {p2} -> {p1}")

    for i in range(1, total_moves + 1):
        if i % 3 == 1:
            make_legal_move(s, t)
        elif i % 3 == 2:
            make_legal_move(s, a)
        elif i % 3 == 0:
            make_legal_move(a, t)


if __name__ == "__main__":
    disks = 3
    print("=" * 40)
    print(f"1. Recursive Solution (n = {disks})")
    print("=" * 40)
    hanoi_recursive(disks)
    
    print("\n" + "=" * 40)
    print(f"2. Iterative Solution (n = {disks})")
    print("=" * 40)
    hanoi_iterative(disks)