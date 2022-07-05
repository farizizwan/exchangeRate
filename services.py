from fastapi import status, HTTPException
from datetime import date, timedelta
from schemas import Rates, History, Error
from utilities import jsonExtract, exchangeAPI
from config import redis
import json

#@cached(cache = TTLCache(maxsize=64, ttl=60*60))
def getRates(endpoint, convertFrom, to, amount):
    # call redis cache
    cache = redis.get('rates'+convertFrom.upper()+'to'+to.upper())
    # check if redis cache contain data
    if cache != None:
        res = json.loads(cache)
        rates = Rates(
            convertFrom = res['query']['from'],
            to = res['query']['to'],
            rates = res['info']['rate'],
            amount = amount * res['info']['rate'],
            source = 'cache'
        )
        return rates

    # call exchangerate api
    payload = {'from': convertFrom.upper(), 'to': to.upper(), 'amount': amount}
    req = exchangeAPI(endpoint, payload)
    if req.status_code == status.HTTP_200_OK:
        res = req.json()
        if res['info']['rate'] == None:
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND, detail="Currency not found"
            )

        rates = Rates(
            convertFrom = res['query']['from'],
            to = res['query']['to'],
            rates = res['info']['rate'],
            amount = res['result'],
            source = 'api'
        )       
        redis.set('rates'+convertFrom.upper()+'to'+to.upper(), json.dumps(res),60*5)
        return rates
                
    else:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Exchange API response returned not status code 200"
        )


#@cached(cache = TTLCache(maxsize=64, ttl=60*60))
def getHistory(endpoint, base, symbol):
    # call redis cache
    cache = redis.get(f'history{base.upper()}{symbol.upper()}')
    # check if redis cache contain data
    if cache != None:
        res = json.loads(cache)
        names = jsonExtract(res, symbol.upper())
        history = History(
            maximum = max(names),
            minumum = min(names),
            rates = res['rates'],
            source = 'cache'
        )
        return history

    # call exchangerate api
    payload = {'base': base.upper(), 'symbols': symbol.upper(), 'start_date' : date.today() - timedelta(days = 14), 'end_date' : date.today()}
    req = exchangeAPI(endpoint, payload)
    if req.status_code == status.HTTP_200_OK:
        res = req.json()
        names = jsonExtract(res, symbol.upper())
        history = History(
            maximum = max(names),
            minumum = min(names),
            rates = res['rates'],
            source = 'api'
        )
        redis.set(f'history{base.upper()}{symbol.upper()}', json.dumps(res), 60*60*24)
        return history
    else:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Exchange API response returned not status code 200"
        )
