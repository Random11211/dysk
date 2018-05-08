from django.shortcuts import render
from django.template import RequestContext
from books.models import Plik
from django.http import HttpResponse

# Create your views here.

#def index(request):
 #   return HttpResponse("Hello")



def index(request):
    context = RequestContext(request)
    plik = Plik.objects.create(adres="adres", nazwa="pliczek")
    context_dict = {"file": plik}

    return render(request, 'home.html', context_dict)
