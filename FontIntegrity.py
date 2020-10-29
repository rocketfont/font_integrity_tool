import os
import sys
import string
import re
import platform
from fontTools.ttLib import TTFont
import fontTools.ttx
from PIL import Image, ImageFont, ImageDraw
import xml.etree.ElementTree as ET

## ARGUMENT PART ##

filename = ""
minGlyph = -1
maxGlyph = -1

if len(sys.argv) == 1:
    print("Please identify the fontname.")
    print("Usage : prog <FONTNAME> <MINGLYPH> <MAXGLYPH>")
    print("FONTNAME excludes the extension.")
    sys.exit(-3)

fontname = sys.argv[1] + '.ttf'
xml_name = sys.argv[1] + '.ttx'
exist_glyph_text = sys.argv[1] + '.txt'

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

if platform.system() == "Windows":
    shcmd = "ttx -t cmap " + fontname

else:
    shcmd = "./ttx -t cmap " + fontname

os.popen(shcmd).read()

## TTX-XML PART ##

xml_file = ET.parse(xml_name)
xml_root = xml_file.getroot()
numtable = []

tag_map = xml_root.iter('map')

for chars in tag_map:
    numtable.append(chars.attrib["code"])

print(numtable[0:128])
## print(buffer)

## IMAGE PART ##

fnt = ImageFont.truetype(fontname, 15)
existCodeAry = []
numofEmpty = 0
numofExist = 0

codenum_prev = -1

for code in numtable:
    codenum = int(code, 16)

    if codenum_prev > codenum:
        break

    if codenum not in range(minGlyph, maxGlyph + 1):
        codenum_prev = codenum
        continue
    if codenum <= 0x20: ## ignore control chars and space
        codenum_prev = codenum
        continue
    
    ## Make a 24x24 image
    img = Image.new('RGB', (24, 24), color = 'white')
    drawer = ImageDraw.Draw(img)
    drawer.text((4,4), chr(codenum), font=fnt, fill=(0,0,0))

    ## print(img)
    
    ## img.save('test.png')
    ## print(img.getpixel((0,0)))
    
    pixels = []

    for x in range(24):
        for y in range(24):
            pixels.append(img.getpixel((x,y)))

    isBlank = True

    for (r, g, b) in pixels:
        if r < 255 or g < 255 or b < 255: #if the color of pixel is not white
            isBlank = False
            break

    if isBlank:
        print("Unnecessary blank detected : %d" % codenum)
        numofEmpty += 1

    else:
        existCodeAry.append(codenum)
        numofExist += 1

    codenum_prev = codenum

txt_file = open(exist_glyph_text, mode='wt', encoding='utf-8')
for code in existCodeAry:
    txtline = "%d\n" % code
    txt_file.write(txtline)

print('For given range : %d empty glyphs / %d existing glyphs' % (numofEmpty, numofExist))
print("Existing glpyhs table created. Check out the text file.\n")
txt_file.close()
sys.exit(0)
