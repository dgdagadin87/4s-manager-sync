import json
from collections import namedtuple

def json2object(data):
    return json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))