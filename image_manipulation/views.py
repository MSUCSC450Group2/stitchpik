from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from .forms import *
import numpy as np
from .manipulate_lib.pixelator import *
from .models import Image
from .manipulate_lib.sizemanip import reSize
import time
import numpy as np



def getUserImages(request):
    if request.method == 'POST':
        chooseform = ChooseImageForm(request.POST)
        if chooseform.is_valid():
            gallery = Image.userImages(request.user)
            #resultImage = 'media/result.jpg'
            #requestImage = request.chosenImage
            form = ManipulateImageForm()
           
            return render_to_response(applicationPage(), {'imgForm': imageUpload(request), 
                                  'form' : form, 
                                  'imagegallery' : gallery, 
                                   'chooseform' : ChooseImageForm(),
                                    
                                  'image' : chooseform.cleaned_data['chosenImage'] },
                                  context_instance = RequestContext(request))   
    else:    
        chooseform=ChooseImageForm()
    return chooseform


def applicationPage():
    return 'image_manipulation/applicationPage.html'

def newUploadedImage(request):
    return Image(imgFile = request.FILES['imgFile'], user = request.user, 
                 private = True)

def imageUpload(request):
    

    imgForm = ImageUploadForm(request.POST, request.FILES)
    if "required" in str(imgForm['imgFile'].errors): # for when no image is uploaded
        imgForm = ImageUploadForm()
    elif imgForm.is_valid():
        clearImageChoice(request) # rid of 'selected' image var
        newImg = newUploadedImage(request)
        newImg.save()
    return imgForm
   

def saveFormDataToCookie(form, response):
    deleteSavedFormCookieData(response)

    setCookie(response, 'numberOfColors', int(form.cleaned_data['numberOfColors']))
    setCookie(response, 'gaugeSize', float(form.cleaned_data['gaugeSize']))
    setCookie(response, 'canvasLength', float(form.cleaned_data['canvasLength']))
    setCookie(response, 'canvasWidth', float(form.cleaned_data['canvasWidth']))
    setCookie(response, 'knitType', int(form.cleaned_data['knitType']))

def isSavedCookieData(request):
    return ('numberOfColors' in request.COOKIES) if True else False

def getSavedCookieData(request):
    return ManipulateImageForm( {
        'numberOfColors':int(request.COOKIES['numberOfColors']),
        'gaugeSize':float(request.COOKIES['gaugeSize']),
        'canvasLength':float(request.COOKIES['canvasLength']),
        'canvasWidth':float(request.COOKIES['canvasWidth']),
        'knitType':int(request.COOKIES['knitType']),
        'colorSelect':0
    } )


def saveFormDataToSession(form, request):
    request.session.set_expiry(31536000) # one year
    request.session['savedFormOptions'] = {
        'numberOfColors': int(form.cleaned_data['numberOfColors']), 
        'gaugeSize': float(form.cleaned_data['gaugeSize']), 
        'canvasLength': float(form.cleaned_data['canvasLength']),
        'canvasWidth': float(form.cleaned_data['canvasWidth']), 
        'knitType': int(form.cleaned_data['knitType'])
    }

def isSavedSessionData(request):
    return request.session.get('savedFormOptions')

def savedSessionData(savedOptions):
    return ManipulateImageForm(
            {'numberOfColors': int(savedOptions.get('numberOfColors')),
             'gaugeSize': float(savedOptions.get('gaugeSize')),
             'canvasLength': float(savedOptions.get('canvasLength')),
             'canvasWidth': float(savedOptions.get('canvasWidth')),
             'knitType': int(savedOptions.get('knitType')) }
           )



def saveImageChoice(request, imagePath):
    if imagePath != "":   
        request.session.set_expiry(0)
        request.session['imageChoice']=imagePath
        
def loadImageChoice(request):
    tempPath= request.session.get('imageChoice', "")
    if tempPath != "":
        tempImage =Image(imgFile = tempPath, user = request.user, 
                     private = True)
        tempPath = tempImage.imgFile
    return tempPath
    

def clearImageChoice(request):
    if loadImageChoice(request) != "":
        del request.session['imageChoice']
    



  
def setCookie(response, key, value, days_expire = 365):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60 

    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie(key, value, max_age=max_age, expires=expires)

def deleteSavedFormCookieData(response):
    response.delete_cookie('numberOfColors')
    response.delete_cookie('gaugeSize')
    response.delete_cookie('canvasLength')
    response.delete_cookie('canvasWidth')
    response.delete_cookie('knitType')

def imageExists(imgPath):
    if imgPath == "None" or imgPath is None or imgPath == "":
        return False
    return True

@login_required
def fetchApplication(request):
    selectedImage=""
    gallery=Image.userImages(request.user)
    
    imgUploadForm = imageUpload(request) # upload image first

    print("loadimages check" ,loadImageChoice(request))
    if loadImageChoice(request)=="":    
        inputImage = Image.latestUserImageFile(request.user)
    else:
        inputImage = loadImageChoice(request)
        
    resultImage = 'media/' + Image.resultImageLocation(inputImage, request.user)

    requestImage = inputImage
    imgForm = ChooseImageForm(request.POST)
    pixelPal = ""
    dasInstructions = ""    


    if request.method == 'POST':
        if imgForm.is_valid():
            print('set select')
            print(inputImage)
            #print(imgForm.cleaned_data['chosenImage'])
            if (request.POST.get("changebutton")):
                #print(inputImage)
                chosenImage=imgForm.cleaned_data['chosenImage']
                #print(chosenImage)
                #inputImage= chosenImage
                print(chosenImage)
                saveImageChoice(request, chosenImage)
                print('changed')
                #print(inputImage) 
                
                requestImage= chosenImage
        form = ManipulateImageForm(request.POST) 

        if form.is_valid() and imageExists(str(inputImage)): # can't render nill image

            getPalette = request.POST['colorList']
            if(getPalette == "" or request.POST['colorSelect'] == '0'):
                requestImage = '../' + resultImage # django is preappending /media
                numColors = form.cleaned_data['numberOfColors']
                pixSize = int(form.cleaned_data['gaugeSize'])
                imgWidth = 96 * int(form.cleaned_data['canvasWidth'])
                print("The input image is ", inputImage)
                print("the request image is ", requestImage)
                imgHeight = 96 * int(form.cleaned_data['canvasLength'])
                print(inputImage)
                print(type(inputImage))
                #inputImage = '../media/' + inputImage
                print("The input image is ", inputImage)
                inputImage = reSize(inputImage,(imgWidth,imgHeight))
                pixelatedImg = Pixelator(inputImage)
                numPie = pixelatedImg.pixelate(numColors, pixSize, resultImage)
                pixelPal = pixelatedImg.pal
                dasInstructions = generateInstructions(form.cleaned_data['knitType'], numPie)
                cookieAction = 0
                
            else:
                requestImage = '../' + resultImage # django is preappending /media
                pixSize = int(form.cleaned_data['gaugeSize'])
                imgWidth = 96 * int(form.cleaned_data['canvasWidth'])
                imgHeight = 96 * int(form.cleaned_data['canvasLength'])
                print("the input image is ", inputImage)
                inputImage = reSize(inputImage,(imgWidth,imgHeight))
                pixelatedImg = Pixelator(inputImage)
                palItems = getPalette.split(',')
                tempPal = np.zeros((len(palItems),3),dtype=int)
                for i in range(len(palItems)):
                    tempPal[i][0] = int(palItems[i][1:3],16)
                    tempPal[i][1] = int(palItems[i][3:5],16)
                    tempPal[i][2] = int(palItems[i][5:7],16)
                numPie = pixelatedImg.palettize(tempPal, pixSize, resultImage)
                pixelPal = getPalette
                dasInstructions = generateInstructions(form.cleaned_data['knitType'], numPie)
                cookieAction = 0
        else:
            cookieAction = 1

    else:
        cookieAction = 1

    # Load saved cookie data if available
    if cookieAction == 1:
        if isSavedCookieData(request):
            form = getSavedCookieData(request)
        else:
            form = ManipulateImageForm()
    
 
         
    response = render_to_response(applicationPage(), {
                              'imgForm': imgUploadForm, #imageUpload(reques
                              'form': form,
                              'imagegallery' : gallery,
                              'image': requestImage,
                              'chooseform' : ChooseImageForm(),
                              'cList': pixelPal,
                              'colorList': pixelPal,
                              'instructions': dasInstructions},
                              context_instance = RequestContext(request))

    # Save any valid data to cookie
    if cookieAction == 0:
        saveFormDataToCookie(form, response)
    return response
  
