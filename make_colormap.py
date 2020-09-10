from PIL import Image

steps = 256

gradient = []

for i in range(steps):
	x = (i + 0.5) / steps
	gradient.append((
		int((1 / (1 + 10000**(0.5-x)))**(1.0 / 2.2) * 255),
		int((((2 * x - 1.0)**4 - 2.0 * (2 * x - 1.0)**2 + 1.0) * 1.5 * x)**(1.0 / 2.2) * 255),
		int((((2.25 * x - 0.75)**4 - 2 * (2.25 * x - 0.75)**2 + 1.0) * 0.75 * (1.5 - 2 * x)**2)**(1.0 / 2.2) * 255)
	))

img = Image.new('RGB', (steps, 1))
img.putdata(gradient)
img.save('colormap.png')
