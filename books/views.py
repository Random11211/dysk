from django.http import Http404
from django.http import HttpResponse
from django.conf import settings
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
from books.forms import UploadFileForm
from books.models import Konto
from books.models import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from books.forms import SignUpForm

# Create your views here.

#def index(request):
 #   return HttpResponse("Hello")

def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    #User.objects.all().delete()
    return render(request, 'home.html')


def AddKatalog():
    return


def UserFiles(konto: Konto):

    return Plik.objects.all()


def left_space(konto: Konto):
    pliki = Plik.objects.all()
    size = 0
    for i in pliki:
        size += i.adres.size
    return konto.pojemnosc - size


def file_uploadable(pojemnosc, file_size):
    pliki = Plik.objects.all()
    size = 0
    for i in pliki:
        size += i.adres.size
    if size + file_size <= pojemnosc:
        return True
    return False


def file_available(request, file_id):
    return HttpResponse("You want file %s." % file_id)


def NameIsFree(name):
    return Plik.objects.filter(nazwa=name).exists()


def SizePresentation(pojemnosc):
    return True


def remove(request, file_id):
    return HttpResponse("You want to remove file %s." %file_id)


def rename(request, file_id):
    return HttpResponse("You want to rename file %s." %file_id)


def move(request, file_id):
    return HttpResponse("You want to move file %s." %file_id)


def storage_control(request):
    # Plik.objects.all().delete()
    context_dict = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if file_uploadable(5000000, form.__sizeof__()):
                if not NameIsFree(form.data['nazwa']):
                    form.save()
    form = UploadFileForm()
    use = request.user
    context_dict["form"] = form
    context_dict["use"] = use
    user = User.objects.get(username=use.username)
    konto = Konto.objects.get(uzytkownik=user)
    lista = UserFiles(konto)
    context_dict["konto"] = konto
    context_dict["file"] = lista
    context_dict["pozostalo"] = left_space(konto)
    context_dict["user"] = user
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

