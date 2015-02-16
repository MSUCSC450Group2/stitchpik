from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from login.forms import *
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

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
        # Use created form.py 
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            # Not sure if it checks uniqueness of user name
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'])
            HttpResponseRedirect('/signup/success.html')
        else:
            form = RegistrationForm()
        variables = RequestContext(request, { 'form':form})
        
        return render_to_response('signup/signup.html', variables)

def signupSuccess(request):
    return render_to_response('signup/success.html')

def logoutPage(request):
    logout(request)
    return HttpResponseRedirect('/')

def home(request):
    return render_to_response('index.html', {'user':request.user})





