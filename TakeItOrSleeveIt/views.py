from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the Take It Or Sleeve It index.")