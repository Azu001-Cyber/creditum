import os
import requests
import time

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

# Simple in-memory cache
_bank_cache = {"timestamp": 0, "data": []}
CACHE_TTL = 3600  # 1 hour in seconds

def fetch_nigerian_banks():
    """
    Fetch list of Nigerian banks from Paystack API with caching.
    """
    current_time = time.time()

    if current_time - _bank_cache["timestamp"] < CACHE_TTL:
        return True, _bank_cache["data"]

    url = "https://api.paystack.co/bank"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get("status"):
            banks = [
                {"name": bank["name"],  "code": bank["code"]}
                for bank in data.get("data", []) ]
            # Update cache
            _bank_cache["timestamp"] = current_time
            _bank_cache["data"] = banks
            return True, banks
        else:
            return False, data.get("message", "Failed to fetch banks")

    except requests.RequestException as e:
        return False, str(e)
