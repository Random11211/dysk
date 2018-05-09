from django.shortcuts import render
from books.models import Plik

# Create your views here.

#def index(request):
 #   return HttpResponse("Hello")


def index(request):
    plik = Plik.objects.create(adres="adres", nazwa="pliczek")
    context_dict = {"file": plik}

    return render(request, 'home.html', context_dict)


def test(request):
    return render(request, 'test.html')


def test2(request):
    return render(request, 'test2.html')
