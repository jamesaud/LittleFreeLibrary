from django import forms
from django.forms import ModelForm, Textarea
from wikiblog.models import Page, Comment, Hashtag


class page_form(ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'bodytext')
        #fields = '__all__'
        
        labels = {
            'title': 'Title',
            'bodytext': 'Content',
            }
        
        widgets = {
            'title': Textarea(attrs={'cols': 60, 'rows': 2, 'value': 'name'},),
            'bodytext': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

class tag_form(forms.Form):
    tag = forms.CharField(label='#tags',
                          widget=forms.Textarea(attrs={'cols': 30, 'rows': 2, 'placeholder': '#separate #your_tags #by #spaces'}),
                          max_length = 70)

class choices_form(forms.Form):
    choices = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple,)

class comment_form(ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        #fields = '__all__'
        
        labels = {
            'content': '',
            }
        
        widgets = {
            'content': Textarea(attrs={'cols': 20, 'rows': 3}),
        }
