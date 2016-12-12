#!/usr/bin/env python
import urllib, os, sys
import validators
from argparse import ArgumentParser

'''
Note: this is strictly for png to mp3 conversion. It's designed to work that way, but can be changed below if needed (not reccomended).
'''

def exit(message=""):
    print(message)
    sys.exit()

def valid_file(x):
    if not os.path.exists(x): # checks if file 'x' exists, but doesn't open
        exit("[!] [imgur.py] {0} does not exist".format(x))
    return x

def strip_link(url):
    if validators.url(url) == True:
        return url.split("/")[3]
    else:
        exit("[!] Not a valid URL")

def main():
    parser = ArgumentParser(description="Transcode text from an imgur image to an mp3")
    parser.add_argument("-l", "--link", dest="link_input", help="The text or image file to transcode", metavar="STRING")
    parser.add_argument("-o", "--output", dest="file_output", help="The file name to output the result into (whether it be an image, or other file type)", metavar="FILE")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = vars(parser.parse_args())

    if args['link_input'] != None:
        output_filename = args['file_output']
        url = args['link_input']
        if output_filename == None: #if a filename isn't specified, make it the imgur image code
            output_fileWithExtension = strip_link(url)
            output_file = output_fileWithExtension.split(".", 1)[0]
            urllib.urlretrieve(url, "temp_"+output_fileWithExtension)
            os.system("python pngify.py -i temp_"+output_fileWithExtension+" -o "+output_file+".mp3; rm temp_"+output_filename) #run pngify.py then delete temp file
        else: #image name is specified
            o = output_filename.split(".", 1)
            output_file = output_filename.split(".", 1)[0]

            if o[len(o)-1] != "png": #if the user didn't input the file extension, add it in automatically
                output_filename = output_filename+".png"

            urllib.urlretrieve(url, "temp_"+output_filename) #download file
            os.system("python pngify.py -i temp_"+output_filename+" -o "+output_file+".mp3; rm temp_"+output_filename) #run pngify.py then delete temp file

if __name__ == "__main__":
    main()
