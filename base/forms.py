from django import forms

class testp(forms.Form):
    text = forms.CharField(max_length=200)