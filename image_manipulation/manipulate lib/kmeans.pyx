#KMeans Clustering and Palette Application Code
#by Dan Goodman
#
#Documentation note: close parentheses and camel-case, explanitory names

#Use PIL from its image manipulation functions
from PIL import Image
#Use numpy for its non pointer-based arrays
import numpy as np 
#Use stdlib for making dynamic C arrays
from libc.stdlib cimport malloc, free
#Use math for log base 2
import math
#use namedtuple to make function output more friendly
from collections import namedtuple

processedImage = namedtuple('processedImage', 'image width height palette')

cdef extern from "kmeans.h":
    int* ckMeans(int** imageData, int imageLength, int** meansList, int meansLength, int imgWidth, int imgHeight, int numRuns)
    int* cPalettize(int** imageData, int imageLength, int** colorsList, int colorsLength)

#The functions in this file:
#scanalyze(image, numMeans) - calls scanImage and passes the result to kMeans. Returns the final result
#scanImage(image, numMeans) - construct an intial palette based on medians
#kMeans(image, meansList) - use kmeans clustering to get an even better palette, and apply it to image
#palletize(image, colorsList) - apply an existing palette to the image

#All of the functions aside from scanImage return a result with the following attributes:
#   image - array with the values representing corresponding palette colors [y][x]
#   width - array width
#   height - array height
#   palette - array of colors [][3]

#Convienience function that scans and does kmeans algorithm. Returns resultant image
def scanalyze(image, numMeans):
    return kMeans(image,scanImage(image,numMeans))

#Given a loaded image (from PIL) and the number of means(colors), creates an initial palette
#The number of means should not be higher than 256
def scanImage(image, numMeans):
    #Make sure people aren't intering weird data for numMeans
    if type(numMeans) != int:
        raise TypeError("numMeans is not an integer")
    if numMeans < 1:
        raise ValueError("numMeans is not a positive number")

    red = np.zeros((256),dtype=np.int)
    green = np.zeros((256),dtype=np.int)
    blue = np.zeros((256),dtype=np.int)

    meansList = np.zeros((numMeans,3),dtype=np.int)

    try:
        imagePixels = image.getdata()
    except:
        raise AttributeError("can't read data from 'image'")
    
    numPixels = len(imagePixels)

    #Construct histogram of red, green, and blue values
    for i in range(numPixels):
        currentPixel = imagePixels[i]
        red[currentPixel[0]] += 1
        green[currentPixel[1]] += 1
        blue[currentPixel[2]] += 1

    #Make the histograms cumulative
    for i in range(255):
        red[i+1] += red[i]
        green[i+1] += green[i]
        blue[i+1] += blue[i]

    #Divide the histogram evenly into numMeans parts to give an acceptably close palette distribution
    #Populate the means list with these starting values
    for i in range(numMeans):
        thresholdRed = i * red[255] // (numMeans+1)
        thresholdGreen = i * green[255] // (numMeans+1)
        thresholdBlue = i * blue[255] // (numMeans+1)
        for j in range(256):
            if red[j] >= thresholdRed:
                meansList[i][0] = j
                break
        for j in range(256):
            if green[j] >= thresholdGreen:
                meansList[i][1] = j
                break
        for j in range(256):
            if blue[j] >= thresholdBlue:
                meansList[i][2] = j
                break

    return meansList

