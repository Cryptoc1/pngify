import urllib, os, sys, validators
from argparse import ArgumentParser

def exit(message=""):
    print(message)
    sys.exit()

def valid_file(x):
    if not os.path.exists(x): # checks if file 'x' exists, but doesn't open
        exit("{0} does not exist".format(x))
    return x

def strip_link(url):
    if validators.url(url) == True:
        return url.split("/")[3]
    else:
        exit("[!] Not a valid URL")

def main():
    parser = ArgumentParser(description="Transcode text between PNGs")
    parser.add_argument("-l", "--link", dest="link_input", help="The text or image file to transcode", metavar="STRING")
    parser.add_argument("-o", "--output", dest="file_output", help="The file name to output the result into (whether it be an image, or other file type)", metavar="FILE")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    args = vars(parser.parse_args())

    if args['link_input'] != None:
        output_filename = args['file_output']
        url = args['link_input']
        if output_filename == None:
            print "output is none"
            output_filename = strip_link(url)
            urllib.urlretrieve(url, "image_temp")
            os.system("python pngify.py -i image_temp -o "+output_filename+".mp3")
        else:
            print "output exists"
            urllib.urlretrieve(url, "image_temp")
            os.system("python pngify.py -i image_temp -o"+output_filenamet+".mp3")

if __name__ == "__main__":
    main()
