#Pixelization code (mode method)
#by Dan Goodman
#
#Documentation note: close parentheses and camel-case, explanitory names

#Use numpy for its non pointer-based arrays
import numpy as np 
#Use stdlib for making dynamic C arrays
from libc.stdlib cimport malloc, free
#Use namedtuple to make function output more friendly
from collections import namedtuple

pixelProcessed = namedtuple('pixelProcessed','array width height')

cdef extern from "pixel.h":
    int** cPixelate(int** imageData, int imageWidth, int imageHeight, int numColors, int pixelSize)
#The functions in this file:

#A medium function to call the C pixelization method. imageData is a 2D numpy array and is passed from the kmeans function
#imageWidth and imageHeight are the dimensions of the image
#pixelSize is the desired pixel size
#the result has the attributes:
#   array - contains a 2D array with the palette values of the corresponding blocks [y][x]
#   width - width of the array
#   height - height of the array
#
#note:will throw an exception if pixelSize > image width or height
def pixelate(imageData, imageWidth, imageHeight, numColors, pixelSize):
    if type(imageData) != np.ndarray:
        raise Exception("imageData must be a numpy array")
    if imageData.ndim != 2:
        raise Exception("imageData must be a 2D numpy array")
    if type(imageWidth) != int:
        raise Exception("imageWidth must be an integer")
    if imageWidth < 1:
        raise Exception("imageWidth must be a positive number")
    if type(imageHeight) != int:
        raise Exception("imageHeight must be an integer")
    if imageHeight < 1:
        raise Exception("imageHeight must be a positive number")
    if type(numColors) != int:
        raise Exception("numColors must be an integer")
    if numColors < 1:
        raise Exception("numColors must be a positive value")
    if type(pixelSize) != int:
        raise Exception("pixelSize must be an integer")
    if pixelSize < 1:
        raise Exception("pixelSize must be a positive value")
    if pixelSize > imageWidth or pixelSize > imageHeight:
        raise Exception("pixelSIze cannot be bigger than the image")

    #test imageData, numColors, pixelSize, imageWidth, imageHeight
    cdef int** imageArray = <int**>malloc(imageHeight*sizeof(int*))
    for i in range(imageHeight):
        imageArray[i] = <int*>malloc(imageWidth*sizeof(int))

    for y in range(imageHeight):
        for x in range(imageWidth):
            imageArray[y][x] = imageData[y][x]

    cdef int** pixelArray = cPixelate(imageArray,imageWidth,imageHeight,numColors,pixelSize)
    #pixelArray = cPixelate(imageData, imageWidth, imageHeight, pixelSize)
    #do C function to pixelate image

    pixelWidth = imageWidth//pixelSize
    pixelHeight = imageHeight//pixelSize

    pixelNPArray = np.zeros((pixelHeight,pixelWidth),dtype=np.int)

    for y in range(pixelHeight):
        for x in range(pixelWidth):
            pixelNPArray[y][x] = pixelArray[y][x]
        free(pixelArray[y])

    free(pixelArray)
    for i in range(imageHeight):
        free(imageArray[i])
    free(imageArray)
    

    return pixelProcessed(pixelNPArray,pixelWidth,pixelHeight)
    #return an array

