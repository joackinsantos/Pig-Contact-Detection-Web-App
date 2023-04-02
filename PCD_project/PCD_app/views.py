from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    obj = NameTester.objects.all()
    data = {
        'obj':obj,
    }
    return render(request, 'home.html', data)