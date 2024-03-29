from django.urls import path

from . import views

app_name = 'TakeItOrSleeveIt'

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('vote/', views.vote, name='vote'),
]