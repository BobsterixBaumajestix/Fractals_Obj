import numpy as np
import cv2

"""def HSV2BGR(hsv_color):
    color = cv2.cvtColor(np.array([[hsv_color]], dtype='uint8'), cv2.COLOR_HSV2BGR).ravel()

    return color

"""


def nroot_generate_map(max_value, order=2, color_range=(0, 255), s=255, v=255):
    colors = np.zeros((max_value + 1, 1, 3), dtype='uint8')

    for n in range(max_value + 1):
        hue = color_range[0] + (color_range[1] - color_range[0]) * np.power(n / max_value, 1 / order)
        colors[n][0] = (hue, s, v)

    colors = cv2.cvtColor(colors, cv2.COLOR_HSV2BGR)

    color_map = np.zeros((max_value + 1, 3), dtype=int)
    for n in range(max_value + 1):
        color_map[n] = colors[n][0]

    return color_map


def sat_nroot_generate_map(max_value, order=2, sat_range=(0, 255), h=10, v=255):
    colors = np.zeros((max_value + 1, 1, 3), dtype='uint8')

    for n in range(max_value + 1):
        sat = sat_range[0] + (sat_range[1] - sat_range[0]) * np.power(n / max_value, 1 / order)
        colors[n][0] = (h, sat, v)

    colors = cv2.cvtColor(colors, cv2.COLOR_HSV2BGR)

    color_map = np.zeros((max_value + 1, 3), dtype=int)
    for n in range(max_value + 1):
        color_map[n] = colors[n][0]

    return color_map
