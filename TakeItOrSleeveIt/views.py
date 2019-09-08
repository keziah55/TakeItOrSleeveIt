from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import ListView
from .models import Album, Question


class ResultsView(ListView):
    template_name = 'TakeItOrSleeveIt/results.html'
    context_object_name = 'sorted_album_list'
    
    def get_queryset(self):
        """Return the albums, sorted by rating, in descending order."""
        return Album.objects.order_by('-rating')


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


#def results(request):
#    # sort albums by rating, in descending order
#    sorted_album_list = Album.objects.order_by('-rating')
#    context = {'sorted_album_list':sorted_album_list}
#    return render(request, 'TakeItOrSleeveIt/results.html', context)


def vote(request):
    
    # Keys will be 'csrfmiddlewaretoken', 'ID0_ID1.x', 'ID0_ID1.y', 
    # where ID0 is the id of the selected album and ID1 is the id of the other
    # album presented.
    # (here must be a better way of doing this...
    keys = list(request.POST.keys())
    keys.remove('csrfmiddlewaretoken')
    album_id = keys[0] # take the first remaining key
    album_ids, _ = album_id.split('.') # get the ID, remove the 'x' (or 'y')
    album_ids = album_ids.split('_') # split into the two IDs
    album_ids = [int(album_id) for album_id in album_ids]
    
    # For both IDs, increment the number of contests and the rating
    # For the first ID, increment the number of votes
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
    
    
