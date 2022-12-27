from django import forms
from datetime import datetime


class BuscadorForm(forms.Form):
    origen = forms.CharField(max_length=50, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Origen'}))
    destino = forms.CharField(max_length=50, label="", widget=forms.TextInput(
        attrs={'placeholder': 'Destino'}))
