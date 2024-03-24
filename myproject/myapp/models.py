from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    capital = models.CharField(max_length=100)
    population = models.IntegerField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    subregion = models.CharField(max_length=100)
    currency = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    borders = models.CharField(max_length=100)
    area = models.FloatField()
    timezone = models.CharField(max_length=100)
    top_level_domain = models.CharField(max_length=100)

    def __str__(self):
        return self.name  
