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

# class ProcessImage(CreateView):
#     print("hello")

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
    image = UploadImage.objects.all().last()
    data = {
        'image':image,
    }
    return render(request, 'upload.html', data)

# this is where image detection and interaction happens
def results(request):
    # getting the image
    image = UploadImage.objects.all().last()
    img_bytes = image.image.read()
    img = im.open(io.BytesIO(img_bytes))

    path_hubconfig = "joackinsantos/YOLOv5-Modification"
    path_weightfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'best-weights', 'test.pt')

    model = torch.hub.load(path_hubconfig, 'custom',
                           path=path_weightfile, source='github',
                           force_reload=True)
    
    results = model(img, size=400)
    results.render()

    for img in results.imgs:
        img_base = im.fromarray(img)
        img_base.save("pig-images/yolo_out/image0.jpg", format="JPEG")
    
    inference_img = "pig-images/yolo_out/image0.jpg"

    data = {
        'image':inference_img,
    }

    return render(request, 'results.html', data)

def test(request):
    return render(request, 'test.html')