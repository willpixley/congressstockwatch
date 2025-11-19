
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()
from server.models import Stock, CongressMember, Trade
import yfinance as yf

def adjust_sizes(objects, size_field="amount"):
    size_map = {
        0: 500,        # "< 1K" → Avg: 500
        1000: (1000 + 15000) // 2,
        15000: (15000 + 50000) // 2,
        50000: (50000 + 100000) // 2,
        100000: (100000 + 250000) // 2,
        250000: (250000 + 500000) // 2,
        500000: (500000 + 1000000) // 2,
        1000000: (1000000 + 5000000) // 2,
        5000000: (5000000 + 25000000) // 2,
        25000000: (25000000 + 50000000) // 2
    }
    
    for obj in objects:
        size_value = getattr(obj, size_field, None) if hasattr(obj, size_field) else obj.get(size_field)
        if size_value in size_map:
            new_size = size_map[size_value]
            
            if hasattr(obj, size_field):  # If it's a Django model instance
                setattr(obj, size_field, new_size)
                obj.save()
            else:  # If it's a dictionary
                obj[size_field] = new_size

    return objects  # Returns updated objects

