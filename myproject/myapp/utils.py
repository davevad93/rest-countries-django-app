import json
import logging
import unicodedata
from pathlib import Path

import requests
import wikipediaapi
from django.core.cache import cache
from requests import RequestException

REST_COUNTRIES_ENDPOINTS = (
    "https://restcountries.com/v3.1/all",
    "https://api.restcountries.com/countries",
)
COUNTRIES_CACHE_KEY = "all_countries"
COUNTRIES_CACHE_SOURCE_KEY = "all_countries_source"
COUNTRIES_CACHE_TIMEOUT = 3600
COUNTRIES_FALLBACK_CACHE_TIMEOUT = 300
COUNTRIES_REQUEST_TIMEOUT_SECONDS = 10
COUNTRIES_SOURCE_REMOTE = "remote"
COUNTRIES_SOURCE_FALLBACK = "fallback"

logger = logging.getLogger(__name__)

# Function to normalize the search term to ASCII, but keep the special characters in the country names.
def normalize_string(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

# Function to fetch countries data from available REST Countries endpoints.
def fetch_countries_data_from_api():
    last_exception = None
    for endpoint in REST_COUNTRIES_ENDPOINTS:
        try:
            response = requests.get(endpoint, timeout=COUNTRIES_REQUEST_TIMEOUT_SECONDS)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, list):
                raise ValueError("Invalid countries payload type, expected a list.")
            return data
        except (RequestException, ValueError, TypeError) as exc:
            last_exception = exc
            logger.warning("Failed to fetch countries data from %s: %s", endpoint, exc)

    if last_exception:
        raise last_exception

    raise ValueError("No REST Countries endpoints configured.")


# Function to fetch and cache countries data.
def fetch_and_cache_countries_data():
    try:
        data = fetch_countries_data_from_api()
        cache.set(COUNTRIES_CACHE_KEY, data, COUNTRIES_CACHE_TIMEOUT)
        cache.set(COUNTRIES_CACHE_SOURCE_KEY, COUNTRIES_SOURCE_REMOTE, COUNTRIES_CACHE_TIMEOUT)
        return data
    except (RequestException, ValueError, TypeError) as exc:
        logger.exception("Failed to fetch countries data from all configured endpoints: %s", exc)
        fallback_data = load_fallback_countries_data()
        cache.set(COUNTRIES_CACHE_KEY, fallback_data, COUNTRIES_FALLBACK_CACHE_TIMEOUT)
        cache.set(COUNTRIES_CACHE_SOURCE_KEY, COUNTRIES_SOURCE_FALLBACK, COUNTRIES_FALLBACK_CACHE_TIMEOUT)
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
    source = cache.get(COUNTRIES_CACHE_SOURCE_KEY)
    if data is None:
        data = fetch_and_cache_countries_data()
    elif source == COUNTRIES_SOURCE_FALLBACK:
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