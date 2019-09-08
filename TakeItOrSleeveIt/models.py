from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    def __str__(self):
        return self.question_text

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
    rating = models.FloatField(default=0) 
    
    def __str__(self):
        s = "{}, {} ({})".format(self.title, self.artist, self.year)
        return s
