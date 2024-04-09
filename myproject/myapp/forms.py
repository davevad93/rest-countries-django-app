from django import forms

class CountrySearchForm(forms.Form):
    search_term = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search a country...'
        })
    )

class RegionFilterForm(forms.Form):
    regions = forms.ChoiceField(
        choices=(
            ('All', 'All'),
            ('Africa', 'Africa'),
            ('Americas', 'Americas'),
            ('Antarctic', 'Antarctic'),
            ('Asia', 'Asia'),
            ('Europe', 'Europe'),
            ('Oceania', 'Oceania'),
        ),
        required=False,
    )
