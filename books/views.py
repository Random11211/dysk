from django.http import Http404
from django.http import HttpResponse
from django.conf import settings
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
from books.forms import UploadFileForm
from books.models import Konto
from books.models import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect


# Create your views here.

def simple_upload(request):
    context_dict = {}
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        context_dict['uploaded_file_url'] = uploaded_file_url
    lista = Plik.objects.all()
    context_dict["file"] = lista

    return render(request, 'storage_control.html', context_dict)

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
    return render(request, 'home.html')


def storage_control(request):
    Plik.objects.all().delete()
    context_dict = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    form = UploadFileForm()
    context_dict["form"] = form
    lista = Plik.objects.all()
    context_dict["file"] = lista
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
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {'form': form})


def login(request,
          template_name='login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            #if not is_safe_url(url=redirect_to, host=request.get_host()):
            #    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

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
