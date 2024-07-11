import requests
from config import env
from typing import Any

def fetch_daily_problem() -> (Any | None):
    response = requests.get(f"{env.API_URL}/daily")

    if response.status_code == 200:
        data = response.json()
        return data

    return None
