import io
import os
import cv2
import torch
import shutil
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
    print(image)
    return render(request, 'upload.html', data)

# Use this to modify Contact Detection Performance
model_weight = 'test.pt'
threshold_value = 0.05

# IMAGE DETECTION AND INTERACTION
def results(request):
    # GET UPLOADED IMAGE
    image = UploadImage.objects.all().last()
    img_bytes = image.image.read()
    img = im.open(io.BytesIO(img_bytes))

    ## DETECTION METHOD
    # LOADING THE MODEL (can be loaded remotely)
    # path_hubconfig = "joackinsantos/YOLOv5-Modification:website-integration"
    path_hubconfig = "YOLOv5-Modification"
    path_weightfile = f"best-weights/{model_weight}"
    model = torch.hub.load(path_hubconfig, 'custom',
                           path=path_weightfile, source='local',
                           force_reload=True)
    results = model(img, size=600)

    # PROCESSING DETECTED IMAGE
    # remove previous detected image directory to save space
    detect_image_path = 'runs/detect'
    exp_path = f'{detect_image_path}/exp'
    if os.path.exists(exp_path):
        shutil.rmtree(exp_path)
    # creates new detected image
    results.print()
    results.save()
    # move directory and change image name
    old_path = f'{detect_image_path}/exp/image0.jpg'
    new_path = f'{detect_image_path}/image0.jpg'
    output_path = f'{detect_image_path}/detect-{str(image)}'
    if not os.path.exists(new_path) and not os.path.exists(output_path):
        shutil.move(old_path, new_path)     # move to non refreshed dir
        os.rename(new_path, output_path)    # rename detected image

    ## INTERACTION METHOD
    # bb = bounding box
    bb = results.pandas().xyxy[0]
    iou_threshold = threshold_value
    results_df = pd.DataFrame(columns=['Classification', 'Interaction_Count'])
    interaction_flag = False
    interaction_count = 0

    # separating by class names
    head_df = bb[bb['name'] == 'Head'].reset_index(drop=True)
    rear_df = bb[bb['name'] == 'Rear'].reset_index(drop=True)

    # loop over heads and rears in the image
    for i, head_row in head_df.iterrows():
        for j, rear_row in rear_df.iterrows():
            # bounding box indexing
            # df[0] = minX, df[1] = minY, df[2] = maxX, df[3] = maxY

            head_minX = head_df.iloc[i, 0]
            head_minY = head_df.iloc[i, 1]
            head_maxX = head_df.iloc[i, 2]
            head_maxY = head_df.iloc[i, 3]

            rear_minX = rear_df.iloc[j, 0]
            rear_minY = rear_df.iloc[j, 1]
            rear_maxX = rear_df.iloc[j, 2]
            rear_maxY = rear_df.iloc[j, 3]

            curr_iou = compute_iou(head_minX, head_maxX, head_minY, head_maxY,
                        rear_minX, rear_maxX, rear_minY, rear_maxY)
            
            # print(curr_iou)
            if(curr_iou >= iou_threshold):
                interaction_flag = True
                interaction_count += 1
    
    temp_list = [1 if interaction_flag else 0,
                 interaction_count]
    results_df.loc[len(results_df)] = temp_list

    row = results_df.iloc[0]
    classification = 'With Contact' if row['Classification'] == 1 else "Without Contact"
    count = row['Interaction_Count']

    data = {
        'image': f'../{output_path}',
        'class': classification,
        'interaction_count': count
    }

    return render(request, 'results.html', data)

def test(request):
    return render(request, 'test.html')



# FUNCTIONS
def compute_iou(head_minX, head_maxX, head_minY, head_maxY, rear_minX, rear_maxX, rear_minY, rear_maxY):
    # determine (x,y) coordinates of the intersection rectangle
    x_left = max(head_minX, rear_minX)
    y_top = max(head_minY, rear_minY)
    x_right = min(head_maxX, rear_maxX)
    y_bottom = min(head_maxY, rear_maxY)

    # compute the area of intersection rectangle
    intersection_area = max(0, x_right - x_left + 1) * max(0, y_bottom - y_top + 1)

    # compute area of both prediction and ground-truth
    # rectangles
    headArea = (head_maxX - head_minX + 1) * (head_maxY - head_minY + 1)
    rearArea = (rear_maxX - rear_minX + 1) * (rear_maxY - rear_minY + 1)
    union_area = float(headArea + rearArea - intersection_area)

    # compute IoU
    iou = intersection_area / union_area
    return iou

# USEFUL TESTERS
# Tester for Head and Rear dfs
# use to test order
# print(head_df.head())
# print(rear_df.head())
# head_minX = head_df.iloc[0, 0]
# head_minY = head_df.iloc[0, 1]
# head_maxX = head_df.iloc[0, 2]
# head_maxY = head_df.iloc[0, 3]
# print(head_minX, head_minY, head_maxX, head_maxY)