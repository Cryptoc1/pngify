import urllib,os,sys

#sys.argv == imgur link

imgur_link = "http://i.imgur.com/"+sys.argv[1]+".png" #add direct image link, run script and it will download the mp3 for you. ie "1zgGEN8"
imgur_name = imgur_link.split("/")[3]

urllib.urlretrieve(imgur_link, imgur_name)

command = "python pngify.py -i "+imgur_name+" -o "+imgur_name+".mp3"

os.system(command)
