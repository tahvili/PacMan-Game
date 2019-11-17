buildings = [
	[1, 11, 5],
	[2, 6, 7],
	[3, 13, 9],
	[12, 7, 16],
	[14, 3, 25],
	[19, 18, 22],
	[23, 13, 29],
	[24, 4, 28],
]

LEFT = 0
HEIGHT = 1
RIGHT = 2

def skyline(buildings):
	left = min(b[LEFT] for b in buildings)
	right = max(b[RIGHT] for b in buildings)
	last_height = None
	output = []
	for i in range(left, right + 1):
		heights = [b[HEIGHT] for b in buildings if b[LEFT] <= i < b[RIGHT]]
		height = max(heights) if heights else 0
		if height != last_height:
			output += [i, height]
			last_height = height
	return output

if __name__ == '__main__':
	assert(skyline(buildings) == [1, 11, 3, 13, 9, 0, 12, 7, 16, 3, 19, 18, 22, 3, 23, 13, 29, 0])
