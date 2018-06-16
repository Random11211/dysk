from django.http import Http404
from django.http import HttpResponse
from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
)

from django.core.mail import send_mail
from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect

from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from books.models import Plik
from books.models import Struktura_Konta
from books.models import Katalog
from books.forms import UploadFileForm, NewDirectory
from books.models import Konto
from books.models import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from books.forms import SignUpForm

# Create your views here.

def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    #czyszczenie bazy danych, odkomentowac tylko w razie koniecznosci

    #Plik.objects.all().delete()
    #Katalog.objects.all().delete()
    #User.objects.all().delete()
    #Struktura_Konta.objects.all().delete()

    return render(request, 'home.html')


def currentAccount(user):
    return Konto.objects.get(uzytkownik=user)


def file_uploadable(konto : Konto, file_size):
    if left_space(konto) + file_size >= 0:
        return True
    return False


def UserFiles(konto: Konto, katalog):
    pliki = Struktura_Konta.objects.get(konto=konto).lista_katalogow.get(nazwa=katalog).lista_plikow.all()
    return pliki


def left_space(konto: Konto):
    katalogi = Struktura_Konta.objects.get(konto=konto).lista_katalogow.all()
    size = 0
    for i in katalogi:
        pliki = i.lista_plikow.all()
        for j in pliki:
            size += j.adres.size
    return konto.pojemnosc - size


def NameIsFree(name):
    return Plik.objects.filter(nazwa=name).exists()


def SizePresentation(pojemnosc):
    return True


def CatalogFree(konto: Konto, name):
    return Struktura_Konta.objects.get(konto=konto).lista_katalogow.filter(nazwa=name).exists()


def file_available(request, file_id):
    return HttpResponse("You want file %s." % file_id)


def directory_create(request):
    context_dict = {}
    konto = currentAccount(request.user)
    if request.method == 'POST' and 'directory' in request.POST:
        form = NewDirectory(request.POST)
        if form.is_valid():
            if not CatalogFree(konto, form.data['nazwa']):
                form.save()
                katalog = Katalog.objects.last()
                Struktura_Konta.objects.get(konto=konto).lista_katalogow.add(katalog)
                return redirect('/storage_control/')

    form = NewDirectory()
    context_dict["form"] = form
    return render(request, 'directory_create.html', context_dict)


def file_upload(request):
    context_dict = {}
    konto = currentAccount(request.user)
    id = request.session['current_id']
    katalog = Struktura_Konta.objects.get(konto=konto).lista_katalogow.get(id=id)
    if request.method == 'POST' and 'file' in request.POST:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if file_uploadable(konto, form.__sizeof__()):
                if not NameIsFree(form.data['nazwa']):
                    form.save()
                    katalog.lista_plikow.add(Plik.objects.last())
                    return redirect('/storage_control/')
    form = UploadFileForm()
    context_dict["form"] = form
    return render(request, 'file_upload.html', context_dict)


def remove(request, file_id):
    return HttpResponse("You want to remove file %s." %file_id)


def rename(request, file_id):
    return HttpResponse("You want to rename file %s." %file_id)


def move(request, file_id):
    return HttpResponse("You want to move file %s." %file_id)


def change_directory(request, directory_id):
    katalog = Struktura_Konta.objects.get(konto=currentAccount(request.user)).lista_katalogow.get(id=directory_id)
    request.session['current_id'] = katalog.id
    request.session['current_directory'] = katalog.nazwa
    return redirect('/storage_control/')

def storage_control(request):
    context_dict = {}
    use = request.user
    context_dict["use"] = use
    user = User.objects.get(username=request.user)
    konto = currentAccount(user)
    if request.session.get('current_directory', None) is None:
        katalog = Struktura_Konta.objects.get(konto=konto).lista_katalogow.first()
        request.session['current_id'] = katalog.id
        request.session['current_directory'] = katalog.nazwa
    lista = UserFiles(konto, request.session['current_directory'])
    context_dict["konto"] = konto
    context_dict["file"] = lista
    context_dict["pozostalo"] = left_space(konto)
    context_dict["user"] = user
    context_dict["katalogi"] = Struktura_Konta.objects.get(konto=konto)
    #request.session['current_directory'] = None
    #import pdb; pdb.set_trace()

    return render(request, 'storage_control.html', context_dict)


def cloud_menu(request):
    return redirect(request, 'storage_control.html')


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            Konto.objects.create(pojemnosc=500000000, uzytkownik=user)
            Struktura_Konta.objects.create(konto=Konto.objects.get(uzytkownik=user))
            struktura = Struktura_Konta.objects.get(konto=Konto.objects.get(uzytkownik=user))
            Katalog.objects.create(nazwa="folder")
            katalog = Katalog.objects.last()
            struktura.lista_katalogow.add(katalog)

            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})


def login(request, template_name='login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return redirect('../main')
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def error_404_view(request, exception):
    data = {}
    return render(request, 'error_404.html', data)


def error_500_view(request):
    data = {}
    return render(request, 'error_500.html', data)

