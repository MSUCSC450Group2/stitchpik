from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from .forms import *

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
            
            # put image in variables field
            # variables = RequestContext(request, { 'image':'' })
            variables = RequestContext(request, { 'form':form, 'image':'image_manipulation/img/bubblegum.jpg'})
            return render_to_response('image_manipulation/applicationPage.html', variables)
    else:
        form = ManipulateImageForm()
    
    variables = RequestContext(request, { 'image':'image_manipulation/img/bubblegum.jpg', 'form':form })
        
    return render_to_response('image_manipulation/applicationPage.html', variables)     

