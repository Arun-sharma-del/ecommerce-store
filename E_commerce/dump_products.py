import io
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "E_commerce.settings")
django.setup()

# Dump data to JSON file with UTF-8 encoding
from django.core.management import call_command

with io.open('products_data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'store.product', indent=2, stdout=f)
    