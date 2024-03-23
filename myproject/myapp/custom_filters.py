import os
import json
from django import template
from django.conf import settings

register = template.Library()

@register.filter
def get_emblems_url(country):
    file_path = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'json', 'emblems.json')
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for info in data:
            if info['country']['name'] == country:
                return info['country']['url']
    return None
