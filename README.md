<h1 align="center">
<br>
PNGify
<br>
<br>
</h1>

![README-scaled.png](screens/readme-scaled.png)

PNGify, or pngify, is a python module that uses [Pillow](https://github.com/python-pillow/Pillow) to transcode text as a PNG.

This repo includes the source for both the module, and an example program.

Here's what the text of this README becomes:

![README.png](screens/readme.png)


## Setup/install
PNGify requires Pillow for manipulating image data, and brotli for compressing data.

`$ pip install Pillow`

`$ pip install brotlipy`

`$ pip install bencoder`

then,

`$ ./pngify.py -h`

## The Beauty of Text Files
So the beautiful thing about text files is that to get their contents, it's just a simple call to `read()`.
Well, because PNGify just opens and calls `read()` on whatever file you specify, you can really encode just about anything into the PNGs data. For example, to encode an mp3 you can simply use the call `./pngify.py -i song.mp3 -o song.png`, to encode the mp3, and use `./pngify.py -i song.png -o song.mp3` to get that mp3 back!

Cheers for simple text files!

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

#### Found a bug?
Please, please, please report it!

I threw this script together pretty quickly, so there could easily be quite a few bugs.

#### Wishing PNGify had feature *x*, that could do *y*?
Submit a pull request, or open an issue, and we'd gladly take a look into it!


###### &copy; Samuel Steele & Ben Poile, under the MIT license
