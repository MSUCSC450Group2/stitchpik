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
      #currently runs properly every time, if image is not done processing when page loads the image is not displayed.
      #can possibly fix with adding a delayed load to the image through jquery or similar.
      pic.pixelate(numColors, pixSize, resultImage)

      # Add variables to session
      request.session.set_expiry(31536000) # 1 year
			
			# Add logic to specify picture id
			request.session['picId'] = {'numberOfColors':form.cleaned_data['numberOfColors'], 'guageSize':form.cleaned_data['guageSize'], 'canvasLength':form.cleaned_data['canvasLength'],'canvasWidth':form.cleaned_data['canvasWidth'], 'knitType':form.cleaned_data['knitType']}

      variables = RequestContext(request, { 'form':form, 'image':'image_manipulation/img/bubblegum2.jpg'})
      return render_to_response('image_manipulation/applicationPage.html', variables)
    else:
      form = ManipulateImageForm()
		
			# Check if there is session data for the picture
			if request.session.get('picId'):
				form = ManipulateImageForm({'numberOfColors':

    variables = RequestContext(request, { 'form':form, 'image':'image_manipulation/img/bubblegum.jpg'})
        
    return render_to_response('image_manipulation/applicationPage.html', variables)     

