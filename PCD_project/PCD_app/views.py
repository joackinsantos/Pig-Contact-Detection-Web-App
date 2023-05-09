from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
# def home(request):
#     obj = NameTester.objects.all()
#     data = {
#         'obj':obj,
#     }
#     return render(request, 'home.html', data)

def home(request):
    if request.method == "POST":
        image = UploadImage()
        if len(request.FILES) != 0:
            image.image = request.FILES['image']

        image.save()
        messages.success(request, "Image Uploaded!")
        return redirect('upload/')
    return render(request, 'home.html')

def upload(request):
    obj = NameTester.objects.all()
    data = {
        'obj':obj,
    }
    return render(request, 'upload.html', data)

def results(request):
    obj = NameTester.objects.all()
    data = {
        'obj':obj,
    }
    return render(request, 'results.html', data)

def test(request):
    obj = NameTester.objects.all()
    data = {
        'obj':obj,
    }
    return render(request, 'test.html', data)