import json
import logging
import unicodedata
from pathlib import Path

import requests
import wikipediaapi
from django.core.cache import cache
from requests import RequestException

REST_COUNTRIES_ENDPOINT = "https://restcountries.com/v3.1/all"
COUNTRIES_CACHE_KEY = "all_countries"
COUNTRIES_CACHE_TIMEOUT = 3600
COUNTRIES_REQUEST_TIMEOUT_SECONDS = 10

logger = logging.getLogger(__name__)

# Function to normalize the search term to ASCII, but keep the special characters in the country names.
def normalize_string(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

# Function to fetch and cache countries data.
def fetch_and_cache_countries_data():
    try:
        response = requests.get(REST_COUNTRIES_ENDPOINT, timeout=COUNTRIES_REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, list):
            raise ValueError("Invalid countries payload type, expected a list.")
        cache.set(COUNTRIES_CACHE_KEY, data, COUNTRIES_CACHE_TIMEOUT)
        return data
    except (RequestException, ValueError, TypeError) as exc:
        logger.exception("Failed to fetch countries data from %s: %s", REST_COUNTRIES_ENDPOINT, exc)
        fallback_data = load_fallback_countries_data()
        cache.set(COUNTRIES_CACHE_KEY, fallback_data, COUNTRIES_CACHE_TIMEOUT)
        return fallback_data


def load_fallback_countries_data():
    file_path = Path(__file__).resolve().parent / 'static' / 'json' / 'countries_fallback.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            if not isinstance(data, list):
                raise ValueError("Fallback countries JSON must contain a list.")
            return data
    except (FileNotFoundError, OSError, json.JSONDecodeError, ValueError) as exc:
        logger.exception("Failed to load fallback countries data from %s: %s", file_path, exc)
        return []

# Function to retrieve cached countries data or fetch if not available.
def get_cached_countries_data():
    data = cache.get(COUNTRIES_CACHE_KEY)
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