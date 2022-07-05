from fastapi import status, HTTPException
import requests

def jsonExtract(obj, key):
    # recursively fetch values from nested JSON
    arr = []

    def extract(obj, arr, key):
        # recursively search for values of key in JSON tree
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

def exchangeAPI(endpoint, payload):
    try:
        req = requests.get(endpoint, params=payload)
        return req
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )
