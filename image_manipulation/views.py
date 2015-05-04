from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from .manipulate_lib.imageclass import *
from .models import Image
from image_manipulation.models import Image
import time

def getUserImages(request):
    if request.method == 'POST':
        chooseform = ChooseImageForm(request.POST)
        if chooseform.is_valid():
            gallery = Image.userImages(request.user)
            imagesDiv=""
            for x in gallery:
                imagesDiv=imagesDiv + '<img src="../media/'+ str(x.imgFile) +'"/>'
            resultImage = 'media/result.jpg'
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
    if imgForm.is_valid():
        newImg = newUploadedImage(request)
        newImg.save()
    else:
        imgForm = ImageUploadForm()
    return imgForm
   

    
    
def saveFormDataToSession(form, request):
    request.session.set_expiry(31536000) # one year
    request.session['savedFormOptions'] = {
        'numberOfColors': int(form.cleaned_data['numberOfColors']), 
        'guageSize': float(form.cleaned_data['guageSize']), 
        'canvasLength': float(form.cleaned_data['canvasLength']),
        'canvasWidth': float(form.cleaned_data['canvasWidth']), 
        'knitType': int(form.cleaned_data['knitType'])
    }

def isSavedSessionData(request):
    return request.session.get('savedFormOptions')

def savedSessionData(savedOptions):
    return ManipulateImageForm(
            {'numberOfColors': int(savedOptions.get('numberOfColors')),
             'guageSize': float(savedOptions.get('guageSize')),
             'canvasLength': float(savedOptions.get('canvasLength')),
             'canvasWidth': float(savedOptions.get('canvasWidth')),
             'knitType': int(savedOptions.get('knitType')) }
           )


def saveImageChoice(request, imagePath):
    if imagePath != "":   
        request.session.set_expiry(0)
        request.session['imageChoice'] = imagePath
        
def loadImageChoice(request):
    return request.session.get('imageChoice', "")

def clearImageChoice(request):
    if loadImageChoice(request) != "":
        del request.session['imageChoice']
    


@login_required
def fetchApplication(request):
    selectedImage=""
    inputImage = Image.latestUserImageFile(request.user)
    #imagechooser setup
    
    gallery = Image.userImages(request.user)
    

    resultImage = 'media/result.jpg'
    requestImage = inputImage
    imgForm = ChooseImageForm(request.POST)
    

    if request.method == 'POST':
        if imgForm.is_valid():
            print('set select')
            print(inputImage)
            print(imgForm.cleaned_data['chosenImage'])
            if (request.POST.get("changebutton")):
                #print(inputImage)
                chosenImage=imgForm.cleaned_data['chosenImage']
                saveImageChoice(request, chosenImage)
                #print('changed')
                #print(inputImage) 
        form = ManipulateImageForm(request.POST) 
        print('check')  
        print(selectedImage)        
        print(inputImage)
         
            
        if form.is_valid():
            print('valid')
            print(inputImage)
            requestImage = '../' + resultImage
            numColors = form.cleaned_data['numberOfColors']
            pixSize = 8
            lastImage=form.cleaned_data['lastChosenImage']
            print('pixelate')
            print(selectedImage)
            print(inputImage)
            if (selectedImage != ""):
                inputImage = selectedImage
            pic = Picture(inputImage)
            print(resultImage)
            selectedImage = ""
            pic.pixelate(numColors, pixSize, resultImage)
            #time.sleep(5) #TODO: REPLACE WITH JQUERY
            saveFormDataToSession(form, request)
        else:
                
            if isSavedSessionData(request):
                savedOptions = request.session.get('savedFormOptions')
                form = savedSessionData(savedOptions)
    else:
        if isSavedSessionData(request):
            savedOptions = request.session.get('savedFormOptions')
            form = savedSessionData(savedOptions)
        else:
            form = ManipulateImageForm()
    
    return render_to_response(applicationPage(), {'imgForm': imageUpload(request), 
                              'form' : form, 
                              'imagegallery' : gallery, 
                               'chooseform' : ChooseImageForm(),
                              'input' : selectedImage,
                              'image' : requestImage },
                              context_instance = RequestContext(request))

