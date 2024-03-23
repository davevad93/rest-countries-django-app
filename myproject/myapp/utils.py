import unicodedata
import requests
import wikipediaapi
from django.core.cache import cache

# Function to normalize the search term to ASCII, but keep the special characters in the country names.
def normalize_string(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

# Function to fetch and cache countries data.
def fetch_and_cache_countries_data():
    data = requests.get("https://restcountries.com/v3.1/all").json()
    cache.set('all_countries', data, 3600)  # Cache data for 1 hour.
    return data

# Function to retrieve cached countries data or fetch if not available.
def get_cached_countries_data():
    data = cache.get('all_countries')
    if data is None:
        data = fetch_and_cache_countries_data()
    return data

# Function to exclude uninhabited territories from the data.
def exclude_countries(data):
    return [country for country in data if country['name']['common'] and 'population' in country and country['population']]

# Function to get autocomplete suggestions with normalized strings.
def get_search_suggestions(data, search_term):
    search_country = normalize_string(search_term.lower())
    return [country['name']['common'] for country in data if normalize_string(country['name']['common'].lower()).startswith(search_country)]

# Function to filter countries by search term with normalized strings.
def filter_countries_by_search_term(data, search_term):
    search_country = normalize_string(search_term.lower())
    return [country for country in data if search_country == normalize_string(country['name']['common'].lower())]

# Function to filter countries by region.
def filter_countries_by_region(data, region):
    return [country for country in data if region in country.get('region', '')]

# Function to handle special cases where the country name does not match the Wikipedia page title.
def get_page_title(country_name):
    special_cases = {
        'Georgia': 'Georgia (country)',
        'Micronesia': 'Federated States of Micronesia',
        'Palestine': 'State of Palestine',
        'Western Sahara': 'Sahrawi Arab Democratic Republic', 
        'Saint Martin': 'Saint Martin (island)'}
    
    return special_cases.get(country_name, country_name)

# Function to fetch country descriptions from Wikipedia.
def fetch_country_descriptions(data):
    descriptions = {}
    wiki_wiki = wikipediaapi.Wikipedia('User Agent', extract_format=wikipediaapi.ExtractFormat.WIKI)

    for country in data:
        country_name = country['name']['common']
        page_title = get_page_title(country_name)
        page = wiki_wiki.page(page_title)
        
        if page.exists():
            descriptions[country_name] = page.summary

    return descriptions