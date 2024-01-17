from django.shortcuts import render
from django.http import HttpResponse
import cv2
import threading

def home(request): 
    return render(request, 'es/home.html')

def about(request): 
    return HttpResponse('<h1>About</h1>')

