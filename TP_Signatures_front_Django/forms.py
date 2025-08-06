from django import forms

class PublicKeyUploadForm(forms.Form):
    username = forms.CharField(max_length=100)
    public_key_file = forms.FileField()