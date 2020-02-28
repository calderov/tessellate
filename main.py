import sys
from tessellate import tessellate

sys.setrecursionlimit(100000)

if __name__ == '__main__':
	# Some nice settings are luminanceThreshold = 70 and pointsCountThreshold = 1 to 7
	tessellate('ExampleInputs/peale.jpg', 'output.png', luminanceThreshold=70,  pointsCountThreshold = 3)