def instructions(request):
    return render_to_response('image_manipulation/instructions.html', context_instance=RequestContext(request))

def getStitchType(needleworkType):
    if needleworkType == '0':
        return "knit"
    elif needleworkType == '1':
        return "crochet"
    elif needleworkType == '2':
        return "crossStitch"

def generateInstructions(stitchTypeNum, array):
    stitchType = getStitchType(stitchTypeNum)

    instructionString = ""
  
    instructionString += stitchType + " abbreviation list:\n"
    #print(stitchType, "abbreviation list:")
    if stitchType == "crochet":
        stitch0 = "ch"
        instructionString += "ch - chain\n"
        #print("ch - chain")
        stitch1 = "sc"
        instructionString += "sc - single crochet\n"
        #print("sc - single crochet")
        stitch2 = "sc"
        stitch3 = "sc"

    elif stitchType == "knit":
        stitch0 = "co"
        instructionString += "co - cast on\n"
        #print("co - cast on")
        stitch1 = "k"
        instructionString += "k - knit\n"
        #print("k - knit")
        stitch2 = "p"
        instructionString += "p - purl\n"
        #print("p - purl")
        stitch3 = "bo"
        instructionString += "bo - bind off\n"
        #print("bo - bind off")

    elif stitchType == "crossStitch":
        stitch0 = "x"
        instructionString += "x - stitch\n"
        print("x - stitch")
        stitch1 = "x"
        stitch2 = "x"
        stitch3 = "x"
    instructionString += "C - color\n"
    #print("C - color")
    instructionString += "row 0 (cast on) reads chart left to right\n"
    #print("row 0 (cast on) reads chart left to right")
    instructionString += "odd rows (purl) reads chart R to L\n"
    #print("odd rows (purl) reads chart R to L")
    instructionString += "even rows (knit) reads chart L to R\n"
    #print("even rows (knit) reads chart L to R")
          

    for y in range(len(array)):
        color = array[y][0]
        count = 0
        instructionString += "Row " + str(y) + ": "
        #print("Row ", y, ":", end=" ", sep="")
        if y % 2 == 1:
            row = reversed(array[y])
        else:
            row = array[y]
        for x in row:  
            if color == x:
                count += 1
            else:
                #row 0 - cast on
                if y == 0:
                    instructionString += str(stitch0) + " " + str(count) + " C" + str(color) + " "
                    #print(stitch0, " ", count," C", color, end=" ", sep="")
                #last rown - bind off
                elif y == len(array) - 1:
                    instructionString += str(stitch3) + " " + str(count) + " C" + str(color) + " "
                    #print(stitch3, " ", count," C", color, end=" ", sep="")
                #odd rows - knit
                elif y % 2 == 1:
                    instructionString += str(stitch1) + " " + str(count) + " C" + str(color) + " "
                    #print(stitch1, " ", count," C", color, end=" ", sep="")
                #even rows - purl
                else:
                    instructionString += str(stitch2) + " " + str(count) + " C" + str(color) + " "
                    #print(stitch2, " ", count," C", color, end=" ", sep="")
                color = x
         
        #row 0 - cast on
        if y == 0:
            instructionString += str(stitch0) + " " + str(count) + " C" + str(color) + "\n"
            #print(stitch0, " ", count," C", color, sep="")
            #last rown - bind off
        elif y == len(array) - 1:
            instructionString += str(stitch3) + " " + str(count) + " C" + str(color) + "\n"
            #print(stitch3, " ", count," C", color, sep="")
            #odd rows - knit
        elif y % 2 == 1:
            instructionString += str(stitch1) + " " + str(count) + " C" + str(color) + "\n"
            #print(stitch1, " ", count," C", color, sep="")
            #even rows - purl
        else:
            instructionString += str(stitch2) + " " + str(count) + " C" + str(color) + "\n"
            #print(stitch2, " ", count," C", color, sep="")
        
    instructionString += "Snip yarn/thread and weave in ends"
    return instructionString
