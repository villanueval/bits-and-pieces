#!/usr/bin/python

from PIL import Image
import sys
import pyocr
import pyocr.builders
import PythonMagick
import os
from random import randrange


# Test "global" variables
if len(sys.argv) != 3:
  print "\n Error: Incorrect number of arguments given."
  print " Call the program as: " + sys.argv[0] + " <filename> <language>"
  print " "
  print " Exiting program."
  print " "
  sys.exit(1)

# Place "global" variables in the namespace
filename = sys.argv[1]
lang = sys.argv[2]

print "\n " + filename + "\n"

#check which OCR it can use, tesseract or cuneiform
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print "\n Error: No OCR tool found"
    print " "
    sys.exit(1)

tool = tools[0]
print("\n Will use OCR tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'tesseract'


#Check if language is installed (sudo apt-get install tesseract-ocr-[lang])
langs = tool.get_available_languages()
if lang in langs:
  print(" Will use lang '%s'" % (lang))
  print("   Installed languages: %s" % ", ".join(langs))
else:
  print("\n Error: Language '%s' not installed" % (lang))
  print("   Installed languages: %s" % ", ".join(langs))
  print(" ")
  sys.exit(1)
# Ex: Will use lang 'fra'


##################################
#FUNCTIONS
##################################

def fileExists(f):
  try:
    file = open(f)
  except IOError:
    exists = 0
  else:
    exists = 1
  return exists


#from http://www.imagemagick.org/download/python/README.txt
def Crop(image):
    img = PythonMagick.Image(image) # make a copy
    #rect = "%sx%s+%s+%s" % (w, h, x1, y1)
    rect = "1600x120+1220+1260"
    img.crop(rect)
    randomname = str(randrange(1000)) + '.tiff'
    img.write(randomname)
    return randomname


def Rotate(image, degrees):
    img = PythonMagick.Image(image) # make a copy
    img.rotate(degrees)
    #img.write('rotated.tiff')
    return img


##################################

if fileExists(filename)==False:
  print("\n Error: File '%s' could not be found" % (filename))
  print(" ")
  sys.exit(1)



#Re-orient and cut the image
# if 'even' in filename:
#   img = Rotate(filename, 90)
# elif 'odd' in filename:
#   img = Rotate(filename, -90)

img = Rotate(filename, 90)

img = Crop(img)

txt = tool.image_to_string(Image.open(img), lang=lang, builder=pyocr.builders.TextBuilder())

spp_name = txt.split(' ')

#Use replace to avoid problems with non-ascii. Will print a '?' instead
genus = spp_name[0].encode('ascii', 'replace')
spp = spp_name[1].encode('ascii', 'replace')

#Fix problem with 'l' getting interpreted as 'I'
spp = spp.replace('I', 'l')


#write the result as "file.jpg   species_name"
tablefile = open ( 'species.txt', 'a' )
tablefile.write ( os.path.basename(filename) + '\t' + genus + '_' + spp + '\n')
tablefile.close()

os.remove(img)
sys.exit(0)