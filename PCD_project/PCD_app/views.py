import io
import os
import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image as im
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView
from .models import *

# Create your views here.
# def home(request):
#     obj = NameTester.objects.all()
#     data = {
#         'obj':obj,
#     }
#     return render(request, 'home.html', data)

class ProcessImage(CreateView):
    print("hello")

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
    images = UploadImage.objects.all().last()
    data = {
        'images':images,
    }
    return render(request, 'upload.html', data)

def results(request):
    images = UploadImage.objects.all().last()
    data = {
        'images':images,
    }
    return render(request, 'results.html', data)

def test(request):
    return render(request, 'test.html')