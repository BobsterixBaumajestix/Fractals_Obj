from fractal_class import Fractal
from iterators import gen_julia_set_iterator
from color_maps import nroot_generate_map
from explorer import explorer


c = complex(input('value:'))

color_map = nroot_generate_map(30, order=2)
fr = Fractal(gen_julia_set_iterator(c), (200, 200), (-2, 2), (-2, 2), 30, 5, color_map)

explorer(fr)
