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

print(fontname)
print(xml_name)

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

file = open(xml_name, mode='rt', encoding='utf-8')
buffer = file.read()
file.close()

lines = buffer.split('\n')
numtable = []
buffer = ""

for line in lines:
    buffer = line.strip()
    if buffer.find('<map') < 0:
        continue
    else:
        buffer = line[line.find('\"') + 1:]
        buffer = buffer[:buffer.find('\"')]
    numtable.append(buffer)


print(numtable[0:128])
## print(buffer)

## FONT PART ##



## IMAGE PART ##

fnt = ImageFont.truetype(fontname, 15)

for code in numtable:
    num = int(code, 16)
    if num not in range(minGlyph, maxGlyph + 1):
        continue
    if num <= 0x20:
        continue
    
    img = Image.new('RGB', (24, 24), color = 'white')
    drawer = ImageDraw.Draw(img)
    drawer.text((4,4), chr(num), font=fnt, fill=(0,0,0))
    ## print(img)
    
    ## img.save('test.png')
    ## print(img.getpixel((0,0)))
    
    pixels = []

    for x in range(24):
        for y in range(24):
            pixels.append(img.getpixel((x,y)))

    isBlank = True

    for (r, g, b) in pixels:
        if r < 255 and g < 255 and b < 255:
            isBlank = False
            break

    if isBlank:
        print("This font has unnecessary blanks : 0x%X\n" % num)
        sys.exit(-1)
        isBlank = True
        break

if not isBlank:
    print("This font doesn't have unnecessary blanks.\n")
    sys.exit(0)
