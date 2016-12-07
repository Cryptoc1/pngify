![README-scaled.png](screens/readme-scaled.png)

# PNGify
PNGify, or pngify, is a python module that uses [Pillow](https://github.com/python-pillow/Pillow) to transcode text as a PNG.

This repo includes the source for both the module, and an example program.

Here's what the text of this README becomes:

![README.png](screens/readme.png)


## Setup/install
PNGify requires Pillow for manipulating image data.

`$ pip install Pillow`

then,

`$ ./pngify.py -h`

## Usage
```
usage: pngify.py [-h] [-i FILE] [-s STRING] [-o FILE]

Transcode text between PNGs

optional arguments:
  -h, --help            show this help message and exit
  -i FILE, --input FILE
                        The text or image file to transcode
  -s STRING, --string STRING
                        The string to transcode into an image
  -o FILE, --output FILE
                        The file to output the result into (whether it be an
                        image, or text file)
```

###### &copy; Samuel Steele & Ben Poile, under the MIT license
