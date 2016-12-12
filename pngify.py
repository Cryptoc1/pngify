#!/usr/bin/env python
import os, sys
from argparse import ArgumentParser
from pngify import Image

def valid_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        exit("[!] [pngify.py] {0} does not exist".format(x))
    return x

def exit(message=""):
    print(message)
    sys.exit()

def main():
    parser = ArgumentParser(description="Transcode text between PNGs")
    parser.add_argument("-i", "--input", dest="file_input", type=valid_file, help="The text or image file to transcode", metavar="FILE")
    parser.add_argument("-s", "--string", dest="string_input", help="The string to transcode into an image", metavar="STRING")
    parser.add_argument("-o", "--output", dest="file_output", help="The file to output the result into (whether it be an image, or text file)", metavar="FILE")
    parser.add_argument("-c", "--compress", dest="compression_method", help="Compression method to compress the data with", metavar="brotli,zlib", type=str, const="None", nargs="?", default="None")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = vars(parser.parse_args())

    img = Image(compression_method=args['compression_method'])
    if args['file_input'] != None:

        if args['string_input']:
            exit("[!] Cannot use -i and -s together")

        file_in = args['file_input']
        file_out = args['file_output']

        ext = file_in[file_in.rfind('.')+1:].lower()
        if ext != "png":
            # we have, what we are assuming, is a text file
            if file_out == None:
                exit("[!] An output file is required when transcoding text to an image")
            else:
                f = open(os.path.abspath(file_in))
                string = f.read()
                f.close()

                if len(string) <= 0:
                    exit("[!] Cannot transcode an empty string")
                else:
                    img.new(string)

                    # there could easily be an error with this dirty way of resolving paths
                    img.save(os.path.abspath(file_out))
                    exit("Image saved!")
        elif ext == "png":
            img.open(os.path.abspath(file_in))

            if file_out == None:
                exit(img.string)
            else:
                f = open(os.path.abspath(file_out), 'w')
                f.write(img.string)
                f.close()
                exit("Wrote string to file")
        else:
            exit("[!] Unknown file type: {0}".format(ext))

    if args['string_input']:
        if args['file_output'] == None:
            exit("[!] Must specify an output file for string input")
        else:
            string = args['string_input']
            file_out = args['file_output']

            img.new(string)

            # there could easily be an error with this dirty way of resolving paths
            img.save(os.path.abspath(file_out))
            exit("Image saved!")

if __name__ == "__main__":
    main()
