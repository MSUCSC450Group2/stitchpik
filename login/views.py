from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
  return render_to_response("index.html", locals(),
			    context_instance = RequestContext(request))


def loginTry(request):
    
    if request.method == 'POST' and request.POST.get('username', False) != False:
        form = RegistrationForm(request.POST)
    else:
        form = RegistrationForm()

    # check the authentication
    user = authenticate(username=request.POST.get('username', None), password=request.POST.get('password', None))
    if user is not None:
        if user.is_active:
            login(request, user)
            # redirect to success page
            return render(request, 'login/loginSuccess.html')
        else:
            # return a 'disabled account'
            return render(request, 'login/registration/login.html')
    else:
        variables = RequestContext(request, { 'form':form })
        return render_to_response('login/registration/login.html', variables)

def registration(request):
    if request.method == 'POST':
        # Use created forms.py 
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            # Not sure if it checks uniqueness of user name
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'])
            return HttpResponseRedirect('/registration/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, { 'form':form, })
        
    return render_to_response('login/registration/registration.html', variables)

def registrationSuccess(request):
    return render(request, 'login/registration/success.html')

def logoutPage(request):
    logout(request)
    return HttpResponseRedirect('/')

#@login_required
#def home(request):
#    return render_to_response('login/index.html', { 'user':request.user })





