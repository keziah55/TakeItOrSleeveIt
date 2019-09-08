from django.contrib import admin

from .models import Album

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'votes', 'contests', 'rating')
    search_fields = ['title', 'artist', 'year']

admin.site.register(Album, AlbumAdmin)
