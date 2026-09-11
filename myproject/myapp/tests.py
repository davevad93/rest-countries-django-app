from django.test import TestCase
from django.core.cache import cache
from unittest.mock import Mock, patch
from requests import RequestException
from .models import Region, Country
from .utils import (
    COUNTRIES_CACHE_KEY,
    COUNTRIES_CACHE_SOURCE_KEY,
    COUNTRIES_SOURCE_FALLBACK,
    COUNTRIES_SOURCE_REMOTE,
    fetch_and_cache_countries_data,
    get_cached_countries_data,
)

class RegionModelTestCase(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name='Europe')

    def test_region_str_representation(self):
        self.assertEqual(str(self.region), 'Europe')

class CountryModelTestCase(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name='Europe')
        self.country = Country.objects.create(
            name='Portugal',
            capital='Lisbon',
            population=10229907,
            region=self.region,
            subregion='Southern Europe',
            currency='Euro',
            language='Portuguese',
            borders='ESP',
            area=92090.0,
            timezone='UTC-01:00',
            top_level_domain='.pt'
        )

    def test_country_str_representation(self):
        self.assertEqual(str(self.country), 'Portugal')
        self.assertEqual(self.country.name, 'Portugal')
        self.assertEqual(self.country.capital, 'Lisbon')
        self.assertEqual(self.country.population, 10229907)
        self.assertEqual(self.country.region, self.region)
        self.assertEqual(self.country.subregion, 'Southern Europe')
        self.assertEqual(self.country.currency, 'Euro')
        self.assertEqual(self.country.language, 'Portuguese')
        self.assertEqual(self.country.borders, 'ESP')
        self.assertEqual(self.country.area, 92090.0)
        self.assertEqual(self.country.timezone, 'UTC-01:00')  
        self.assertEqual(self.country.top_level_domain, '.pt')


class CountriesFetchCacheTestCase(TestCase):
    def setUp(self):
        cache.clear()

    @patch('myapp.utils.requests.get')
    def test_fetch_and_cache_uses_remote_data_when_available(self, mock_get):
        payload = [{'name': {'common': 'Argentina'}, 'population': 1}]
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = payload
        mock_get.return_value = response

        data = fetch_and_cache_countries_data()

        self.assertEqual(data, payload)
        self.assertEqual(cache.get(COUNTRIES_CACHE_KEY), payload)
        self.assertEqual(cache.get(COUNTRIES_CACHE_SOURCE_KEY), COUNTRIES_SOURCE_REMOTE)

    @patch('myapp.utils.requests.get')
    def test_get_cached_countries_data_refreshes_fallback_cache(self, mock_get):
        cache.set(COUNTRIES_CACHE_KEY, [{'name': {'common': 'Portugal'}, 'population': 1}], 300)
        cache.set(COUNTRIES_CACHE_SOURCE_KEY, COUNTRIES_SOURCE_FALLBACK, 300)

        mock_get.side_effect = RequestException("first endpoint failed")

        response = Mock()
        response.raise_for_status.return_value = None
        remote_payload = [{'name': {'common': 'France'}, 'population': 2}]
        response.json.return_value = remote_payload
        mock_get.side_effect = [RequestException("first endpoint failed"), response]

        data = get_cached_countries_data()

        self.assertEqual(data, remote_payload)
        self.assertEqual(cache.get(COUNTRIES_CACHE_KEY), remote_payload)
        self.assertEqual(cache.get(COUNTRIES_CACHE_SOURCE_KEY), COUNTRIES_SOURCE_REMOTE)