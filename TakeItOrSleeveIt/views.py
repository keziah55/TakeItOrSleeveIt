from django.http import HttpResponse

def index(request):
#    response = "Hello, world. You're at the Take It Or Sleeve It index."
    response = "Choose your favourite cover!"
    return HttpResponse(response)

def results(request):
    response = "The rankings"
    return HttpResponse(response)

#def vote(request):
#    response = "Choose your favourite cover!"
#    return HttpResponse(response)
