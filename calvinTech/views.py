from django.shortcuts import render

# Create your views here.
def index(request):
    response = render(request, 'index.html')
    return response

def DS8660_Module4(request):
    response = render(request, 'DS8660_Module4.html')
    return response