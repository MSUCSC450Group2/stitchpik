from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("this is the logo page")

def loginSuccess(request):
    return HttpResponse("Successfull login")

def loginFailure(request):
    return HttpResponse("Failed login")









