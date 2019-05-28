from django import forms

RANKING_CHOICES = ['upload date', 'rating', 'relevance', 'views']
QUALITY_CHOICES = ['best', 'worst']


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=255, label='Keyword')
    api_key = forms.CharField(max_length=255, label='Api Key')
    rank_by = forms.ChoiceField(widget=forms.RadioSelect, choices=RANKING_CHOICES)
    max_result = forms.NumberInput()


class CaptureForm(forms.Form):
    capture_in = forms.NumberInput()
    quality = forms.CharField(label='quality', widget=forms.Select(choices=QUALITY_CHOICES))
    date = forms.CharField(label='Date prefix', widget=forms.DateField())
    title_prefix = forms.CharField(label='title prefix', max_length=255)
