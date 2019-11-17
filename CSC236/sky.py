
def getSkyline(blds):
        """
        :type blds: List[List[int]]
        :rtype: List[List[int]]
        """
        if not blds:
            return []
        if len(blds) == 1:
            return [[blds[0][0], blds[0][2]], [blds[0][1], 0]]
        mid = len(blds) // 2
        left = getSkyline(blds[:mid])
        right = getSkyline(blds[mid:])
        return merge(left, right)

def merge(left, right):
        h1, h2, res = 0, 0, []
        while left and right:
            if left[0][0] < right[0][0]:
                pos, h1 = left[0]
                left = left[1:]
            elif left[0][0] > right[0][0]:
                pos, h2 = right[0]
                right = right[1:]
            else:
                pos, h1 = left[0]
                h2 = right[0][1]
                left = left[1:]
                right = right[1:]
            H = max(h1, h2)
            if not res or H != res[-1][1]:
                res.append([pos, H])
        if left:
            res += left
        if right:
            res += right
        return res

if __name__ == '__main__':

    print(getSkyline([[3, 13, 9],[1, 11, 5],[12, 7, 16],[14, 3, 25],
                     [19, 18, 22],[2, 6, 7],[23, 13, 29],[23, 4, 28]]))
