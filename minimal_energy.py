import pygame
from numpy import array as a
import numpy as np
from PIL import Image

im = Image.open("image.jpg")
gray = im.convert('LA')
asnumpy_gray = np.asarray(gray)
image = np.asarray(im)

sobel_0 = [
    [-0.125, 0, 0.125],
    [-0.25, 0, 0.25],
    [-0.125, 0, 0.125]
]

sobel_1 = [
    [-0.125, -0.25, -0.125],
    [0, 0, 0],
    [0.125, 0.25, 0.125]
]

edge_values = a([
    a([0, 1, 0.5, 0.8]),
    a([0.5, 0.2, 0.3, 0.4]),
    a([1, 0.5, 0.6, 0.7]),
    a([0.2, 0.1, 0.1, 0.1])
])

asnumpy_gray = a([a([pixel[0] for pixel in row]) for row in asnumpy_gray])
image = [row.tolist() for row in image]


def get_minimal_energy_map_vertical(edge_values_):

    minimal_energy_map = np.zeros(shape=edge_values_.shape)
    minimal_energy_map[-1] = edge_values_[-1]

    for i in range(-2, -len(edge_values_) - 1, -1):
        for j in range(len(edge_values_[0])):
            if j == 0:
                minimal_energy_map[i][j] = edge_values_[i][j] + min(minimal_energy_map[i + 1][j:j + 2])
            elif j == len(edge_values_[0]) - 1:
                minimal_energy_map[i][j] = edge_values_[i][j] + min(minimal_energy_map[i + 1][j - 1:j + 1])
            else:
                minimal_energy_map[i][j] = edge_values_[i][j] + min(minimal_energy_map[i + 1][j - 1:j + 2])

    return minimal_energy_map


def seam_carve_vertical(image, minimal_energy_map):
    seam = np.zeros(len(minimal_energy_map), dtype=np.int32)

    seam[0] = (minimal_energy_map[0].tolist()).index(min(minimal_energy_map[0]))

    for i in range(len(minimal_energy_map) - 1):
        j = seam[i]

        if j == 0:
            sub_array = minimal_energy_map[i + 1][:2].tolist()
            seam[i + 1] = sub_array.index(min(sub_array))
        elif j == len(minimal_energy_map[0]) - 1:
            sub_array = minimal_energy_map[i + 1][-2:].tolist()
            seam[i + 1] = j + sub_array.index(min(sub_array)) - 1
        else:
            sub_array = minimal_energy_map[i + 1][j - 1:j + 2].tolist()
            seam[i + 1] = j + sub_array.index(min(sub_array)) - 1

    for i in range(len(seam)):
        image[i] = image[i].tolist()[:seam[i]] + image[i].tolist()[seam[i] + 1:]

    return image


def get_edges_values(input):
    img1 = np.zeros(shape=asnumpy_gray.shape)
    for y in range(1, len(img1) - 1):
        for x in range(1, len(img1[y]) - 1):
            inx = 0.
            for ax in range(-1, 2):
                for b in range(-1, 2):
                    try:
                        inx += asnumpy_gray[y + ax][x + b] * sobel_0[ax + 1][b + 1] + asnumpy_gray[y + ax][x + b] * sobel_1[ax + 1][b + 1]
                    except:
                        pass

            img1[y][x] = inx
    return img1


def dostuff(input):
    for y in range(len(input)):
        for x in range(len(input[y])):
            input[y][x] = (((input[y][x] - -9635.0) * (255 - 0)) / (255 - -9635.0)) + 0

    return input


tmp = get_minimal_energy_map_vertical(get_edges_values(asnumpy_gray))

tmp = dostuff(tmp)

image = seam_carve_vertical(image, tmp)

out = Image.fromarray(image)

out.show()
