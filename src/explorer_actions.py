import numpy as np
import cv2
from color_maps import nroot_generate_map
import pickle
import datetime


def save_img(fractal):
    destination = input('please specify destination:')
    if destination == '':
        basename = 'saved_img_'
        suffix = datetime.datetime.now().strftime('[%m_%d_%Y][%H:%M:%S]')
        destination = '/home/julius/Documents/projects/Fractals/images/' + basename + suffix

    print(destination)
    fractal.save_img(destination)

    if input('continue? [Y/n]') == 'n':
        exit(0)


def draw_rect(out, pt1, pt2, color=(0, 0, 255), thickness=3):
    out = cv2.rectangle(out, pt1, pt2, color, thickness, lineType=cv2.LINE_AA)
    return out


def toggle_edit(edit, out, fractal, pt1, pt2):
    if edit:
        edit = False
        out = fractal.img.copy()
        return edit, out
    else:
        edit = True
        out = draw_rect(out, pt1, pt2)
        return edit, out


def re_render(fractal, pt1, pt2):
    gaussian_pnt1 = fractal.gaussian[pt1[1]][pt1[0]]
    gaussian_pnt2 = fractal.gaussian[pt2[1]][pt2[0]]

    real_start = min(gaussian_pnt1.real, gaussian_pnt2.real)
    real_end = max(gaussian_pnt1.real, gaussian_pnt2.real)

    imag_start = min(gaussian_pnt1.imag, gaussian_pnt2.imag)
    imag_end = max(gaussian_pnt1.imag, gaussian_pnt2.imag)

    fractal.real_range = (real_start, real_end)
    fractal.imag_range = (imag_start, imag_end)

    fractal.generate()
    fractal.visualize()

    out = fractal.img.copy()
    edit = False

    return edit, out


def move_rectangle(key, edit, fractal, center, left_up, right_down, zoom, step=10):
    out = fractal.img.copy()

    # handle different arrows
    if key == 81:  # left
        center[0] -= step
    elif key == 82:  # up
        center[1] -= step
    elif key == 83:  # right
        center[0] += step
    elif key == 84:  # down
        center[1] += step

    if not edit:
        edit = True

    # re-draw rectangle
    pt1 = (center + zoom * left_up).astype(int)
    pt2 = (center + zoom * right_down).astype(int)

    draw_rect(out, pt1, pt2)
    return pt1, pt2, edit, out


def change_zoom(key, zoom, fractal, edit, pt1, pt2, center, left_up, right_down, step=0.05):
    if key == ord('+'):
        zoom -= step
    else:
        zoom += step

    out = fractal.img.copy()

    if not edit:
        edit = True

    # update rectangle
    pt1 = (center + zoom * left_up).astype(int)
    pt2 = (center + zoom * right_down).astype(int)

    draw_rect(out, pt1, pt2)

    return pt1, pt2, edit, out, zoom


def display_legend(disp_legend, fractal, out, legend, font):
    if disp_legend:
        out = fractal.img.copy()
        disp_legend = False
    else:
        disp_legend = True
        out = cv2.putText(out, legend, (20, 20), font, 0.6, (0, 0, 0), thickness=1, lineType=cv2.LINE_AA)

    return out, disp_legend


def save_fractal(fractal):
    file_location = input('please filepath for data to be saved: [leave empty for Default] \n')
    if file_location == '':
        basename = 'saved_fractal_'
        suffix = datetime.datetime.now().strftime('[%m_%d_%Y][%H:%M]')
        file_location = '/home/julius/Documents/projects/Fractals/saved_fractals' + basename + suffix
    pickle.dump(fractal, open(file_location, "wb"))

    cont = input('data saved. Continue? [Y/n]')
    if cont == 'n':
        exit(0)


def load_fractal(filepath):
    fractal = pickle.load(open(filepath, "rb"))
    return fractal


def select_point(fractal, center):
    radius = 5
    rad_step = 1
    move_step = 4
    color = (0, 0, 255)

    while True:
        out = fractal.img.copy()
        cv2.circle(out, center, radius, color, thickness=-1, lineType=cv2.LINE_AA)
        cv2.imshow('point selection', out)
        key = cv2.waitKey(0)
        if key == ord('+'):
            radius += rad_step
        if key == ord('-'):
            radius -= rad_step
        if key == 81:
            center[0] -= move_step
        elif key == 82:
            center[1] -= move_step
        elif key == 83:
            center[0] += move_step
        elif key == 84:
            center[1] += move_step
        elif key == 13:  # enter
            cv2.destroyAllWindows()
            pnt = fractal.gaussian[center[1], center[0]]
            return pnt
        else:
            print('unknown command!')


def change_color_map(fractal):
    fractal.color_map = fractal.color_map_generator(fractal.iterations, float(input('enter root order: ')))
    fractal.visualize()
