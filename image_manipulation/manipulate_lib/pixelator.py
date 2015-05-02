from PIL import Image, ImageDraw
import sys
from .kmeans import *
from .pixel import *

class Pixelator: #class assumes input checking will occur before class creation

  def __init__(self, imgfile):
    self.file = imgfile
    self.img = Image.open(imgfile)
    self.pal = ""

  def pixelate(self, numColors, pixSize, resultFile):
    # numcolors, and pixelsize are integers, the desired number of colors 
    # and pixelation block size. resultfile is the location to save the 
    # resulting pixelated image.

    try:
      result = scanalyze(self.img, numColors)
      for c in range(len(result.palette)):
        if c > 0:
          self.pal += ','
        self.pal += "#"
        self.pal += hex(result.palette[c][0])[2:].zfill(2)
        self.pal += hex(result.palette[c][1])[2:].zfill(2)
        self.pal += hex(result.palette[c][2])[2:].zfill(2)
      try:
        result2 = pixelate(result.image, result.width, result.height, numColors, pixSize)
        canvas = Image.new(size=(result2.width*pixSize,result2.height*pixSize),mode="RGB")
        draw = ImageDraw.Draw(canvas)
        for y in range(result2.height):
          for x in range(result2.width):
            draw.rectangle((x*pixSize,
                            y*pixSize,
                            x*pixSize+(pixSize-1),
                            y*pixSize+(pixSize-1)),
                            fill=(result.palette[result2.array[y][x]][0], 
                            result.palette[result2.array[y][x]][1], 
                            result.palette[result2.array[y][x]][2]))
            if(y>0):
              greyHorizT = 0.299*result.palette[result2.array[y-1][x]][0] 
              + 0.587*result.palette[result2.array[y-1][x]][1] 
              + 0.114*result.palette[result2.array[y-1][x]][2]  
              greyHorizB = 0.299*result.palette[result2.array[y][x]][0] 
              + 0.587*result.palette[result2.array[y][x]][1] 
              + 0.114*result.palette[result2.array[y][x]][2]  
              maxValue = int(max(greyHorizT,greyHorizB))
              minValue = int(min(greyHorizT,greyHorizB))
              inside = maxValue - minValue
              outside = 255-inside
              if(inside > outside):
                gval = minValue + inside // 2
              else:
                gval = (maxValue + outside // 2) % 256
              draw.rectangle((x*pixSize,
                              y*pixSize,
                              x*pixSize + (pixSize-1),
                              y*pixSize),
                              fill=(gval,gval,gval))
            if(x>0):
              greyHorizL = 0.299*result.palette[result2.array[y][x-1]][0] 
              + 0.587*result.palette[result2.array[y][x-1]][1] 
              + 0.114*result.palette[result2.array[y][x-1]][2]  
              greyHorizR = 0.299*result.palette[result2.array[y][x]][0] 
              + 0.587*result.palette[result2.array[y][x]][1] 
              + 0.114*result.palette[result2.array[y][x]][2]
              maxValue = int(max(greyHorizL,greyHorizR))
              minValue = int(min(greyHorizL,greyHorizR))
              inside = maxValue - minValue
              outside = 255-inside
              if(inside > outside):
                gval = minValue + inside // 2
              else:
                gval = (maxValue + outside // 2) % 256
              draw.rectangle((x*pixSize,
                             (y*pixSize) + 1,
                             x*pixSize,
                             y*pixSize + (pixSize-1)),
                             fill=(gval,gval,gval))
        canvas.save(resultFile)
        return result.palette
      except:
        print("pixelization error, check pixSize and resultFile")
    except:
      print("Error from scanalyze function, check numColors or imagefile")


