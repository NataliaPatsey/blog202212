from django.forms import ModelForm
from django import forms
from blog_app.models import Article

CHOICE_YN = ((0, "No"), (1, "Yes"))

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'title', 'summary', 'text', 'image']


class SearchForm(forms.Form):
    searchtext = forms.CharField(label='Search', max_length=100, initial='type here')
    where = forms.ChoiceField(label='Where',choices=((0, "----"), (1, "Title"), (2, "Summary")))

class ChoiceForm(forms.Form):
    mychoice = forms.ChoiceField(label='Уверены???', choices=CHOICE_YN)



