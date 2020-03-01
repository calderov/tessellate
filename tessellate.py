import cv2
import numpy
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

def extractPointsFromEdges(image, minThreshold = 100, maxThreshold = 200):
	# Transform the image to a format compatible with OpenCV
	cvImage = numpy.array(image)

	# Extract the edges from the image
	edges = cv2.Canny(cvImage, minThreshold, maxThreshold)

	# Extract data points from the edges
	points = []
	cols, rows = image.size
	for x in range(cols):
		for y in range(rows):
			if edges[y][x] == 255:
				points.append((x, y))
	return points

def paintPointsToImage(points, size):
	image = Image.new('L', size)
	for point in points:
		image.putpixel(point, 255)
	return image

def getPointsInRegion(points, topLeft, bottomRight):
	pointsInRegion = []

	minX, minY = topLeft
	maxX, maxY = bottomRight

	for x, y in points:
		if minX <= x and x < maxX and minY <= y and y < maxY:
			pointsInRegion.append((x, y))

	return pointsInRegion

def getTessellationSections(points, topLeft, bottomRight, pointsCountThreshold):
	sections = []
	pointsInRegion = getPointsInRegion(points, topLeft, bottomRight)

	# print(len(pointsInRegion), " - ", pointsCountThreshold, " : ", (topLeft, bottomRight))

	# breakpoint()
	if len(pointsInRegion) > pointsCountThreshold:
		x0, y0 = topLeft
		x1, y1 = bottomRight

		# Randomly choose in what direction to partiton
		if random.random() < 0.5:
			# Compute possible vertical partitions and recursivelly extract its tessellations
			topMiddle = (x0 + int((x1 - x0) / 2), y0)
			bottomMiddle = (x0 + int((x1 - x0) / 2), y1)
			
			leftSections = getTessellationSections(pointsInRegion, topLeft, bottomMiddle, pointsCountThreshold)
			rightSections = getTessellationSections(pointsInRegion, topMiddle, bottomRight, pointsCountThreshold)
			
			sections += leftSections
			sections += rightSections

		else:
			# Compute possible horizontal partitions and recursivelly extract its tessellations
			middleLeft = (x0, y0 + int((y1 - y0) / 2))
			middleRight = (x1, y0 + int((y1 - y0) / 2))

			topSections = getTessellationSections(pointsInRegion, topLeft, middleRight, pointsCountThreshold)
			bottomSections = getTessellationSections(pointsInRegion, middleLeft, bottomRight, pointsCountThreshold)

			sections += topSections
			sections += bottomSections

	else:
		sections.append((topLeft, bottomRight))

	return sections

def getColorFromSection(originalImage, topLeft, bottomRight):
	r = 0
	g = 0
	b = 0
	minX, minY = topLeft
	maxX, maxY = bottomRight

	totalPixels = max((maxX - minX) * (maxY - minY), 1)

	for x in range(minX, maxX):
		for y in range(minY, maxY):
			pixel_r, pixel_g, pixel_b = originalImage.getpixel((x, y))
			r += pixel_r
			g += pixel_g
			b += pixel_b

	r = int(r / totalPixels)
	g = int(g / totalPixels)
	b = int(b / totalPixels)

	return (r, g, b)


def paintSections(originalImage, sections):
	image = Image.new('RGB', originalImage.size)
	draw = ImageDraw.Draw(image)

	for section in sections:
		topLeft, bottomRight = section
		color = getColorFromSection(originalImage, topLeft, bottomRight)
		draw.rectangle([topLeft, bottomRight], color)

	return image
	
def tessellate(inputPath, outputPath, cannyMinThreshold = 100, cannyMaxThreshold = 200, pointsCountThreshold = 10):
	print("Load original image\n")
	image = Image.open(inputPath)

	print("Extract data points from image edges")
	points = extractPointsFromEdges(image, cannyMinThreshold, cannyMaxThreshold)
	pointedImage = paintPointsToImage(points, image.size)
	pointedImage.show()

	print("Get a list of the sections that tessellate the image [(topLeft, bottomRight), ...]\n")
	sections = getTessellationSections(points, (0,0), image.size, pointsCountThreshold)

	print("Image split into %d sections\n" % len(sections))

	print("Paint sections to image\n")
	tessellatedImage = paintSections(image, sections)

	print("Save tessellated image\n")
	tessellatedImage.save(outputPath)
	tessellatedImage.show()

	print('Done')
