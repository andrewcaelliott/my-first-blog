from django import forms

from .models import Post
from .models import NumberFact

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'numberFact',)


class FactForm(forms.ModelForm):

    class Meta:
        model = NumberFact
        fields = ('title', 'number', 'unit', 'subject', 'text',)        