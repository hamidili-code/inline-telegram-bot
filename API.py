import json

import aiohttp
import os


API_URL = "https://shelow.ir/wp-json/shelow/v1/posts"

async def send_to_api(data: str):
    async with aiohttp.ClientSession() as session:
        params = {}
        if data.strip():
            params["search"] = data.strip()
        async with session.get(
            API_URL,
            params=params{
                "query": data,
                "_embed": 1
            }
        ) as response:

            result = await response.json()


    return result

