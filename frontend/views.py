from django.shortcuts import render
from django.shortcuts import render


# Create your views here.

def search(request):
    return render(request, 'frontend\search.html')


