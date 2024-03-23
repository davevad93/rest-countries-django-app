import pyuca
from .forms import RegionFilterForm, CountrySearchForm
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .utils import get_cached_countries_data, exclude_countries, get_search_suggestions, filter_countries_by_search_term, filter_countries_by_region, fetch_country_descriptions

# Initialize the collator for sorting.
collator = pyuca.Collator()

# Function to render the home page.
def home(homepage):
    return render(homepage, 'index.html')

# Function to filter countries by region and return the filtered data as a JSON response.
def filter_regions(request):  
    if request.method == 'GET':
        region = request.GET.get('region', '')
        data = get_cached_countries_data()
        data = exclude_countries(data)
        data.sort(key=lambda country: collator.sort_key(country['name']['common']))

        if data:
            filtered_data = filter_countries_by_region(data, region) if region != 'All' else data
            return JsonResponse({'data': render_to_string('filter_countries.html', {'country_data': filtered_data})})

    return JsonResponse({'data': 'Invalid request'}, status=400)

# Function to search for countries.
def search_countries(request):
    search_form = CountrySearchForm(request.GET)
    filter_form = RegionFilterForm(request.GET)

    if request.method == 'GET':
        search_term = request.GET.get('search_term', '')
        data = get_cached_countries_data()
        data = exclude_countries(data)
        data.sort(key=lambda country: collator.sort_key(country['name']['common']))

        if 'autocomplete' in request.GET:
            suggestions = get_search_suggestions(data, search_term)
            return JsonResponse({'suggestions': suggestions})

        if search_term:
            data = filter_countries_by_search_term(data, search_term)
            descriptions = fetch_country_descriptions(data)
            for country in data:
                country['description'] = descriptions.get(country['name']['common'], None)

        return render(request, 'countries.html', {'country_data': data, 'search_form': search_form, 'filter_form': filter_form})
    
# Function to display country information in the HTML template.
def country_info(request):
    data = get_cached_countries_data()
    data = exclude_countries(data)
    data.sort(key=lambda country: collator.sort_key(country['name']['common']))

    search_form = CountrySearchForm(request.GET)
    filter_form = RegionFilterForm(request.GET)

    search_term = request.GET.get('search_term', '')

    if search_term:
        data = filter_countries_by_search_term(data, search_term)
        descriptions = fetch_country_descriptions(data)
        for country in data:
            country['description'] = descriptions.get(country['name']['common'], None)

    elif filter_form.is_valid():
        region = filter_form.cleaned_data.get('region', '')
        if region:
            data = filter_countries_by_region(data, region)

    return render(request, 'countries.html', {'country_data': data, 'search_form': search_form, 'filter_form': filter_form})
