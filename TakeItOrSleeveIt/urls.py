from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('vote/', views.vote, name='vote'),
]