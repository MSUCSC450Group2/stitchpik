from PIL import Image, ImageDraw
import sys
from .kmeans import *
from .pixel import *

class Pixelator: #class assumes input checking will occur before class creation
    def __init__(self, imgfile):
        self.file = imgfile
        self.img = Image.open(imgfile)

    def pixelate(self, numColors, pixSize, resultFile):
        #numcolors, and pixelsize are integers, the desired number of colors 
        #and pixelation block size. resultfile is the location to save the 
        #resulting pixelated image
        try:
            scannedImg = scanalyze(self.img, numColors)
            try:
                result = pixelate(scannedImg.image, scannedImg.width, scannedImg.height, 
                                   numColors, pixSize)
                canvas = Image.new(size = (result.width*pixSize,
                                           result.height*pixSize),mode="RGB")
                draw = ImageDraw.Draw(canvas)
                for y in range(result.height):
                    for x in range(result.width):
                        filled = scannedImg.palette[result.array[y][x]]
                        draw.rectangle(
                            (x*pixSize, y*pixSize, x*pixSize + (pixSize-1),
                             y*pixSize+(pixSize-1)), 
                             fill=(filled[0], filled[1], filled[2]))
                canvas.save(resultFile)
            except:
                print("pixelization error, check pixSize and resultFile")
        except:
            print("Error from scanalyze function, check numColors or imagefile")

