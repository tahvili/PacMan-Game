
def boundary(rec_list):

    lst = [list(x) for x in rec_list]
    org = len(lst)
    result, n = [], []
    res = []
    if len(rec_list) == 1:
        result.append([lst[0][0], lst[0][1]])
        result.append([lst[0][2], 0])

        return result


    mid = len(lst) // 2
    left = boundary(lst[:mid])
    right = boundary(lst[mid:])
    res = merge(left, right)

    print("left:", left, "right:", right)
    """
    if len(res) == :
        print("happend")
        n = flatten(res)
        return n
        
    else:
    """
    return res

def flatten(lst):

    result = []
    for i in lst:
        for j in i:
            result.append(j)
    return result


def merge(left, right):

    h1, h2, i, j = 0, 0, 0, 0
    result = []
    n = []

    while i < len(left) and j < len(right):
        if left[i][0] < right[j][0]:
            h1 = left[i][1]
            bound = left[i][0]
            i += 1
        elif right[j][0] < left[i][0]:
            h2 = right[j][1]
            bound = right[j][0]
            j += 1
        else:
            h1 = left[i][1]
            h2 = right[j][1]
            bound = right[j][0]
            i += 1
            j += 1
        if valid(result, max(h1, h2)):
            result.append([bound, max(h1, h2)])
    result.extend(right[j:])
    result.extend(left[i:])

    return result


def valid(result, height):
    return not result or result[-1][1] != height

if __name__ == '__main__':

    #print(boundary([(3, 13, 9)]))
    print(boundary([(3, 13, 9),(1, 11, 5),(12, 7, 16),(14, 3, 25),
                     (19, 18, 22),(2, 6, 7),(23, 13, 29),(23, 4, 28)]))

    #print(compare([(3, 13, 9)],[(1, 11, 5)]))
