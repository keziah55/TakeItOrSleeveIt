from django.http import HttpResponse
#from django.template import loader
from django.shortcuts import render
from .models import Album

import random

def index(request):
#    response = "Hello, world. You're at the Take It Or Sleeve It index."
#    response = "Choose your favourite cover!"
    
    all_albums = Album.objects.all()
    n = len(all_albums)
    k = 2
    idx = random.sample(range(n),k)
    albums = [all_albums[i] for i in idx]
    
#    template = loader.get_template('TakeItOrSleeveIt/index.html')
    context = {'album0':albums[0],
               'album1':albums[1]}
    
    return render(request, 'TakeItOrSleeveIt/index.html', context)
#    return HttpResponse(response)

def results(request):
    response = "The rankings"
    return HttpResponse(response)

#def vote(request):
#    response = "Choose your favourite cover!"
#    return HttpResponse(response)
