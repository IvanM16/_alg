
def my_map(func, seq):
 
    if not seq:
        return []
    return [func(seq[0])] + my_map(func, seq[1:])


def my_filter(func, seq):
   
    if not seq:
        return []
    head, tail = seq[0], seq[1:]
    if func(head):
        return [head] + my_filter(func, tail)
    return my_filter(func, tail)


def my_reduce(func, seq, initializer=None):

    if initializer is None:
        if not seq:
            raise TypeError("my_reduce() of empty sequence with no initial value")
        return my_reduce(func, seq[1:], seq[0])
    if not seq:
        return initializer
    return my_reduce(func, seq[1:], func(initializer, seq[0]))


def make_range(n):

    if n <= 0:
        return []
    return make_range(n - 1) + [n]