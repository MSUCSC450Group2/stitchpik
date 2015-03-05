from PIL import Image, ImageDraw
import sys
from .kmeans import *
from .pixel import *

class Picture: #class assumes input checking will occur before class creation
	def __init__(self, imgfile):
		self.file = imgfile
		self.img = Image.open(imgfile)

	def pixelate(self, numColors, pixSize, resultFile):# numcolors, and pixelsize are integers, the desired number of colors and pixelation block size. resultfile is the location to save the resulting pixelated image
		try:
			result = scanalyze(self.img, numColors)
			try:
				result2 = pixelate(result.image, result.width, result.height, numColors, pixSize)
				canvas = Image.new(size=(result2.width*pixSize,result2.height*pixSize),mode="RGB")
				draw = ImageDraw.Draw(canvas)
				for y in range(result2.height):
					for x in range(result2.width):
						draw.rectangle((x*pixSize,y*pixSize,x*pixSize+(pixSize-1),y*pixSize+(pixSize-1)),fill=(result.palette[result2.array[y][x]][0], result.palette[result2.array[y][x]][1], result.palette[result2.array[y][x]][2]))
				canvas.save(resultFile)
			except:
				print("pixelization error, check pixSize and resultFile")
		except:
			print("Error from scanalyze function, check numColors or imagefile")

#	def resize(self, stitchType, newSize):
		#add code to resize image depending on desired size and type of pattern being produced.
	
#	def colorize(self, colors):
		#add code to colorize image.

