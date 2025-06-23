import json
from datetime import datetime, date

class CustomJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime and date objects."""
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

def convert_date(d):
    """Convert string to date object if valid, otherwise return None."""
    if isinstance(d, str) and d:
        try:
            return datetime.fromisoformat(d).date()
        except ValueError:
            return None
    return d
