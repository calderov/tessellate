from PIL import Image
from PIL import ImageFilter

# Define a few constants
LUMINANCE_THRESHOLD = 128
HORIZONTAL_SPLITS = 3
VERTICAL_SPLITS = 4
MIN_POINTS_PERCENT_PER_SECTION = 1

def extract_points_from_edges(edges, luminance_threshold):
	points = []
	maxX, maxY = edges.size
	for x in range(maxX):
		for y in range(maxY):
			if edges.getpixel((x, y)) > luminance_threshold:
				points.append((x, y))
	return points

def paint_points_to_image(points, size):
	image = Image.new('L', size)
	for point in points:
		image.putpixel(point, 255)
	return image

def main():
	# Load original image
	image = Image.open('input.jpg')

	# Find the edges from the grayscale version of the image
	edges = image.convert('L').filter(ImageFilter.FIND_EDGES)

	# Preview the edges
	edges.show()

	# Create a data structure of points with those pixels
	# from the edges that are above the luminance threshold
	points = extract_points_from_edges(edges, LUMINANCE_THRESHOLD)

	# Paint the points into a new image (hard edges)
	hardEdges = paint_points_to_image(points, image.size)

	# Preview hard edges
	hardEdges.show('output.png')

	print(len(points), "points found")
	print('Done')

if __name__ == '__main__':
	main()