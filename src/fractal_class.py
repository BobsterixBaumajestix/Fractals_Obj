import numpy as np
from tqdm import tqdm
import cv2

import color_maps
import iterators


class Fractal:

    def __init__(self, iterator, size, real_range, imag_range, iterations, bound, color_map_generator, root_order, conv_map=None, gaussian=None,
                 img=None, conv_color=(0, 0, 0), name='Fractal'):

        self.iterator = iterator
        self.size = size
        self.real_range = real_range
        self.imag_range = imag_range
        self.iterations = iterations
        self.bound = bound
        self.color_map_generator = color_map_generator
        self.color_map = color_map_generator(self.iterations, root_order)
        self.conv_map = conv_map
        self.gaussian = gaussian
        self.img = img
        self.conv_color = conv_color
        self.name = name

        if self.conv_map is None or self.gaussian is None:
            self.generate()

        if self.img is None:
            self.visualize()

    def generate(self):
        # generate the axes from the endpoints
        real_axis = np.linspace(self.real_range[0], self.real_range[1], self.size[1])
        imag_axis = np.linspace(self.imag_range[0], self.imag_range[1], self.size[0])

        # initialize gaussian plane
        # size refers to size of screen (height, width)
        self.gaussian = np.zeros(self.size, dtype='complex')

        # generate gaussian plane
        print('generating gaussian plane...')
        it = np.nditer(self.gaussian, flags=['multi_index'])
        for x in tqdm(it, total=it.itersize):
            i, j = it.multi_index
            self.gaussian[i][j] = complex(real_axis[j], imag_axis[-(i + 1)])

        # initialize convergence map
        self.conv_map = np.zeros(self.size, dtype=int)

        # generate convergence map
        print('generating convergence map...')
        it = np.nditer(self.conv_map, flags=['multi_index'])
        for x in tqdm(it, total=it.itersize):
            i, j = it.multi_index
            self.conv_map[i][j] = self.iterator(self.gaussian[i][j], self.iterations, self.bound)

    def visualize(self):
        shape = (self.conv_map.shape[0], self.conv_map.shape[1], 3)
        self.img = np.zeros(shape, dtype='uint8')

        it = np.nditer(self.conv_map, flags=['multi_index'])

        print('generating image...')
        for x in tqdm(it, total=it.itersize):
            i, j = it.multi_index
            if x == -1:
                self.img[i][j] = self.conv_color
            else:
                self.img[i][j] = self.color_map[x]

    def view(self, wait=0):
        cv2.imshow(self.name, self.img)
        key = cv2.waitKey(wait)
        cv2.destroyAllWindows()
        return key

    def save_img(self, path):

        if not cv2.haveImageWriter(path):
            path += '.png'

        try:
            cv2.imwrite(path, self.img)
        except (RuntimeError, NameError, TypeError):
            print('something went wrong, image could not be saved. ')

"""def setup_fractal():
    #self, iterator, size, real_range, imag_range, iterations, bound, color_map, conv_map=None, gaussian=None,
                 #img=None, conv_color=(0, 0, 0), name='Fractal'
    
    # select iterator
    selection = input('select iterator: \nmandelbrot [1]\njulia set [2]\n')
    if selection == '1':
        iterator = iterators.mandelbrot_iterator
    elif selection == '2'
        c = input('please enter complex value to generate specific julia set iterator:  ')
        try:
            c = complex(c)
        except ValueError:
            print('could not convert input to complex number (must have form a + b.j)')
            exit(1)
            
        iterator = iterators.gen_julia_set_iterator(c)
    else:
        print('invalid input')
    
    # select size
    size = (input('height'), input('size'))
    
    # select ranges
    real_range = (float(input('real range start: ')), float(input('real range end: ')))
    imag_range = (input('imaginary range start: '), input('imaginary range end: '))
    
    # select iterations
    iterations = int(input('iterations: '))
    
    # select color mpa
    color_map = color_maps.nroot_generate_map(iterations, in)"""
