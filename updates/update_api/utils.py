import json

def is_json(data):
    try:
        json_data = json.loads(data)
        is_valid = True
    except ValueError: 
        is_valid = False
    return is_valid