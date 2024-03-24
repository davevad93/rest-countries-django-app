from django.test import TestCase
from .models import Region, Country

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
        