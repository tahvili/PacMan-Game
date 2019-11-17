def rec_mult(x, y):

    a = len(str(x))
    b = len(str(y))
    if a == 1 or b == 1:
        return x * y

    n = max(a, b)

    p = x % (10**(a//2)) # 5
    q = y % (10**(b//2)) # 77

    r = rec_mult(p, q)
    print(r)

    return r * 10 ** (n // 2) + r


if __name__ == '__main__':
    print(rec_mult(7777, 55)) #0055, 7777
