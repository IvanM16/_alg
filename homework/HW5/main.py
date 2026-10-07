from functional_core import my_map, my_filter, my_reduce
from bubble_sort import bubble_sort_functional


def main():
    print("=" * 60)
    print(" 1. Testing Custom High-Order Functions (my_map, my_filter, my_reduce)")
    print("=" * 60)

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


    squared = my_map(lambda x: x ** 2, numbers)
    print(f"my_map (Square)     : {squared}")

 
    evens = my_filter(lambda x: x % 2 == 0, numbers)
    print(f"my_filter (Evens)   : {evens}")


    total_sum = my_reduce(lambda acc, x: acc + x, numbers, 0)
    print(f"my_reduce (Sum)     : {total_sum}")

    print("\n" + "=" * 60)
    print(" 2. Testing Loopless Bubble Sort (bubble_sort_functional)")
    print("=" * 60)

    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [42, -5, 0, 18, -10, 42],
        []
    ]

    def run_case(case):
        sorted_res = bubble_sort_functional(case)
        filtered_gt_10 = my_filter(lambda x: x > 10, sorted_res)
        print(f"Original : {case}")
        print(f"Sorted   : {sorted_res}")
        print(f"Filtered (> 10): {filtered_gt_10}")
        print("-" * 50)


    my_map(run_case, test_cases)


if __name__ == "__main__":
    main()