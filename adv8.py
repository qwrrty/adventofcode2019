#! /usr/bin/env python3

import itertools

class PixelException:
    pass

class SIF(object):
    def __init__(self, width, height, image_data):
        self.layers = []
        self.width = width
        self.height = height

        i = 0
        while i < len(image_data):
            layer = []
            for h in range(0, height):
                layer.append(image_data[i:i+width])
                i += width
            self.layers.append(layer)

    def render(self):
        img = []
        for h in range(0, self.height):
            img.append([' '] * self.width)

        for h in range(0, self.height):
            for w in range(0, self.width):
                for l in self.layers:
                    if l[h][w] != "2":
                        img[h][w] = l[h][w]
                        break

        return "\n".join(["".join(x) for x in img])
            

def count_digits(layer, digit):
    return sum(1 for row in layer for d in row if d == digit)


def part1():
    with open("adv8_input.txt", "r") as f:
        data = f.read().strip()
    img = SIF(25, 6, data)

    # Find the layer with the fewest 0s
    smallest_layer = None
    smallest_layer_count = None
    for i in range(0, len(img.layers)):
        cnt = count_digits(img.layers[i], "0")
        if smallest_layer_count is None or cnt < smallest_layer_count:
            smallest_layer = img.layers[i]
            smallest_layer_count = cnt

    # Count the 1s and the 2s in this layer
    ones = count_digits(smallest_layer, "1")
    twos = count_digits(smallest_layer, "2")
    return ones * twos

def part2():
    with open("adv8_input.txt", "r") as f:
        data = f.read().strip()
    img = SIF(25, 6, data)

    print(img.render())
