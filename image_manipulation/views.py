from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from .forms import *
from .manipulate_lib.imageclass import *
from .models import Image
from image_manipulation.models import Image

def applicationPage():
    return 'image_manipulation/applicationPage.html'

def newUploadedImage(request):
    return Image(imgFile = request.FILES['imgFile'], user = request.user, private = True)

def imageUpload(request):
    imgForm = ImageUploadForm(request.POST, request.FILES)
    if imgForm.is_valid():
        newImg = newUploadedImage(request)
        newImg.save()
    else:
        imgForm = ImageUploadForm()
    return imgForm  
   
def saveFormDataToSession(request):
    request.session.set_expiry(31536000) # 1 year
    request.session['savedFormOptions'] = {
        'numberOfColors': int(form.cleaned_data['numberOfColors']), 
        'guageSize': int(form.cleaned_data['guageSize']), 
        'canvasLength': int(form.cleaned_data['canvasLength']),
        'canvasWidth': int(form.cleaned_data['canvasWidth']), 
        'knitType': int(form.cleaned_data['knitType'])
    }

def isSavedSessionData(request):
    return request.session.get('savedFormOptions')

def savedSessionData(savedOptions):
    return ManipulateImageForm(
            {'numberOfColors': int(savedOptions.get('numberOfColors')),
             'guageSize': int(savedOptions.get('guageSize')),
             'canvasLength': int(savedOptions.get('canvasLength')),
             'canvasWidth': int(savedOptions.get('canvasWidth')),
             'knitType': int(savedOptions.get('knitType')) }
           )

def fetchApplication(request):
    inputImage = 'image_manipulation/static/image_manipulation/img/bubblegum.jpg'
    resultImage = 'image_manipulation/static/image_manipulation/img/bubblegum2.jpg'
    requestImage = inputImage
    if request.method == 'POST':
        form = ManipulateImageForm(request.POST)
        if form.is_valid():
            requestImage = resultImage
            numColors = form.cleaned_data['numberOfColors']
            pixSize = 8
            pic = Picture(inputImage)
            pic.pixelate(numColors, pixSize, resultImage)
            saveFormDataToSession(request)
    else:
        form = ManipulateImageForm()
        if isSavedSessionData(request):
          savedOptions = request.session.get('savedFormOptions')      
          form = savedSessionData(savedOptions)
        else:
          form = ManipulateImageForm()
    return render_to_response(applicationPage(), {'imgForm': imageUpload(request), 
                              'form' : form, 
                              'image' : requestImage },
                              context_instance = RequestContext(request))

