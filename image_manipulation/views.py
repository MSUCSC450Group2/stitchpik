from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from .forms import *
from .manipulate_lib.imageclass import *


# Create views here

# open application page
# take in data 
# serve up image and parameters
def fetchApplication(request):
  # if readying to edit image
  if request.method == 'POST':
    form = ManipulateImageForm(request.POST)
    if form.is_valid():
      # Use data to serve up image
      numColors = form.cleaned_data['numberOfColors']
      pixSize = 8
            
      pic = Picture('image_manipulation/static/image_manipulation/img/bubblegum.jpg')
      resultImage = 'image_manipulation/static/image_manipulation/img/bubblegum2.jpg'
      pic.pixelate(numColors, pixSize, resultImage)

      # Add variables to session
      request.session.set_expiry(31536000) # 1 year
      
      # save in dictionary for savedForm
      request.session['savedFormOptions'] = {'numberOfColors':int(form.cleaned_data['numberOfColors']), 'guageSize':int(form.cleaned_data['guageSize']), 'canvasLength':int(form.cleaned_data['canvasLength']),'canvasWidth':int(form.cleaned_data['canvasWidth']), 'knitType':int(form.cleaned_data['knitType'])}

      # save form variables
      variables = RequestContext(request, { 'form':form, 'image':'image_manipulation/img/bubblegum2.jpg'})
      return render_to_response('image_manipulation/applicationPage.html', variables)
  else:
    # Check for session data and load it
    if request.session.get('savedFormOptions'):
      savedOptions = request.session.get('savedFormOptions')      

      form = ManipulateImageForm({'numberOfColors':int(savedOptions.get('numberOfColors')),'guageSize':int(savedOptions.get('guageSize')),'canvasLength':int(savedOptions.get('canvasLength')),'canvasWidth':int(savedOptions.get('canvasWidth')),'knitType':int(savedOptions.get('knitType'))})

    else:
      form = ManipulateImageForm()

    variables = RequestContext(request, { 'form':form, 'image':'image_manipulation/img/bubblegum.jpg'})
        
    return render_to_response('image_manipulation/applicationPage.html', variables)     


