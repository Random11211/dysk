from django.contrib.auth import get_user_model
from django.db import models


class Plik(models.Model):
    id = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    adres = models.FileField(upload_to='media/')
    size_format = models.CharField(max_length=10)
    czy_udostepniony = models.BooleanField(default=False)


class Katalog(models.Model):
    id = models.IntegerField(primary_key=True)
    nazwa = models.CharField(max_length=50)
    lista_plikow = models.ManyToManyField(Plik)


class Konto(models.Model):
    konto = models.IntegerField(primary_key=True)
    pojemnosc = models.IntegerField()
    uzytkownik = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class Struktura_Konta(models.Model):
    konto = models.ForeignKey(Konto, on_delete=models.CASCADE)
    lista_katalogow = models.ManyToManyField(Katalog)


class Dysk(models.Model):
    lista_kont = models.ManyToManyField(Konto)
