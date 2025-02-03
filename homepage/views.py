from django.shortcuts import render

def home(request):
    return render(request, 'homepage/base.html')
# Create your views here.
