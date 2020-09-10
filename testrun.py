import timeit, random


def factored():
	x = random.random()
	y = random.random()
	return (pow(x, 1 / 3) + (x - 1)**3 + 1) / 2


def expanded():
	x = random.random()
	y = random.random()
	return (pow(x, 1 / 3) + x**3 - 3 * x**2 + 3 * x) / 2


print(timeit.timeit(factored, number=1000000))
print(timeit.timeit(expanded, number=1000000))
