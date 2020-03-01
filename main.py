import sys
from tessellate import tessellate

sys.setrecursionlimit(100000)

if __name__ == '__main__':
	# Some nice settings are cannyMinThreshold = 100, cannyMaxThreshold = 200 and pointsCountThreshold = 1 to 7
	tessellate('ExampleInputs/johanes.jpg', 'output.png', cannyMinThreshold = 50, cannyMaxThreshold = 150, pointsCountThreshold = 5)
