#!/usr/bin/env python
import sys
import math, re
from PIL import Image as PImage
import brotli, zlib
import bencoder

VERSION = 1

# Abstraction for the header (a bencoded string)
class Header:
    START_DELIMETER = ';'
    END_DELIMETER = ';\t\t\t'

    def __init__(self, raw=None, data=None):
        self.mode = "RGBA"
        self.values = {}

        if raw != None:
            self.from_string(raw)
        if data != None:
            self.from_data(data)


    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    '''
    Parse a bencoded (with our delimeters) string to be used as the represented Header
    '''
    def from_string(self, string):
        start = string.find(self.START_DELIMETER) + len(self.START_DELIMETER)
        string = string[start:string.find(self.END_DELIMETER, start)]
        self.raw = string
        self.values = bencoder.decode(string)

        return self.values

    '''
    Parse the header from raw pixel data
    '''
    def from_data(self, data, mode="RGBA"):
        if mode != "RGB" and mode != "RGBA":
            raise Exception("Invalid mode")

        if not isinstance(data, list):
            data = list(data)

        string = ""
        for pixel in data:
            string += chr(pixel[0])
            string += chr(pixel[1])
            string += chr(pixel[2])
            if mode == "RGBA":
                string += chr(pixel[3])

        return self.from_string(string)

    '''
    Return a bencoded string representing the Header
    '''
    def to_string(self):
        return "{0}{1}{2}".format(self.START_DELIMETER, bencoder.encode(self.values), self.END_DELIMETER)

    def get(self, key):
        return self.values[key]

    def set(self, key, value):
        self.values[key] = value

'''
For transcode strings to Images
'''
class Image:
    '''
    Transcode the given string
    @param string The string to transcode
    @param mode The image color mode (RGBA|RGB) defaults to RGBA
    '''
    def __init__(self, mode="RGBA", compression_method="None"):
        self.mode = mode
        if mode != "RGB" and mode != "RGBA":
            raise Exception("Invalid mode")

        self.compression_method = compression_method

        # default header
        self.header = Header()
        self.header.set('v', VERSION)
        self.header.set('cm', compression_method)

        # init empty image prop. to hold the PIL Image
        self.image = None

    def new(self, string):
        self.string = string
        self.value = self.header.to_string() + self.compress(self.string)

        self.image = PImage.new(self.mode, self.calculate_size(length=len(self.value)), 0)

        self.data = self.encode(self.value)
        self.image.putdata(self.data)

    def open(self, path):
        self.image = PImage.open(path)
        self.data = self.image.getdata()
        self.value = self.decode(self.data)
        self.header = Header(data=self.data)

        # if a compression_method wasn't specified, try to determine from the header
        if self.compression_method == "None":
            self.compression_method = self.header.get('cm')

        if self.compression_method != self.header.get('cm'):
            raise Exception('Specified compression_method is different than that found in PNGify Header')

        self.string = self.decompress(self.trim_header(self.value))

    def compress(self, string=None, compression_method="None"):
        if string == None:
            string = self.string
        if compression_method == "None":
            compression_method = self.compression_method

        if compression_method == "None":
            return string
        elif compression_method.lower() == "brotli":
            return brotli.compress(string)
        elif compression_method == "zlib":
            return zlib.compress(string)
        else:
            raise Exception("Invalid compression_method: {0}".format(compression_method))

    def decompress(self, string=None, compression_method=None):
        if string == None:
            string = self.string
        if compression_method == None:
            compression_method = self.compression_method

        if compression_method == "None":
            return string
        elif compression_method.lower() == "brotli":
            return brotli.decompress(string)
        elif compression_method == "zlib":
            return zlib.decompress(string)
        else:
            raise Exception("Invalid compression_method: {0}".format(compression_method))

    def save(self, path):
        # TODO: verify path

        self.image.save(path)

    '''
    returns the string encoded as pixel data
    '''
    def encode(self, string=None, mode=None):
        if mode == None:
            mode = self.mode

        # probably not needed because of the check below
        if mode != "RGB" and mode != "RGBA":
            raise Exception("Invalid mode: {0}".format(mode))

        data = []

        if mode == "RGBA":
            factor = 4
        elif mode == "RGB":
            factor = 3
        else:
            raise Exception("Invalid mode: {0}".format(mode))

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
    returns the pixel data as a string
    '''
    def decode(self, data=None, mode=None):
        if mode == None:
            mode = self.mode

        if mode != "RGB" and mode != "RGBA":
            raise Exception("Invalid mode: {0}".format(mode))

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

    '''
    Calculates the size needed to fit a string with a length `length`, using color mode `mode`
    @returns A tuple representing the size (w, h)
    '''
    def calculate_size(self, mode=None, length=None):
        if mode == None:
            mode = self.mode
        if length == None:
            length = len(self.compressed_string)

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

    def trim_header(self, string):
        return string[string.find(Header.END_DELIMETER) + len(Header.END_DELIMETER):]

if __name__ == "__main__":
    print("pngify is not meant to be run as a standalone program.")
