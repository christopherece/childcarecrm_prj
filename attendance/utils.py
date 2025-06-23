from datetime import datetime

def convert_date(d):
    """Convert string to datetime object if valid, otherwise return None."""
    if isinstance(d, str) and d:
        try:
            return datetime.strptime(d, '%Y-%m-%d')
        except ValueError:
            return None
    return d
