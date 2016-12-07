#!/usr/bin/env python
import math
from PIL import Image as PImage

'''
For transcode strings to Images
'''
class Image:
    '''
    Transcode the given string
    @param string The string to transcode
    @param mode The image color mode (RGBA|RGB) defaults to RGBA
    '''
    def __init__(self, string, mode="RGBA"):
        self.string = string
        self.mode = mode
        if mode != "RGB" and mode != "RGBA":
            raise Exception("Invalid mode")
        self.image = PImage.new(mode, self.calculate_size(), 0)
        self.image.putdata(self.string_to_data(mode, string))

    def save(self, path):
        # TODO: verify path
        self.image.save(path)

    def string_to_data(self, mode=None, string=None):
        if mode == None:
            mode = self.mode
        if string == None:
            string = self.string

        data = []

        if mode == "RGBA":
            factor = 4
        elif mode == "RGB":
            factor = 3
        else:
            raise Exception("Invalid mode")

        for i in range(0, len(string)):
            if i % factor == 0:
                r = ord(string[i])
                # account for array out-of-bounds
                g = 0
                if not i + 2 >= len(string):
                    g = ord(string[i + 1])
                b = 0
                if not i + 2 >= len(string):
                    b = ord(string[i + 2])

                if mode == "RGBA":
                    a = 0
                    if not i + 3 >= len(string):
                        a = ord(string[i + 3])
                    data.append((r, g, b, a))
                else:
                    data.append((r, g, b))
        return data

    '''
    Calculates the size needed to fit a string with a length `length`, using color mode `mode`
    @returns A tuple representing the size (w, h)
    '''
    def calculate_size(self, mode=None, length=None):
        if mode == None:
            mode = self.mode
        if length == None:
            length = len(self.string)

        if mode == "RGBA":
            n_pixels = length / 4.
        elif mode == "RGB":
            n_pixels = length / 3.
        else:
            raise Exception("Invalid mode")

        # okay, so basically, `n_pixels` is really the area of our image
        # so we want to find the sqrt of `n_pixels` (bc the area of a square is a width^2)
        w = math.ceil(math.sqrt(n_pixels))
        h = w

        # since we rounded up for the width, trim an extra row if needed
        if (w*w) - n_pixels > w:
            h = w - 1

        return (int(w), int(h))


class String:
    '''
    A pngify String, from an image!
    @param path Can be the path to an image, a pngify Image, or a Pillow Image
    @param mode (optional) the color mode to use when transcoding the image. If None, the PImage.mode is used
    '''
    def __init__(self, path, mode=None):
        if isinstance(path, Image):
            self.image = path.image
        elif isinstance(path, str):
            self.image = PImage.open(path)
        elif isinstance(path, PImage):
            self.image = path

        if mode == None:
            mode = self.image.mode

        if mode != "RGB" and mode != "RGBA":
            raise Exception("Invalid mode")

        self.mode = mode

        self.value = self.get_string(list(self.image.getdata()))

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def get_string(self, data=None, mode=None):
        if mode == None:
            mode = self.mode

        if mode != "RGB" and mode != "RGBA":
            raise Exception("Invalid mode")

        if data == None:
            data = self.image.getdata()
        elif not isinstance(data, list):
            data = list(data)

        string = ""
        for pixel in data:
            string += chr(pixel[0])
            string += chr(pixel[1])
            string += chr(pixel[2])
            if mode == "RGBA":
                string += chr(pixel[3])

        return string

if __name__ == "__main__":
    print("pngify is not meant to be run as a standalone program.")
