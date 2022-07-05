from fastapi import status, Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyHeader, APIKey
from services import getRates, getHistory

API_KEY = "myapikey"
API_KEY_NAME = "api_key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

app = FastAPI()

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN, detail="Invalid credential"
        )

@app.get('/convert')
async def convert(convertFrom: str, to: str, amount: int, api_key: APIKey = Depends(get_api_key)):
    endpoint = "https://api.exchangerate.host/convert"
    rates = getRates(endpoint, convertFrom, to, amount)
    return rates

@app.get('/history')
async def history(base: str, symbol: str, api_key: APIKey = Depends(get_api_key)):
    endpoint = "https://api.exchangerate.host/timeseries"
    history = getHistory(endpoint, base, symbol)
    return history
