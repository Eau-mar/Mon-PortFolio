from django import forms
from .models import LettersMails


class messageForm(forms.Form):
    nom = forms.CharField(max_length=50, required=True, label="Nom")
    email = forms.EmailField(required=True, label="Email")
    message = forms.CharField(widget=forms.Textarea, required=False, label="Message")


class LetterMail(forms.ModelForm):

    class Meta:
        model = LettersMails
        fields = ("mail",)