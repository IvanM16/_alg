

from functional_core import my_reduce, make_range


def bubble_sort_functional(lst):
   
    if len(lst) <= 1:
        return lst

    
    def bubble_pass(arr):
        def step(acc, x):
            res_list, swapped = acc
            if not res_list:
                return ([x], swapped)
            last = res_list[-1]
            prev = res_list[:-1]
            if last > x:
               
                return (prev + [x, last], True)
            else:
                return (res_list + [x], swapped)

        return my_reduce(step, arr, ([], False))

    
    def outer_step(acc, pass_num):
        arr, swapped = acc
        
        if not swapped and pass_num != 1:
            return (arr, False)
        return bubble_pass(arr)

    
    sorted_arr, _ = my_reduce(outer_step, make_range(len(lst)), (lst, True))
    return sorted_arr