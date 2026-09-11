import pyuca
import logging
from .forms import RegionFilterForm, CountrySearchForm
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .utils import get_cached_countries_data, exclude_countries, get_search_suggestions, filter_countries_by_search_term, filter_countries_by_region, fetch_country_descriptions

# Initialize the collator for sorting.
collator = pyuca.Collator()
logger = logging.getLogger(__name__)
COUNTRIES_UNAVAILABLE_MESSAGE = "Country data is temporarily unavailable. Please try again later."


def prepare_country_data():
    try:
        data = get_cached_countries_data() or []
        if not data:
            return [], COUNTRIES_UNAVAILABLE_MESSAGE
        data = exclude_countries(data)
        if not data:
            return [], COUNTRIES_UNAVAILABLE_MESSAGE
        data.sort(key=lambda country: collator.sort_key(country['name']['common']))
        return data, None
    except Exception as exc:
        logger.exception("Failed to prepare country data: %s", exc)
        return [], COUNTRIES_UNAVAILABLE_MESSAGE

# Function to render the home page.
def home(homepage):
    return render(homepage, 'index.html')

# Function to filter countries by region and return the filtered data as a JSON response.
def filter_regions(request):  
    if request.method == 'GET':
        region = request.GET.get('region', '')
        data, data_error = prepare_country_data()
        if data_error:
            return JsonResponse({'data': f'<div id="no-results"><h1>{data_error}</h1></div>'}, status=503)

        filtered_data = filter_countries_by_region(data, region) if region != 'All' else data
        return JsonResponse({'data': render_to_string('filter_countries.html', {'country_data': filtered_data})})

    return JsonResponse({'data': 'Invalid request'}, status=400)

# Function to search for countries.
def search_countries(request):
    search_form = CountrySearchForm(request.GET)
    filter_form = RegionFilterForm(request.GET)

    if request.method == 'GET':
        search_term = request.GET.get('search_term', '')
        data, data_error = prepare_country_data()
        if data_error and 'autocomplete' in request.GET:
            return JsonResponse({'suggestions': []}, status=503)

        if 'autocomplete' in request.GET:
            suggestions = get_search_suggestions(data, search_term)
            return JsonResponse({'suggestions': suggestions})

        if search_term:
            data = filter_countries_by_search_term(data, search_term)
            descriptions = fetch_country_descriptions(data)
            for country in data:
                country['description'] = descriptions.get(country['name']['common'], None)

        status_code = 503 if data_error else 200
        return render(
            request,
            'countries.html',
            {
                'country_data': data,
                'search_form': search_form,
                'filter_form': filter_form,
                'error_message': data_error,
            },
            status=status_code,
        )
    
# Function to display country information in the HTML template.
def country_info(request):
    data, data_error = prepare_country_data()

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

    status_code = 503 if data_error else 200
    return render(
        request,
        'countries.html',
        {
            'country_data': data,
            'search_form': search_form,
            'filter_form': filter_form,
            'error_message': data_error,
        },
        status=status_code,
    )
