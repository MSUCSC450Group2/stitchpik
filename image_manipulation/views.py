from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from .forms import *
from .manipulate_lib.imageclass import *
from .models import Image
from image_manipulation.models import Image
import time

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
   
def saveFormDataToCookie(form, request):
    return

def isSavedCookieData(request):
    return request.COOKIES.get('savedFormOptions', None)

def getSavedCookieData(savedOptions):
    return ManipulateImageForm( {
        'numberOfColors':int(savedOptions.get('numberOfColors')),
        'guageSize':float(savedOptions.get('guageSize')),
        'canvasLength':float(savedOptions.get('canvasLength')),
        'canvasWidth':float(savedOptions.get('canvasWidth')),
        'knitType':int(savedOptions.get('knitType'))
    } )
#    return ManipulateImageForm(
#        {
#        'numberOfColors':int(request.COOKIE.get('numberOfColors')),
#        'guageSize':float(request.COOKIES.get('guageSize')),
#        'canvasLength':float(request.COOKIES.get('canvasLength')),
#        'canvasWidth':float(request.COOKIES.get('canvasWidth')),
#        'knitType':int(request.COOKIES.get('knitType'))
#        } )



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

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60 
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

@login_required
def fetchApplication(request):
    inputImage = Image.latestUserImageFile(request.user)
    resultImage = 'media/result.jpg'
    requestImage = inputImage

    if request.method == 'POST':
        form = ManipulateImageForm(request.POST) 
        if form.is_valid():
            requestImage = "../" + resultImage
            numColors = form.cleaned_data['numberOfColors']
            pixSize = 8
            pic = Picture(inputImage)
            pic.pixelate(numColors, pixSize, resultImage)
            time.sleep(5) #TODO: REPLACE WITH JQUERY
            saveFormDataToSession(form, request)
            cookieAction = 0;
        else:
            form = ManipulateImageForm()
            if isSavedSessionData(request):
                savedOptions = request.session.get('savedFormOptions')
                form = savedSessionData(savedOptions)
                coookieAction = 1;
    else:
        if isSavedSessionData(request):
            savedOptions = request.session.get('savedFormOptions')
            form = savedSessionData(savedOptions)
            cookieAction = 2;
        else:
            form = ManipulateImageForm()
            cookieAction=3;

    response = render_to_response(applicationPage(), {'imgForm': imageUpload(request), 
                              'form' : form, 
                              'image' : requestImage },
                              context_instance = RequestContext(request))

    # meddle with saved cookie information
    # if new valid inputs
    if cookieAction = 0:
        saveFormDataToCookie(response, form)
    elif cookieAction = 1:
        if isSavedCookieDate(request)

    # if cookie data can be used

    # if no cookie data

    return response

