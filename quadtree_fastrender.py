
import math, random, timeit
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap

from turbo_colormap import turbo_colormap_data


def makeQuad():
	return [
		[None, None],
		[None, None]
	]


def getPixel(quadTree, x, y, mapSize):
	u = x / mapSize
	v = y / mapSize

	cell = quadTree

	while type(cell) is list:
		if u < 0.5:
			cellX = 0
		else:
			cellX = 1
		if v < 0.5:
			cellY = 0
		else:
			cellY = 1

		cell = cell[cellX][cellY]
		u = 2 * (u - cellX / 2)
		v = 2 * (v - cellY / 2)

	return cell


def mandelbrot(x, y, maxIterations):
	z0 = np.complex(x, y)
	z = 0
	for n in range(maxIterations):
		if abs(z) > 2:
			return 1 + n - math.log(math.log(abs(z)) / math.log(2)) / math.log(2)
		z = z * z + z0
	return 0


def randSamp(x, y, boxSize):
	return (i + random.random() * boxSize for i in (x, y))


def transformCoords(x, y, resolution, zoomWindow, centerPoint):
	real = ((x / resolution - 0.5) * zoomWindow + centerPoint[0])
	imaginary = (-(y / resolution - 0.5) * zoomWindow + centerPoint[1])

	return real, imaginary


def renderQuad(grid, resolution, maxBlockSize, sampleCount, maxIterations, zoomWindow, centerPoint, rangeThreshold, stdThreshold, x=0, y=0, subResolution=0):
	if subResolution == 0: subResolution = resolution

	boxSize = subResolution / 2

	for cellX, col in enumerate(grid):
		for cellY, cell in enumerate(col):
			x2 = x + cellX * boxSize
			y2 = y + cellY * boxSize

			sampledValues = [mandelbrot(*transformCoords(*randSamp(x2, y2, boxSize), resolution, zoomWindow, centerPoint), maxIterations) for s in range(min(sampleCount[1], max(int(sampleCount[1] * boxSize / maxBlockSize), sampleCount[0])))]

			if ((np.std(sampledValues) >= stdThreshold or np.ptp(sampledValues) >= rangeThreshold) and boxSize >= 2) or boxSize >= maxBlockSize:
				subdivision = makeQuad()
				grid[cellX][cellY] = subdivision
				renderQuad(subdivision, resolution, maxBlockSize, sampleCount, maxIterations, zoomWindow, centerPoint, rangeThreshold, stdThreshold, x2, y2, subResolution / 2)

			else:
				grid[cellX][cellY] = np.mean(sampledValues)
				#print('Solved ' + str(int(x2)) + ',' + str(int(y2)))


mandelbrotGrid = makeQuad()

MAX_ITERATIONS = 1024
RESOLUTION = 1024
SAMPLES = (2, 32)
ZOOM_WINDOW = 4 / 300
CENTER_POINT = (-.79, .15)
RANGE_THRESHOLD = 1
STD_THRESHOLD = 0.1
MAX_BLOCK_SIZE = 64


def execute():
	renderQuad(mandelbrotGrid, RESOLUTION, MAX_BLOCK_SIZE, SAMPLES, MAX_ITERATIONS, ZOOM_WINDOW, CENTER_POINT, RANGE_THRESHOLD, STD_THRESHOLD)


print(timeit.timeit(execute, number=1))

img = np.full((RESOLUTION, RESOLUTION), 0)

for y in range(img.shape[0]):
	for x in range(img.shape[1]):
		img[y, x] = getPixel(mandelbrotGrid, x, y, RESOLUTION)

	if not y % 10:
		print(y / RESOLUTION)

plt.imshow(img, interpolation="bicubic", cmap=ListedColormap(turbo_colormap_data))

plt.show(block=True)