#A medium function meant to translate data to and from the C kmeans function
#   which will also apply the generated palette to the image
#Pass the image to be scanned and a list of initial means
#Returns tuple (imageArrayByPalette,imageWidth,imageHeight,colorList)
def kMeans(image, meansList):
    if (meansList<0).any():
        raise ValueError("meansList values must be greater than or equal to zero")
    if (meansList>255).any():
        raise ValueError("meansList values must be less than or equal to 255")
    #make sure that meansList is a proper numpy array int[*][3]
    if type(meansList) != np.ndarray:
        raise TypeError("meansList is not a numpy array")
    if meansList.ndim != 2:
        raise ValueError("kMeans expects a 2D numpy array as its input")
    if meansList.shape[0] == 0:
        raise ValueError("there should be at least one mean")
    if meansList.shape[1] != 3:
        raise ValueError("there should be three values for the second dimension of meansList")
    if meansList.dtype != np.int:
        raise TypeError("meansList should be an array of ints")

    #convert image and means list to format suitable for C
    imagePixels = image.getdata()
    cdef int** imageArray = <int**>malloc(len(imagePixels)*sizeof(int*))
    for i in range(len(imagePixels)):
        imageArray[i] = <int*>malloc(3*sizeof(int))

    for i in range(len(imagePixels)):
        imageArray[i][0] = imagePixels[i][0]
        imageArray[i][1] = imagePixels[i][1]
        imageArray[i][2] = imagePixels[i][2]

    cdef int** meansArray = <int**>malloc(len(meansList)*sizeof(int*))
    for i in range(len(meansList)):
        meansArray[i] = <int*>malloc(3*sizeof(int))

    for i in range(len(meansList)):
        meansArray[i][0] = meansList[i][0]
        meansArray[i][1] = meansList[i][1]
        meansArray[i][2] = meansList[i][2]
    
    kmeansIterations = math.ceil(math.log((len(imagePixels)/4),4)) #try to get about 25% of the image sampled

    #the heart of the function. Calls C to make the common case fast
    #note: image.getbbox()[2] is image width and image.getbbox()[2] is image height
    cdef int* imageData = ckMeans(imageArray, len(imagePixels), meansArray, len(meansList), image.getbbox()[2], image.getbbox()[3], kmeansIterations)

    #translate means table back from an array of ints
    for i in range(len(meansList)):
        meansList[i][0] = meansArray[i][0]
        meansList[i][1] = meansArray[i][1]
        meansList[i][2] = meansArray[i][2]

    #construct a new image based on palette values instead of RGB
    valuesArray = np.zeros((image.getbbox()[3],image.getbbox()[2]),dtype=np.int)
    count = 0;
    for y in range(image.getbbox()[3]):
        for x in range(image.getbbox()[2]):
            valuesArray[y][x] = imageData[count]
            count += 1
    
    free(imageData)
    for i in range(len(imagePixels)):
        free(imageArray[i])
    free(imageArray)
    for i in range(len(meansList)):
        free(meansArray[i])
    free(meansArray)
    
    return processedImage(valuesArray,image.getbbox()[2],image.getbbox()[3],meansList)

#A medium function meant to just apply a palette to an image without doing the kmeans algorithm
#colorsList is an array[numColors][3] where numColors <= 256
#Returns tuple (imageArrayByPalette,imageWidth,imageHeight,colorList)
#needs to be tested
def palletize(image, colorsList):
    #make sure that colorsList is a proper numpy array int[*][3]
    if type(colorsList) != np.ndarray:
        raise TypeError("colorsList is not a numpy array")
    if colorsList.ndim != 2:
        raise ValueError("palletize expects a 2D numpy array as its input")
    if colorsList.shape[0] == 0:
        raise ValueError("there should be at least one color")
    if colorsList.shape[1] != 3:
        raise ValueError("there should be three values for the second dimension of colorsList")
    if colorsList.dtype != np.int:
        raise TypeError("colorsList should be an array of ints")
    
    imagePixels = image.getdata()
    cdef int** imageArray = <int**>malloc(len(imagePixels)*sizeof(int*))
    for i in range(len(imagePixels)):
        imageArray[i] = <int*>malloc(3*sizeof(int))

    for i in range(len(imagePixels)):
        imageArray[i][0] = imagePixels[i][0]
        imageArray[i][1] = imagePixels[i][1]
        imageArray[i][2] = imagePixels[i][2]

    cdef int** colorsArray = <int**>malloc(len(colorsList)*sizeof(int*))
    for i in range(len(colorsList)):
        colorsArray[i] = <int*>malloc(3*sizeof(int))

    for i in range(len(colorsList)):
        colorsArray[i][0] = colorsList[i][0]
        colorsArray[i][1] = colorsList[i][1]
        colorsArray[i][2] = colorsList[i][2]

    #call only the palettize function in C
    cdef int* imageData = cPalettize(imageArray, len(imagePixels), colorsArray, len(colorsList))

    valuesArray = np.zeros((image.getbbox()[3],image.getbbox()[2]),dtype=np.int)
    count = 0;
    for y in range(image.getbbox()[3]):
        for x in range(image.getbbox()[2]):
            valuesArray[y][x] = imageData[count]
            count += 1
    
    free(imageData)
    for i in range(len(imagePixels)):
        free(imageArray[i])
    free(imageArray)
    for i in range(len(colorsList)):
        free(colorsArray[i])
    free(colorsArray)

    return processedImage(valuesArray,image.getbbox()[2],image.getbbox()[3],colorsList)


