import os
import sys
import string
import re
import platform
from fontTools.ttLib import TTFont
import fontTools.ttx
from PIL import Image, ImageFont, ImageDraw
import xml.etree.ElementTree as ET
from orderedset import OrderedSet

## ARGUMENT PART ##

filename = ""
minGlyph = -1
maxGlyph = -1

if len(sys.argv) == 1:
    print("Please identify the fontname.")
    print("Usage : prog <FONTNAME> <MINGLYPH> <MAXGLYPH>")
    print("FONTNAME excludes the extension.")
    sys.exit(-3)

fontname = sys.argv[1] + '.ttf' ## input font file
xml_name = sys.argv[1] + '.ttx' ## output xml file
exist_glyph_text = sys.argv[1] + '.txt' ## output text file

## print(fontname)
## print(xml_name)

if not os.path.exists(fontname):
    print("The TTF font does not exist. Finding OTF...")
    fontname = sys.argv[1] + '.otf'
    if not os.path.exists(fontname):
        print("The font does not exist.")
        sys.exit(-2)

if len(sys.argv) == 2:
    minGlyph = 0xAC00
    maxGlyph = 0xD7A3
    ## apply default value

elif len(sys.argv) == 3:
    minGlyph = int(sys.argv[3], 16)

elif len(sys.argv) >= 4:
    maxGlyph = int(sys.argv[4], 16)

if minGlyph > maxGlyph:
    print("The range is incorrect.")
    sys.exit(-2)

if os.path.exists(xml_name):
    print('TTX file for this font found!')
else: ## if TTX exists then use it
    print('TTX file for this font not found. Making new TTX file.')
    if platform.system() == "Windows": ## Windows CMD
        shcmd = "ttx -t cmap " + "\"" + fontname + "\""
    else: ## POSIX CMD
        shcmd = "./ttx -t cmap " + "\"" + fontname + "\""
    os.popen(shcmd).read()

## TTX-XML PART ##

xml_file = ET.parse(xml_name)
xml_root = xml_file.getroot()
numtable = set() ## initialize empty set

tag_map = xml_root.iter('map')

for chars in tag_map:
    try:
        numtable.add(chars.attrib["code"]) ## add hex string into the set, without duplication
    except KeyError:
        pass ## ignore key error

codeAry = []
for code in numtable:
    codeAry.append(int(code, 16)) ## convert string into integer

codeAry.sort(reverse=False) ## sort values in ascending order

print(codeAry[0:128])
## print(buffer)

## IMAGE PART ##

fnt = ImageFont.truetype(fontname, 24)
allowedBlank = [0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x20, 0x85, 0xA0, 0x1680, 0x180E, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006, 0x2007, 0x2008, 0x2009, 0x200A, 0x200B, 0x200C, 0x200D, 0x2028, 0x2029, 0x202F, 0x205F, 0x2060, 0x3000, 0xFEFF]
numofEmpty = 0
numofExist = 0

txt_file = open(exist_glyph_text, mode='wt', encoding='utf-8')

img_width = 48
img_height = 48

for codenum in codeAry:

    if codenum < 0x20: ## ignore control chars and space
        continue
    
    ## Make an image
    img = Image.new('RGB', (img_width, img_height), color = 'white')
    drawer = ImageDraw.Draw(img)
    drawer.text((8,8), chr(codenum), font=fnt, fill=(0,0,0))

    ## print(img)
    
    ## img.save('test.png')
    ## print(img.getpixel((0,0)))
    
    pixels = []

    for x in range(img_width):
        for y in range(img_height):
            pixels.append(img.getpixel((x,y)))

    isBlank = True

    for (r, g, b) in pixels:
        if r < 255 or g < 255 or b < 255: ## if the color of pixel is not white
            isBlank = False
            break

    if isBlank:
        if codenum in allowedBlank: ## allowed blank
            txt_file.write("%d\n" % codenum)
            numofExist += 1
        else:
            print("Unnecessary blank detected : %d" % codenum)
            numofEmpty += 1

    else:
        txt_file.write("%d\n" % codenum)
        numofExist += 1



##for code in existCodeAry:
##    txtline = "%d\n" % code
##    txt_file.write(txtline)

print('%d unnecessary blanks / %d existing glyphs' % (numofEmpty, numofExist))
print("Existing glpyhs table created. Check out the text file.\n")
txt_file.close()
sys.exit(0)
