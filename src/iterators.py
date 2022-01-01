import numpy as np


def mandelbrot_iterator(seed, iterations, bound):
    z = complex(0, 0)
    for i in range(iterations):
        z = z ** 2 + seed
        if abs(z) >= bound:
            return i + 1

    return -1


def gen_julia_set_iterator(c):
    def julia_set_iterator(seed, iterations, bound):
        z = seed
        for i in range(iterations):
            z = z ** 2 + c
            if abs(z) >= bound:
                return i + 1
        return -1

    return julia_set_iterator


def mandelbrot_moon(seed, iterations, bound):
    z = complex(1, 1)
    for i in range(iterations):
        z = z / (np.exp(z) + seed)
        if abs(z) >= bound:
            return i + 1

    return -1


def mandelbrot_variation(seed, iterations, bound):
    z = complex(0, 0)
    for i in range(iterations):
        z = 1 / np.power(z + seed, 3)
        if abs(z) >= bound:
            return i + 1

    return -1


def mandelbrot_variation2(seed, iterations, bound):
    z = complex(0, 0)
    for i in range(iterations):

        if abs(z) >= bound:
            return i + 1

    return -1
