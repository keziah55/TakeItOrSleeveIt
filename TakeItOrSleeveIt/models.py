from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    img = models.CharField(max_length=200)
    
    votes = models.PositiveIntegerField() # no. of times been voted for
    contests = models.PositiveIntegerField() # no. of times presetned to users
    rating = models.FloatField() # 100*votes/contests %
    
    def __str__(self):
        s = self.title + ', ' + self.artist
        return s
