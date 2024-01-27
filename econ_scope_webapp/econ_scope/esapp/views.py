from django.shortcuts import render
from django.http import HttpResponse
import cv2
import threading

def home(request): 
    if request.method == 'POST':
        image_file = request.FILES['image']
        with open('photo.jpg', 'wb') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

    return render(request, 'es/home.html')

def about(request): 
    return HttpResponse('<h1>About</h1>')

