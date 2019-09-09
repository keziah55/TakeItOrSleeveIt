from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Album, Question

import re

def index(request):
    # get all albums
    all_albums = Album.objects.all()
    # make Question object
    q = Question(all_albums)
    # get two albums
    albums = q.getAlbums()   
    # make context for template     
    context = {'album0':albums[0],
               'album1':albums[1]}
    
    return render(request, 'TakeItOrSleeveIt/index.html', context)


def results(request):
    
    # see if the `request` object has a 'search' item
    try:
        search = request.GET['search']
    # if not, use empty string
    except:
        search = ''
    
    # search title, artist and year fields for the `search` string
    a1 = Album.objects.filter(title__icontains=search)
    a2 = Album.objects.filter(artist__icontains=search)
    a3 = Album.objects.filter(year__icontains=search)
    # merge the filtered datasets
    results = a1 | a2 | a3
    # sort albums by rating, in descending order
    sorted_album_list = results.order_by('-rating')
    
    # make string to display in search bar
    if search:
        search_placeholder = "Showing results for: '{}'".format(search)
    else:
        search_placeholder = 'Search...'
    
    # args to be substituted into the templates    
    context = {'sorted_album_list':sorted_album_list,
               'search_placeholder':search_placeholder}
    
    return render(request, 'TakeItOrSleeveIt/results.html', context)


def vote(request):
    
    # Keys will be 'csrfmiddlewaretoken', 'ID0_ID1.x', 'ID0_ID1.y', 
    # where ID0 is the id of the selected album and ID1 is the id of the other
    # album presented.
    # There must be a better way of doing this...
    
    # regex to extract the IDs
    regex = re.compile(r'(\d+)_(\d+)\.x')
    
    # for each key, check if regex matches
    keys = list(request.POST.keys())
    for key in keys:
        srch = regex.search(key)
        if srch is not None:
            # get IDs as list of ints
            album_ids = [int(srch.group(i)) for i in [1,2]]
            break
    
    # For both IDs, increment the number of contests and update the rating
    # For the first ID, increment the number of votes
    for idx, album_id in enumerate(album_ids):
        album = Album.objects.get(id=album_id)
        if idx == 0:
            album.votes += 1
        album.contests += 1
        try:
            album.rating = 100 * (album.votes / album.contests) # % rating
        except ZeroDivisionError:
            album.rating = 0
        album.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('TakeItOrSleeveIt:index', args=()))
    
    
