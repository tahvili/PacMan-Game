from typing import *


def multiply_monotone(a, b):

    a = str(a)
    b = str(b)
    x = len(a)
    y = len(b)


    if x < y:
        a = make_equal(a, y-x)
    if y < x:
        b = make_equal(b, x-y)

    n = max(len(a), len(b))

    if n == 1:
        return int(a[0]) * int(b[0])

    s1 = a[n//2:n]
    s2 = a[0:n//2]
    print(s1)
    print(s2)

    #i = a % (10 **(n//2))
    #j = b % (10 ** (n // 2))

    r = multiply_monotone(s1, s2)

    return r * 10**n + (r + r) * 10**(n//2) + r

def make_equal(a, b):

    for i in range(b):
        a = '0' + a
    return a

if __name__ == '__main__':
    print(multiply_monotone(5, 77))
