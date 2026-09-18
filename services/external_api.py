import httpx
from fastapi import HTTPException

async def get_usd_rate() -> float:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            usd_value = data["Valute"]["USD"]["Value"]
            return float(usd_value)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="сервис курсов валют долго не отвечает")
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="ошибка при запросе к внешнему сервису валют")