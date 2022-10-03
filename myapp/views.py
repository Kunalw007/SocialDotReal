from operator import index
from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    context={
        'device':'Hello world'
    }
    return render(request,"index.html",context)
    # return HttpResponse("This is Home Page")
def about(request):
    # return HttpResponse("This is about Page")
    return render(request,"about.html")

def detector(request):
    return render(request,"detector.html")

def contactus(request):
    return render(request,"contactus.html")
