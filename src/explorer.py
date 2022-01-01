import cv2
import color_maps
from os import system
import explorer_actions
import numpy as np


def explorer(fractal):

    # SETUP #

    convergence_color = (0, 0, 255)  # in HSV for now

    # rectangle selection
    right_down = np.array([int(fractal.size[1] / 2), int(fractal.size[0] / 2)], dtype=int)
    left_up = np.array([- int(fractal.size[1] / 2), - int(fractal.size[0] / 2)], dtype=int)
    center = np.array([int(fractal.size[1] / 2), int(fractal.size[0] / 2)], dtype=int)
    move_step = 10

    zoom = 0.5
    zoom_step = 0.05
    edit = False
    pt1 = (center + zoom * left_up).astype(int)
    pt2 = (center + zoom * right_down).astype(int)

    # legend
    legend = 'save: s  quit: q  move: arrows  zoom: +,-  re-render: return  toggle edit mode: e  toggle legend: ?'
    disp_legend = False
    font = cv2.FONT_ITALIC

    out = fractal.img.copy()

    resize = False

    while True:

        if resize:
            out = cv2.resize(out, resize, interpolation=cv2.INTER_AREA)
        cv2.imshow('fractal', out)
        key = cv2.waitKey(0)
        system('clear')

        # process input

        if key == ord('q'):
            exit(0)

        elif key == ord('s'):
            # save image
            cv2.destroyAllWindows()
            explorer_actions.save_img(fractal)

        elif key == ord('e'):
            # toggle edit mode
            edit, out = explorer_actions.toggle_edit(edit, out, fractal, pt1, pt2)

        elif key == 13:  # enter
            cv2.destroyAllWindows()

            explorer_actions.re_render(fractal, pt1, pt2)
            out = fractal.img.copy()

        elif key in [81, 82, 83, 84]:  # arrows
            pt1, pt2, edit, out = explorer_actions.move_rectangle(key, edit, fractal, center, left_up, right_down, zoom, step=move_step)

        elif key in [ord('+'), ord('-')]:
            pt1, pt2, edit, out, zoom = explorer_actions.change_zoom(key, zoom, fractal, edit, pt1, pt2, center, left_up, right_down, step=zoom_step)

        elif key == ord('?'):
            out = explorer_actions.display_legend(disp_legend, fractal, out, legend, font)

        elif key == ord('c'):
            cv2.destroyAllWindows()
            explorer_actions.change_color_map(fractal)
            out = fractal.img.copy()

        elif key == ord('d'):
            move_step = float(input('enter value for move step: '))
            zoom_step = float(input('enter value for zoom step: '))

        elif key == ord('\\'):  # custom command
            cv2.destroyAllWindows()
            command = input('enter custom command: ')
            command = command.split(' ')
            if len(command) == 0:
                continue

            # handle custom commands
            if command[0] == 'print':
                if len(command) != 2:
                    print('incorrect syntax!')
                    continue
                elif command[1] == 'point':
                    point = explorer_actions.select_point(fractal, center.copy())
                    print(point)
                else:
                    print('unknown parameter {} for \'print\''.format(command[1]))

            elif command[0] == 'save':
                if len(command) != 2:
                    print('incorrect syntax for \'save\'!')
                    continue
                elif command[1] == 'fractal':
                    explorer_actions.save_fractal(fractal)
                elif command[1] == 'img':
                    explorer_actions.save_img(fractal)
                else:
                    print('unknown parameter {} for \'save\''.format(command[1]))

            elif command[0] == 'load':
                if len(command) != 1:
                    print('\'load\' doesn\'t accept parameters.')
                else:
                    fractal = explorer_actions.load_fractal(input('please specify filepath: '))
                    out = fractal.img.copy()

            elif command[0] == 'param':
                if len(command) != 2:
                    print('invalid syntax!')
                    continue
                try:
                    parameter, value = command[1].split('=')
                except ValueError:
                    print('invalid syntax!')
                    continue
                if parameter == 'iterations':
                    try:
                        value = int(value)
                    except ValueError:
                        print('value must be convertible to int')
                        continue
                    fractal.iterations = value
                    fractal.color_map = color_maps.nroot_generate_map(fractal.iterations, 2)
                    if input('reload fractal? [Y/n]') != 'n':
                        fractal.generate()
                        fractal.visualize()
                elif parameter == 'bound':
                    try:
                        value = float(value)
                    except ValueError:
                        print('value must be convertible to float')
                        continue
                    fractal.bound = value
                    if input('reload fractal? [Y/n]') != 'n':
                        fractal.generate()
                        fractal.visualize()
            elif command[0] == 'rescale':
                if len(command) != 3:
                    print('invalid syntax')
                    continue
                else:
                    try:
                        height = int(command[1])
                        width = int(command[2])
                    except ValueError:
                        print('could not convert parameters to int')
                        continue
                    fractal.size = (height, width)
                    fractal.generate()
                    fractal.visualize()
                    out = fractal.img.copy()

            elif command[0] == 'resize':
                if len(command) != 3:
                    print('syntax error')
                    continue
                else:
                    try:
                        height = int(command[1])
                        width = int(command[2])
                    except ValueError:
                        print('could not convert parameters to int')
                        continue
                    resize = (height, width)

            else:
                print('unknown command')

        else:
            print('input could not be processed!')
