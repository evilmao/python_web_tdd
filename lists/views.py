from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def home_page(request):
    if request.method == 'POST':
        context = {'new_item_text':request.POST.get('item_text','')}
        return render(request,'home.html',context)
    return render(request,'home.html',)