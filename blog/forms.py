from django import forms

from .models import Post
from .models import NumberFact
from .models import NumberQuery

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'numberFact',)


class FactForm(forms.ModelForm):

    class Meta:
        model = NumberFact
        fields = ('title', 'number', 'unit', 'subject', 'text',)        

class QueryForm(forms.ModelForm):

    class Meta:
        model = NumberQuery
        fields = ('number','multiple','unit','measure',)                

class ConvertForm(forms.ModelForm):

    class Meta:
        model = NumberQuery
        fields = ('number','multiple','unit','measure','target_unit',)                        