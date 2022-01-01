from fractal_class import Fractal
import iterators
from color_maps import nroot_generate_map, sat_nroot_generate_map
import pickle
from explorer import explorer

iterator = iterators.mandelbrot_iterator

fr = Fractal(iterator, (200, 200), (-2, 2), (-2, 2), 30, 5, nroot_generate_map, 2)

explorer(fr)
