from django import forms

from .models import Post
from .models import NumberFact
from .models import NumberQuery
from .models import ChanceQuery

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'numberFact',)


class FactForm(forms.ModelForm):

    class Meta:
        model = NumberFact
        fields = ('title', 'magnitude', 'unit', 'subject', 'text',)        

class FreeForm(forms.ModelForm):
    class Meta:
        model = NumberQuery
        fields = ('number',)                

class FreeFormCountry(forms.ModelForm):
    class Meta:
        model = NumberQuery
        fields = ('location','number',)                

class QueryForm(forms.ModelForm):

    class Meta:
        model = NumberQuery
        fields = ('magnitude','multiple','unit','measure',)                

class ConvertForm(forms.ModelForm):

    class Meta:
        model = NumberQuery
        fields = ('magnitude','multiple','unit','measure','target_unit',)                        

class FilterFactsForm(forms.Form):
    search = forms.CharField(max_length=50)

class ChanceForm(forms.ModelForm):

    class Meta:
        model = ChanceQuery
        fields = ('probability', 'exposed_items', 'item_text', 'exposed_repetitions', 'repetition_text', 'outcome_count', 'outcome_text', 'repeat_mode')    

