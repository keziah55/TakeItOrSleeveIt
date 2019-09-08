from django.db import models

import random

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    img = models.CharField(max_length=200)
    
    # no. of times been voted for
    votes = models.PositiveIntegerField(default=0) 
    # no. of times presented to users
    contests = models.PositiveIntegerField(default=0) 
    # 100*votes/contests %
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=0) 
    
    def __str__(self):
        s = "{}, {} ({})".format(self.title, self.artist, self.year)
        return s

class Question(models.Model):
    
    def __init__(self, all_albums):
        self.all_albums = all_albums
        
    def getAlbums(self):
        n = len(self.all_albums)
        k = 2
        idx = random.sample(range(n),k)
        self.albums = [self.all_albums[i] for i in idx]
        return self.albums
    
    def __str__(self):
        if self.albums:
            s = "{} or {}".format(*self.albums)
        else:
            s = ''
        return s
