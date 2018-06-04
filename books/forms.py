from django import forms
from books.models import Plik


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Plik
        fields = ('nazwa', 'adres')

