from django import forms
from .models import Profile
from django.forms.widgets import TextInput, Textarea


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('path',)
        widgets = {
                   'serial': TextInput(attrs={'readonly': 'readonly'}),
                    'note': Textarea(attrs={"rows":"3"})
                   }
