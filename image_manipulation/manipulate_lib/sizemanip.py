import PIL
from PIL import Image
import os

def reSize(imgFile,option):
    '''
    Assumes first parameter image is a file path to the image
    Option can be either a string in the from a XUnit:YUnit ratio
    or a tuple containing (newWidth,newHeight)
    '''
    image = Image.open(imgFile)
    if(type(option) == str):  # Scale by ratio
        index = option.find(":")  # finds the index of : in width:height
        if(index == -1): # ':' not found, wrong format
            raise IndexError("ratio must be in the form XUnit:YUnit")
        try: xUnit = int(option[0:index])  # Desired base unit for the width
        except: raise ValueError("XUnit must be an integer in string format")
        try:yUnit = int(option[index+1:]) #   ||     ||   ||  ||   || height
        except: raise ValueError("YUnit must be an integer in string format")
        if(xUnit < 0 or yUnit < 0):
            raise ValueError("aspect ratio must be greater than zero")
        newImage = scale(image,xUnit,yUnit)
    elif(type(option) == tuple):
        if(type(option[0]) != int or type(option[1]) != int):
            raise TypeError("desired height and width must be an integer")
        elif(option[0] <= 0 or option[1] <= 0):
            raise ValueError("desired height and width must be greater than zero")
        newImage = image.resize((option[0],option[1]))
        pathInfo = str(imgFile).split('.',1)
        newPath = "media/" + pathInfo[0] + "copy." + pathInfo[1] 
        newImage.save(newPath)
    else:
        raise TypeError("second argument must be an string or a tuple")
    return newPath


def scale(image,xUnit,yUnit):
    ''' 
    Scales the image based on the given width to height ratio
    in the form "XUnit:YUnit"
    '''
    (width,height) = image.size
    multiplier = width//xUnit  # Scales using the width as a pivot
    newWidth = xUnit * multiplier
    newHeight = yUnit * multiplier
    newImage = image.resize((newWidth,newHeight))
    return newImage

##def main():
##    im = Image.open("/home/lefty/stitchpik/image_manipulation/static/image_manipulation/img/bubblegum.jpg")
##    im2 = reSize(im,(1000,1000))
##    im3 = reSize(im,"16:9")
##    im.show()
##    im2.show()
##    im3.show()
##    
##main()

    



    
