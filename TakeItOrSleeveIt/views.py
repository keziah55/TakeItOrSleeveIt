from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .models import Album, Question


def index(request):
    all_albums = Album.objects.all()
    q = Question(all_albums)
    albums = q.getAlbums()
    
    # Increment number of contests for chosen albums
    # TODO: think of better way to do this. If someone continually refreshes
    # the page, number of contests will be updated, even though neither won.
    # Find a way to do this in vote()
#    for album in albums:
#        album.contests += 1
#        album.save()
        
    context = {'album0':albums[0],
               'album1':albums[1]}
    
    return render(request, 'TakeItOrSleeveIt/index.html', context)


def results(request):
    response = "The rankings"
    return HttpResponse(response)


def vote(request):
    
    # Keys will be 'csrfmiddlewaretoken', 'ID.x', 'ID.y', where ID is the id
    # of the selected album
    # There must be a better way of doing this...
    keys = list(request.POST.keys())
    keys.remove('csrfmiddlewaretoken')
    album_id = keys[0] # take the first remaining key
    album_ids, _ = album_id.split('.') # get the ID, remove the 'x' (or 'y')
    album_ids = album_ids.split('_')
    album_ids = [int(album_id) for album_id in album_ids]
    
    for idx, album_id in enumerate(album_ids):
        album = Album.objects.get(id=album_id)
        if idx == 0:
            album.votes += 1
        album.contests += 1
        album.rating = 100 * (album.votes / album.contests) # % rating
        album.save()

        
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('TakeItOrSleeveIt:index', 
                                        args=()))
