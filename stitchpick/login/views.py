from django.shortcuts import render, render_to_repsonse
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from login.forms import *
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def loginTry(request):
    # check the authentication
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            # redirect to success page
            return render_to_response('index.html')
        else:
            # return a 'disabled account'
            return render_to_response('login.html')
    else:
        tries = int(request.POST['tries']) + 1
        if tries == 3:
            # Fail at three tries
            return render_to_response('failure.html', { "tries":"3" })
        else:
            # return invalid login
            return render_to_response('login.html', { "tries":str(tries) })

def signUp(request):
    if request.method == 'POST':
        # Use created forms.py 
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            # Not sure if it checks uniqueness of user name
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'])
            HttpResponseRedirect('/signup/success.html')
        else:
            form = SignupForm()
        variables = RequestContext(request, { 'form':form })
        
        return render_to_response('signup/signup.html', variables)

def signupSuccess(request):
    return render_to_response('/signup/success/')

def logoutPage(request):
    logout(request)
    return HttpResponseRedirect('/')

def home(request):
    return render_to_response('/home/', { 'user':request.user })





