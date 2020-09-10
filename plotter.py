
import random, math, timeit
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

from turbo_colormap import turbo_colormap_data

WIDTH = 1024
HEIGHT = WIDTH
ITERATIONS = 1024
SAMPLES = 2

SCOPE = (-.79, .15, 4 / 300)


def mandelbrot(x, y):
	z0 = np.complex(x, y)
	z = 0
	for n in range(0, ITERATIONS):
		if abs(z) > 2:
			return 1 + n - math.log(math.log(abs(z)) / math.log(2)) / math.log(2)
		z = z * z + z0
	return 0


def samplePixel(x, y):
	return random.random() / WIDTH * SCOPE[2] + x, random.random() / HEIGHT * SCOPE[2] + y


img = np.full((round(HEIGHT), WIDTH), 0)


def render():
	for y in range(img.shape[0]):
		for x in range(img.shape[1]):
			img[y, x] = np.mean([mandelbrot(*samplePixel(((x / img.shape[1] - 0.5) * SCOPE[2] + SCOPE[0]), ((y / img.shape[0] - 0.5) * SCOPE[2] + SCOPE[1]))) for s in range(SAMPLES)])

		if not y % 10:
			print(y / HEIGHT)


print(timeit.timeit(render, number=1))

plt.imshow(img, interpolation="bicubic", cmap=ListedColormap(turbo_colormap_data))

plt.show(block=True)
