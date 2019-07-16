from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

### ModelForms
from .models import Person, Article, User

class PersonForm(forms.ModelForm):
    class Meta:
        model=Person
        fields=['id','first_name','last_name','shirt_size']


class TickerForm(forms.ModelForm):
    pub_date=forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model=Article
        fields=['headline','pub_date','content','reporter']

class ArticleForm(forms.ModelForm):
    class Meta:
        model=Article
        fields=['id','pub_date','headline','content','reporter']
