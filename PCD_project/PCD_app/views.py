from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    obj = NameTester.objects.all()
    data = {
        'obj':obj,
    }
    return render(request, 'home.html', data)

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