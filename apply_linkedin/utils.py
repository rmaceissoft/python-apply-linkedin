from datetime import date


def parse_meta(meta):
    list_meta = meta.split(',')
    dict_meta = {}
    for item in list_meta:
        key, value = item.split(':')
        dict_meta[key] = value
    return dict_meta


def parse_date(value):
    try:
        day = int(value.get('day', 1))
        month = int(value.get('month', 1))
        year = int(value['year'])
    except:
        return None
    else:
        return date(year, month, day)
    
    
def _import_simplejson():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json  # Python 2.6+
        except ImportError:
            try:
                from django.utils import simplejson as json  # Google App Engine
            except ImportError:
                raise ImportError, "Can't load a json library"

    return json

simplejson = _import_simplejson()